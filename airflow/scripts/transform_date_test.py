from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql import functions as f


conf = SparkConf()

conf.set("spark.jars.packages","io.delta:delta-core:1.0.0")
conf.set("spark.sql.extensions","io.delta.sql.DeltaSparkSessionExtension")
conf.set("spark.sql.catalog.spark_catalog","org.apache.spark.sql.delta.catalog.DeltaCatalog")


spark = SparkSession.builder.appName("delta_vocab").config(conf=conf).getOrCreate()

df = spark.read.csv("gs://raw_data_lake/omop_vocab/DRUG_STRENGTH.csv",sep="\t",inferSchema=True, header=True, dateFormat="yyyy-MM-dd")

df = df.withColumn('valid_start_date', f.to_date(f.col("valid_start_date").cast("string"),'yyyyMMdd')).withColumn('valid_end_date', f.to_date(f.col("valid_end_date").cast("string"),'yyyyMMdd'))

df.write.format('delta').mode('overwrite').option('overwriteSchema','true').save("gs://optimized_data_lake_2/DRUG_STRENGTH")
