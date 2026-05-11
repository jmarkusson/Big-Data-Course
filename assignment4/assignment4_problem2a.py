import time
import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, to_date
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import year, floor
import pandas as pd
import sys


@udf(returnType=IntegerType())
def jdn(dt):
    """
    Computes the Julian date number for a given date.
    Parameters:
    - dt, datetime : the Gregorian date for which to compute the number

    Return value: an integer denoting the number of days since January 1, 
    4714 BC in the proleptic Julian calendar.
    """
    y = dt.year
    m = dt.month
    d = dt.day
    if m < 3:
        y -= 1
        m += 12
    a = y//100
    b = a//4
    c = 2-a+b
    e = int(365.25*(y+4716))
    f = int(30.6001*(m+1))
    jd = c+d+e+f-1524
    return jd

    
# you probably want to use a function with this signature for computing the
# simple linear regression with least squares using applyInPandas()
# key is the group key, df is a Pandas dataframe
# should return a Pandas dataframe
def lsq(key,df):
    df = df.dropna(subset=['JDN', 'TAVG']) # Incase of na-vals


    x = df['JDN']
    y = df['TAVG']


    x_mean = x.mean()
    y_mean = y.mean()
    delta_x = x - x_mean
    delta_y = y - y_mean

    numerator = (delta_x * delta_y).sum()
    denominator = (delta_x ** 2).sum()


    if denominator == 0:
        beta = 0.0
    else:
        beta = numerator / denominator

    return pd.DataFrame([{
        "STATION": key[0],
        "BETA": beta
    }])

    


