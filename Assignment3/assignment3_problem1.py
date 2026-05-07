#!/usr/bin/env python3

from mrjob.job import MRJob

class MRMineral(MRJob):

    def mapper(self, _, row):

        cols = row.split(',')

        
        if cols[5] == "Mineral Value (RU)":
            return

        star = cols[0]
        constellation = cols[1]

        try:
            mineral_value = float(cols[5])
        except:
            return

        if star == "Prime":
            star_system = constellation
        else:
            star_system = star + " " + constellation

        yield star_system, mineral_value


    def reducer(self, star_system, list_of_mineral_values):

        total = sum(list_of_mineral_values)

        yield star_system, total

if __name__ == '__main__':
    MRMineral().run()