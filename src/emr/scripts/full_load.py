from pyspark.sql import SparkSession


def main():
    spark = SparkSession\
        .builder\
        .appName("JdbcToHudi")\
        .getOrCreate()

    df = spark.read.format('jdbc') \
        .option("url", "jdbc:postgresql://pg-hammerdb.cob4psnojwdw.us-east-1.rds.amazonaws.com:5432/hammerdb") \
        .option('dbtable', 'customer') \
        .option('user', 'postgres') \
        .option('password', 'WQ6psvDWVLA8myZ') \
        .option("driver", "org.postgresql.Driver") \
        .load()

    hudi_options = {
        'hoodie.table.name': 'customer',
        'hoodie.datasource.write.recordkey.field': 'c_w_id,c_d_id,c_id',
        'hoodie.datasource.write.precombine.field': 'c_since',
        'hoodie.datasource.hive_sync.database': 'hammerdb',
        'hoodie.datasource.hive_sync.enable': 'true',
        'hoodie.datasource.hive_sync.table': 'customer',
        'hoodie.datasource.hive_sync.partition_extractor_class': 'org.apache.hudi.hive.NonPartitionedExtractor',
        'hoodie.datasource.write.keygenerator.class': 'org.apache.hudi.keygen.ComplexKeyGenerator',
        'hoodie.datasource.write.operation': 'bulk_insert',
        'hoodie.bulkinsert.sort.mode': 'NONE'
    }

    df.write \
        .format('org.apache.hudi') \
        .options(**hudi_options) \
        .mode('overwrite') \
        .save('s3://da-black-belt-2021-datalakestack-bt3qd-lakebucket-11ejurq2mbulm/hammerdb/customer/')


if __name__ == "__main__":
    main()