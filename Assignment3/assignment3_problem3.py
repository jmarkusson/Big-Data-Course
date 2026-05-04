 #!/usr/bin/env python3

from mrjob.job import MRJob

class MRJobTwitterFollows(MRJob):
    # The final (key,value) pairs returned by the class should be
    # 
    # yield ('most followed id', ???)
    # yield ('most followed', ???)
    # yield ('average followed', ???)
    # yield ('count follows no-one', ???)
    #
    # You will, of course, need to replace ??? with a suitable expression
    def mapper(self, _, line):
        sections = line.split(":")
        user_id = int(sections[0].strip())
        following_string = sections[1].strip()

        if not following_string:
            follow_count = 0
            zero_following_flag = 1
        else:
            follower_list = following_string.split()
            follow_count = len(follower_list)
            zero_following_flag = 0

        yield('GLOBAL', (user_id, follow_count, follow_count, 1, zero_following_flag))

    def combiner(self, key, values):
        local_max_id = -1
        local_max_follower_count = -1
        local_sum_follwers = 0
        local_user_count = 0
        local_sum_zeros = 0

        for v in values:
            max_id, max_f_count, sum_followers, user_count, zero_count = v

            local_sum_follwers += sum_followers
            local_user_count += user_count
            local_sum_zeros += zero_count

            if max_f_count > local_max_follower_count:
                local_max_follower_count = max_f_count
                local_max_id = max_id

        yield('GLOBAL', (local_max_id, local_max_follower_count, local_sum_follwers, local_user_count, local_sum_zeros))

    def reducer(self, key, values):
        global_max_id = -1
        global_max_follower_count = -1
        global_sum_follwers = 0
        global_user_count = 0
        global_sum_zeros = 0

        for v in values:
            max_id, max_f_count, sum_followers, user_count, zero_count = v

            global_sum_follwers += sum_followers
            global_user_count += user_count
            global_sum_zeros += zero_count

            if max_f_count > global_max_follower_count:
                global_max_follower_count = max_f_count
                global_max_id = max_id

        if global_user_count > 0:
            average_follower_count = global_sum_follwers / global_user_count
        else:
            average_follower_count = 0
            
        yield ('most followed id', global_max_id)
        yield ('most followed', global_max_follower_count)
        yield ('average followed', average_follower_count)
        yield ('count follows no-one', global_sum_zeros)
        

if __name__ == '__main__':
    MRJobTwitterFollows.run()