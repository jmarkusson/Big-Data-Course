#!/usr/bin/env python3

import argparse
import sys
import os
from pyspark import SparkContext, SparkConf
import math
import time

def murmur3_32(key, seed):
    """Computes the 32-bit murmur3 hash"""
    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    r1 = 15
    r2 = 13
    m = 5
    n = 0xe6546b64

    data = key.encode('utf-8')
    length = len(data)
    hash = seed

    num_blocks = length // 4

    for i in range(num_blocks):
        k = int.from_bytes(data[i*4:(i+1)*4], byteorder='little')

        k = (k * c1) & 0xffffffff # Appropriate mask
        k = rol32(k, r1)
        k = (k * c2) & 0xffffffff

        hash ^= k
        hash = rol32(hash, r2)
        hash = ((hash * m) + n) & 0xffffffff

    tail_index = num_blocks * 4
    remaining_bytes = length % 4

    k1 = int.from_bytes(data[tail_index:tail_index + remaining_bytes], byteorder='little')
    if remaining_bytes > 0:
        k1 = (k1 * c1) & 0xffffffff
        k1 = rol32(k1, r1)
        k1 = (k1 * c2) & 0xffffffff
        hash ^= k1


    # Exakt som står på wiki
    hash ^= length

    hash ^= (hash >> 16)
    hash = (hash * 0x85ebca6b) & 0xffffffff
    hash ^= (hash >> 13)
    hash = (hash * 0xc2b2ae35) & 0xffffffff
    hash ^= (hash >> 16)

    return hash

def rol32(x,k):
    """Auxiliary function (left rotation for 32-bit words)"""
    return ((x << k) | (x >> (32-k))) & 0xffffffff

def auto_int(x):
    """Auxiliary function to help convert e.g. hex integers"""
    return int(x,0)

def dlog2(n):
    return n.bit_length() - 1

def rho(n):
    """Given a 32-bit number n, return the 1-based position of the first
    1-bit"""
    if n == 0:
        return 0
    return 32 - n.bit_length() + 1

def compute_jr(key,seed,log2m):
    """hash the string key with murmur3_32, using the given seed
    then take the **least significant** log2(m) bits as j
    then compute the rho value **from the left**

    E.g., if m = 1024 and we compute hash value 0x70ffec73
    or 0b01110000111111111110110001110011
    then j = 0b0001110011 = 115
         r = 2
         since the 2nd digit of 0111000011111111111011 is the first 1

    Return a tuple (j,r) of integers
    """
    h = murmur3_32(key,seed)
    j = ~(0xffffffff << log2m) & h
    r = rho(h)
    return j, r

def get_files(path):
    """
    A generator function: Iterates through all .txt files in the path and
    returns the content of the files

    Parameters:
    - path : string, path to walk through

    Yields:
    The content of the files as strings
    """
    for (root, dirs, files) in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                path = f'{root}/{file}'
                with open(path,'r') as f:
                    yield f.read()

def alpha(m):
    """Auxiliary function: bias correction"""
    if m == 16:
        return 0.673
    elif m == 32:
        return 0.697
    elif m == 64:
        return 0.709
    else:
            return 0.7213 / (1.0 + 1.079 / m)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Using HyperLogLog, computes the approximate number of '
            'distinct words in all .txt files under the given path.'
    )
    parser.add_argument('path',help='path to walk',type=str)
    parser.add_argument('-s','--seed',type=auto_int,default=0,help='seed value')
    parser.add_argument('-m','--num-registers',type=int,required=True,
                            help=('number of registers (must be a power of two)'))
    parser.add_argument('-w','--num-workers',type=int,default=1,
                        help='number of Spark workers')
    args = parser.parse_args()

    seed = args.seed
    m = args.num_registers
    if m <= 0 or (m&(m-1)) != 0:
        sys.stderr.write(f'{sys.argv[0]}: m must be a positive power of 2\n')
        quit(1)
    log2m = dlog2(m)

    num_workers = args.num_workers
    if num_workers < 1:
        sys.stderr.write(f'{sys.argv[0]}: must have a positive number of '
                         'workers\n')
        quit(1)

    path = args.path
    if not os.path.isdir(path):
        sys.stderr.write(f"{sys.argv[0]}: `{path}' is not a valid directory\n")
        quit(1)

    start = time.time()
    conf = SparkConf()
    conf.setMaster(f'local[{num_workers}]')
    conf.set('spark.driver.memory', '16g')
    sc = SparkContext(conf=conf)

    data = sc.parallelize(get_files(path))

    # Implement HyperLogLog here

    words = data.flatMap(lambda text: text.split())
    jr_pairs = words.map(lambda word: compute_jr(word, seed, log2m))
    max_r_in_j = jr_pairs.reduceByKey(lambda r1, r2: max(r1, r2))
    M_dict = max_r_in_j.collectAsMap()

    M = [0] * m
    for j, r in M_dict.items():
        M[j] = r

    # Harmonic mean
    Z = 1.0 / sum(math.pow(2.0, -val) for val in M)
    
    # Cardinality Estimate
    E = alpha(m) * (m ** 2) * Z

    # Linear counting correction that was used in flajolets algorithm
    if E <= 2.5 * m:
        V = M.count(0)
        if V > 0:
            E = m * math.log(m / float(V)) # Counting zeros instead.
    
    end = time.time()

    print(f'Cardinality estimate: {E}')
    print(f'Number of workers: {num_workers}')
    print(f'Took {end-start} s')

    
    