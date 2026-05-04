#!/usr/bin/env python3

from mrjob.job import MRJob
from mrjob.step import MRStep

class MRMineral(MRJob):

    def configure_args(self):
        super(MRMineral, self).configure_args()
        self.add_passthru_arg('-k', type=int, default=1, help='Top k systems')

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

        yield None, (star_system, total)

    def reducer_find_top_k(self, _, star_system_and_totals):
        
        k = self.options.k
        top_k = sorted(star_system_and_totals, key=lambda x: x[1], reverse=True)[:k]

        for star_system, total in top_k:
            yield star_system, total
    
    def steps(self):
        return [
            MRStep(
                mapper=self.mapper,
                reducer=self.reducer
            ),
            MRStep(
                reducer=self.reducer_find_top_k
            )
        ]

if __name__ == '__main__':
    MRMineral().run()