if __name__ == '__main__':
    # do not change the interface
    parser = argparse.ArgumentParser(description = \
                                    'Compute climate data.')
    parser.add_argument('-w','--num-workers',default=1,type=int,
                            help = 'Number of workers')
    parser.add_argument('filename',type=str,help='Input filename')
    args = parser.parse_args()

    # this bit is important: by default, Spark only allocates 1 GiB of memory 
    # which will likely cause an out of memory exception with the full data

    start_time_total = time.time()

    spark = SparkSession.builder \
            .master(f'local[{args.num_workers}]') \
            .config("spark.driver.memory", "16g") \
            .config("spark.ui.enabled", "false") \
            .getOrCreate()
    
    # read the CSV file into a pyspark.sql dataframe and compute the things you need

    reading_time_start = time.time()

    df = spark.read.csv(args.filename, header=True, inferSchema=True)

    reading_time = time.time() - reading_time_start

    computation_time_start = time.time()

    df = df.withColumn("parsed_date", to_date(col("DATE"), "yyyy-MM-dd"))
    df = df.withColumn("YEAR", year(col("parsed_date")))
    df = df.withColumn("JDN", jdn(col("parsed_date")))
    df = df.drop("parsed_date")

    df = df.withColumn("TAVG", (col("TMIN") + col("TMAX")) / 2.0)

    df = df.withColumn("DECADE", (floor(col("YEAR") / 10) * 10))

    df = df.cache()
    df.count()

    decade_avg = df.groupBy("STATION", "DECADE") \
        .avg("TAVG") \
        .withColumnRenamed("avg(TAVG)", "AVG_TEMP_DECADE")

    slopes = df.groupBy("STATION").applyInPandas(
        lsq,
        schema="STATION string, BETA double"
    ).cache()
    slopes.count()

    station_names = df.select("STATION", "NAME").distinct()
    slopes_with_name = slopes.join(station_names, on="STATION", how="left") 


    # top 5 slopes are printed here
    # replace None with your dataframe, list, or an appropriate expression
    # replace STATIONCODE, STATIONNAME, and BETA with appropriate expressions
    top5_slopes = slopes_with_name.orderBy(col("BETA").desc()).limit(5).collect()
    
    print('Top 5 coefficients:')
    for row in top5_slopes:
        print(f'{row["STATION"]} at {row["NAME"]} BETA={row["BETA"]:0.3e} °F/d')

    # replace None with an appropriate expression
    positive_count = slopes.filter(col("BETA") > 0).count()
    total_count = slopes.count()
    fraction_positive = positive_count / total_count if total_count > 0 else 0
    print('Fraction of positive coefficients:')
    print(fraction_positive)

    # Five-number summary of slopes, replace with appropriate expressions

    summary = slopes.select("BETA").summary("min", "25%", "50%", "75%", "max").collect()
    
    beta_min = float(summary[0]["BETA"])
    beta_q1 = float(summary[1]["BETA"])
    beta_median = float(summary[2]["BETA"])
    beta_q3 = float(summary[3]["BETA"])
    beta_max = float(summary[4]["BETA"])
    print('Five-number summary of BETA values:')
    print(f'beta_min {beta_min:0.3e}')
    print(f'beta_q1 {beta_q1:0.3e}')
    print(f'beta_median {beta_median:0.3e}')
    print(f'beta_q3 {beta_q3:0.3e}')
    print(f'beta_max {beta_max:0.3e}')

    # Here you will need to implement computing the decadewise differences 
    # between the average temperatures of 1910s and 2010s
    
    filtered = decade_avg.filter(
    (col("DECADE") == 1910) | (col("DECADE") == 2010)
    )

    pivoted = filtered.groupBy("STATION").pivot("DECADE").avg("AVG_TEMP_DECADE")    
    pivoted = pivoted.withColumn(
        "TAVGDIFF",
        col("2010") - col("1910")
    )    
    pivoted = pivoted.dropna(subset=["1910", "2010"])

    pivoted = pivoted.withColumn("TAVGDIFF", (col("TAVGDIFF") * (5/9))) 

    # There should probably be an if statement to check if any such values were 
    # computed (no suitable stations in the tiny dataset!)

    # Note that values should be printed in celsius

    # Replace None with an appropriate expression
    # Replace STATION, STATIONNAME, and TAVGDIFF with appropriate expressions

    #JOIN AGAIN TO GET NAMES
    station_names = df.select("STATION", "NAME").distinct()
    result = pivoted.join(station_names, on="STATION", how="left").cache()
    result.count()

    positive = result.filter(col("TAVGDIFF") > 0)
    top5_diff = result.orderBy(col("TAVGDIFF").desc()).limit(5).collect()

    print('Top 5 differences:')
    for row in top5_diff:
        print(f'{row["STATION"]} at {row["NAME"]} difference {row["TAVGDIFF"]:0.1f} °C)')

    positive_diff_count = positive.count()
    total_diff_count = result.count()
    fraction_positive_diff = positive_diff_count / total_diff_count if total_diff_count > 0 else 0
    # replace None with an appropriate expression
    print('Fraction of positive differences:')
    print(fraction_positive_diff)

    if total_diff_count > 0:
        diff_summary = result.select("TAVGDIFF").summary("min", "25%", "50%", "75%", "max").collect()
        tdiff_min = float(diff_summary[0]["TAVGDIFF"])
        tdiff_q1 = float(diff_summary[1]["TAVGDIFF"])
        tdiff_median = float(diff_summary[2]["TAVGDIFF"])
        tdiff_q3 = float(diff_summary[3]["TAVGDIFF"])
        tdiff_max = float(diff_summary[4]["TAVGDIFF"])
        # Five-number summary of temperature differences, replace with appropriate expressions
        print('Five-number summary of decade average difference values:')
        print(f'tdiff_min {tdiff_min:0.1f} °C')
        print(f'tdiff_q1 {tdiff_q1:0.1f} °C')
        print(f'tdiff_median {tdiff_median:0.1f} °C')
        print(f'tdiff_q3 {tdiff_q3:0.1f} °C')
        print(f'tdiff_max {tdiff_max:0.1f} °C')

    computation_time = time.time() - computation_time_start
    total_time = time.time() - start_time_total


    # Add your time measurements here
    # It may be interesting to also record more fine-grained times (e.g., how 
    # much time was spent computing vs. reading data)
    print(f'num workers: {args.num_workers}')
    print(f'total time: {total_time:0.1f} s')
    print(f'total reading time: {reading_time:0.1f} s')
    print(f'total computation time: {computation_time:0.1f} s')
