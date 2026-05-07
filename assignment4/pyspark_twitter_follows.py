#!/usr/bin/env python3

import time
import argparse
import findspark
findspark.init()
from pyspark import SparkContext

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = \
                                    'Compute Twitter follows.')
    parser.add_argument('-w','--num-workers',default=1,type=int,
                            help = 'Number of workers')
    parser.add_argument('filename',type=str,help='Input filename')
    args = parser.parse_args()

    start = time.time()
    sc = SparkContext(master = f'local[{args.num_workers}]')

    lines = sc.textFile(args.filename)

    def parse_line(line):
        user, followers = line.split(":")
        user = user.strip()
        followers = followers.strip()

        if not followers:
            follow_count = 0
            zero_follow_flag = 1
        else:
            follow_count = len([
                f for f in followers.replace(",", " ").split()
                if f.strip() != ""
            ])
            zero_follow_flag = 0

        return (user, follow_count, zero_follow_flag)

    def seq_op(accumulator, record):
        max_user, max_count, total, count, zero_count = accumulator
        user, follow_count, zero_follow_flag = record

        if follow_count > max_count:
            max_user = user
            max_count = follow_count

        return (
            max_user,
            max_count,
            total + follow_count,
            count + 1,
            zero_count + zero_follow_flag,
        )

    def comb_op(left, right):
        left_max_user, left_max_count, left_total, left_count, left_zero = left
        right_max_user, right_max_count, right_total, right_count, right_zero = right

        if right_max_count > left_max_count:
            max_user = right_max_user
            max_count = right_max_count
        else:
            max_user = left_max_user
            max_count = left_max_count

        return (
            max_user,
            max_count,
            left_total + right_total,
            left_count + right_count,
            left_zero + right_zero,
        )

    initial = (None, -1, 0, 0, 0)
    max_user, max_count, total, count, num_users_with_no_follow = lines.map(parse_line).aggregate(
        initial,
        seq_op,
        comb_op,
    )

    avg = total / count if count > 0 else 0
    end = time.time()
    
    total_time = end - start

    # the first ??? should be the twitter id
    print(f'max follows: {max_user} follows {max_count}')
    print(f'users follow on average: {avg}')
    print(f'number of user who follow no-one: {num_users_with_no_follow}')
    print(f'num workers: {args.num_workers}')
    print(f'total time: {total_time}')

    sc.stop()

