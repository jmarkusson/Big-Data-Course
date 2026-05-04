 #!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class MRJobTwitterFollowers(MRJob):
    # The final (key,value) pairs returned by the class should be
    # 
    # yield ('most followers id', ???)
    # yield ('most followers', ???)
    # yield ('average followers', ???)
    # yield ('count no followers', ???)
    #
    # You will, of course, need to replace ??? with a suitable expression
    def steps(self):
        return [MRStep(mapper = self.mapper1, 
                       combiner = self.reducer1, 
                       reducer = self.reducer1),
                       
                MRStep(mapper = self.mapper2, 
                       combiner = self.combiner, 
                       reducer = self.reducer2)
                       ]

    def mapper1(self, _, line):
        sections = line.split(":")
        user_id = int(sections[0].strip())
        following_string = sections[1].strip()

        yield(user_id, 0) # Makes sure don't miss to register this user

        if following_string:
            following_list = following_string.split()
            for user in following_list:
                yield(int(user), 1)

    def reducer1(self, user, counts):
        # Acting as reducer and combiner
        yield(user, sum(counts))

    def mapper2(self, user, sum_followers):
        if sum_followers == 0:
            zero_followers = 1
        else:
            zero_followers = 0
        
        yield("GLOBAL", (user, sum_followers, sum_followers, 1, zero_followers))

    def combiner(self, key, values):
        local_max_id = -1
        local_max_follower_count = -1
        local_sum_follwers = 0
        local_user_count = 0
        local_sum_zeros = 0

        for v in values:
            user_id, max_follower_count, sum_followers, user_count, zero_count = v

            local_sum_follwers += sum_followers
            local_user_count += user_count
            local_sum_zeros += zero_count

            if max_follower_count > local_max_follower_count:
                local_max_follower_count = max_follower_count
                local_max_id = user_id

        yield('GLOBAL', (local_max_id, local_max_follower_count, local_sum_follwers, local_user_count, local_sum_zeros))

    def reducer2(self, key, values):
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
            
        yield ('most followers id', global_max_id)
        yield ('most followers', global_max_follower_count)
        yield ('average followers', average_follower_count)
        yield ('count no followers', global_sum_zeros)

if __name__ == '__main__':
    MRJobTwitterFollowers.run()

