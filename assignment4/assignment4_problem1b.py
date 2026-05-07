#!/usr/bin/env python3

import time
import argparse
import findspark
findspark.init()
from pyspark import SparkContext

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
                                    'Compute Twitter followers.')
    parser.add_argument('-w','--num-workers',default=1,type=int,
                            help = 'Number of workers')
    parser.add_argument('filename',type=str,help='Input filename')
    args = parser.parse_args()

    start = time.time()
    sc = SparkContext(master = f'local[{args.num_workers}]')

    lines = sc.textFile(args.filename)

    # fill in your code here
    def parse_line(line):
        user, following = line.split(":")
        user = user.strip()
        following = following.strip()

        results = [(user, 0)]

        if following:
            for followed_user in following.split():
                results.append((followed_user, 1))
                
        return results 

    def seq_op(accumulator, record):
        max_user, max_count, total_follower_count, total_users, no_followers_count = accumulator
        user, follower_count = record

        if follower_count > max_count:
            max_user = user
            max_count = follower_count

        return (
            max_user,
            max_count,
            total_follower_count + follower_count,
            total_users + 1,
            no_followers_count + (1 if follower_count == 0 else 0)
        )

    def comb_op(left, right):
        if right[1] > left[1]:
            max_user = right[0]
            max_count = right[1]
        else:
            max_user = left[0]
            max_count = left[1]
        
        return (
            max_user,
            max_count,
            left[2] + right[2],
            left[3] + right[3],
            left[4] + right[4],
        )
                

    initial = (None, -1, 0, 0, 0)
    follower_counts = lines.flatMap(parse_line).reduceByKey(lambda a, b: a + b)
    
    max_user, max_count, total_follower_count, total_users, no_followers_count = follower_counts.aggregate(
        initial,
        seq_op,
        comb_op,
    )

    average_followers = total_follower_count / total_users if total_users > 0 else 0

    end = time.time()
    
    total_time = end - start

    # the first ??? should be the twitter id
    print(f'max followers: {max_user} has {max_count} followers')
    print(f'followers on average: {average_followers}')
    print(f'number of user with no followers: {no_followers_count}')
    print(f'num workers: {args.num_workers}')
    print(f'total time: {total_time}')
