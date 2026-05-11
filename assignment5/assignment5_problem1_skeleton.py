#!/usr/bin/env python3

import argparse

def rol32(x,k):
    """Auxiliary function (left rotation for 32-bit words)"""
    return ((x << k) | (x >> (32-k))) & 0xffffffff

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


def auto_int(x):
    """Auxiliary function to help convert e.g. hex integers"""
    return int(x,0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Computes MurMurHash3 for the keys.'
    )
    parser.add_argument('key',nargs='*',help='key(s) to be hashed',type=str)
    parser.add_argument('-s','--seed',type=auto_int,default=0,help='seed value')
    args = parser.parse_args()

    seed = args.seed
    for key in args.key:
        h = murmur3_32(key,seed)
        print(f'{h:#010x}\t{key}')
        