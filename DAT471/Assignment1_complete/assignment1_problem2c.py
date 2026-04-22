#!/usr/bin/env python3

import sys
import duckdb

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write(f'Usage: {sys.argv[0]} <input_csv>\n')
        sys.exit(1)
    
    input_csv = sys.argv[1]
    

    with duckdb.connect(database=":memory:") as con:
        con.execute('CREATE VIEW hour AS SELECT * FROM ' + 
                    f'read_csv_auto(\'{input_csv}\', header=True);')

        print("How many rows of data are in the file?")
        sql_query1 = "SELECT COUNT(*) FROM hour;"
        print(con.execute(sql_query1).df())
        print()

        print("What was the average hourly count of bike rentals?")
        sql_query2 = "SELECT AVG(cnt) FROM hour;"
        print(con.execute(sql_query2).df())
        print()

        print("Which were the top-5 busiest hours in terms of average bike rentals?")
        sql_query3 = """SELECT hr, AVG(cnt) AS avg_cnt FROM hour 
                        GROUP BY hr 
                        ORDER BY avg_cnt DESC 
                        LIMIT 5;"""
        print(con.execute(sql_query3).df())
        print()

        print("What was the average daily count of bike rentals in January 2012?")
        sql_query4 = """SELECT AVG(daily_cnt) AS avg_daily_cnt
                        FROM (
                            SELECT dteday, SUM(cnt) AS daily_cnt
                            FROM hour
                            WHERE yr = 1 AND mnth = 1
                            GROUP BY dteday
                        ) tot;"""
        print(con.execute(sql_query4).df())