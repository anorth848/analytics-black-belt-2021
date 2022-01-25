spark-submit --class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer \
/usr/lib/spark/jars/hudi-utilities-bundle_2.12-0.10.0.jar \
--table-type COPY_ON_WRITE \
--source-ordering-field trx_seq \
--source-class org.apache.hudi.utilities.sources.ParquetDFSSource \
--target-base-path s3://da-black-belt-2021-datalakestack-silverlakebucket-112e2j6kous0x/rdbms_analytics/ --target-table hammerdb_public_warehouse \
--transformer-class org.apache.hudi.utilities.transform.AWSDmsTransformer \
--payload-class org.apache.hudi.payload.AWSDmsAvroPayload \
--hoodie-conf hoodie.datasource.write.recordkey.field=w_id,\
hoodie.table.name=hammerdb_public_warehouse,\
hoodie.datasource.write.precombine.field=trx_seq,\
hoodie.datasource.hive_sync.database=rdbms_analytics,\
hoodie.datasource.hive_sync.enable=true,\
hoodie.datasource.hive_sync.table=hammerdb_public_warehouse,\
hoodie.datasource.write.hive_style_partitioning=true,\
hoodie.deltastreamer.source.dfs.root=s3://da-black-belt-2021-datalakestack-bronzelakebucket-19216ilyowszc/rdbms_analytics/cdc/hammerdb/public/warehouse/,\
hoodie.datasource.hive_sync.partition_extractor_class=org.apache.hudi.hive.NonPartitionedExtractor,\
hoodie.datasource.writer.operation=upsert



--class
org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer
--table-type
COPY_ON_WRITE
--source-ordering-field
trx_seq
--source-class
org.apache.hudi.utilities.sources.ParquetDFSSource
--target-base-path
s3://da-black-belt-2021-datalakestack-silverlakebucket-112e2j6kous0x/rdbms_analytics/hammerdb_public_warehouse/
--target-table
hammerdb_public_warehouse
--transformer-class
org.apache.hudi.utilities.transform.AWSDmsTransformer
--payload-class
org.apache.hudi.payload.AWSDmsAvroPayload
--hoodie-conf hoodie.datasource.write.recordkey.field=w_id,hoodie.table.name=hammerdb_public_warehouse,hoodie.datasource.write.precombine.field=trx_seq,hoodie.datasource.hive_sync.database=rdbms_analytics, hoodie.datasource.hive_sync.enable=true,hoodie.datasource.hive_sync.table=hammerdb_public_warehouse,hoodie.datasource.write.hive_style_partitioning=true,hoodie.deltastreamer.source.dfs.root=s3://da-black-belt-2021-datalakestack-bronzelakebucket-19216ilyowszc/rdbms_analytics/cdc/hammerdb/public/warehouse/,hoodie.datasource.hive_sync.partition_extractor_class=org.apache.hudi.hive.NonPartitionedExtractor,hoodie.datasource.writer.operation=upsert



spark-submit --deploy-mode client --class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer /usr/lib/spark/jars/hudi-utilities-bundle_2.12-0.10.0.jar --table-type COPY_ON_WRITE --source-ordering-field trx_seq --source-class org.apache.hudi.utilities.sources.ParquetDFSSource --target-base-path s3://da-black-belt-2021-datalakestack-silverlakebucket-112e2j6kous0x/rdbms_analytics/hammerdb_public_warehouse/ --target-table hammerdb_public_warehouse --transformer-class org.apache.hudi.utilities.transform.AWSDmsTransformer --payload-class org.apache.hudi.payload.AWSDmsAvroPayload --hoodie-conf hoodie.datasource.write.recordkey.field=w_id,hoodie.table.name=hammerdb_public_warehouse,hoodie.datasource.write.precombine.field=trx_seq,hoodie.datasource.hive_sync.database=rdbms_analytics,hoodie.datasource.hive_sync.enable=true,hoodie.datasource.hive_sync.table=hammerdb_public_warehouse,hoodie.datasource.write.hive_style_partitioning=true,hoodie.deltastreamer.source.dfs.root=s3://da-black-belt-2021-datalakestack-bronzelakebucket-19216ilyowszc/rdbms_analytics/cdc/hammerdb/public/warehouse/,hoodie.datasource.hive_sync.partition_extractor_class=org.apache.hudi.hive.NonPartitionedExtractor,hoodie.datasource.writer.operation=upsert,hoodie.datasource.write.partitionpath.field=,hoodie.datasource.write.keygenerator.class=org.apache.hudi.keygen.SimpleKeyGenerator

spark-submit --deploy-mode client --class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer /usr/lib/spark/jars/hudi-utilities-bundle_2.12-0.10.0.jar --table-type COPY_ON_WRITE --source-ordering-field trx_seq --source-class org.apache.hudi.utilities.sources.ParquetDFSSource --target-base-path s3://da-black-belt-2021-datalakestack-silverlakebucket-112e2j6kous0x/rdbms_analytics/hammerdb_public_warehouse/ --target-table hammerdb_public_warehouse --transformer-class org.apache.hudi.utilities.transform.AWSDmsTransformer --payload-class org.apache.hudi.payload.AWSDmsAvroPayload --hoodie-conf hoodie.datasource.write.recordkey.field=w_id,hoodie.table.name=hammerdb_public_warehouse,hoodie.datasource.write.precombine.field=trx_seq,hoodie.datasource.hive_sync.database=rdbms_analytics,hoodie.datasource.hive_sync.enable=true,hoodie.datasource.hive_sync.table=hammerdb_public_warehouse,hoodie.datasource.write.hive_style_partitioning=true,hoodie.deltastreamer.source.dfs.root=s3://da-black-belt-2021-datalakestack-bronzelakebucket-19216ilyowszc/rdbms_analytics/cdc/hammerdb/public/warehouse/,hoodie.datasource.hive_sync.partition_extractor_class=org.apache.hudi.hive.NonPartitionedExtractor,hoodie.datasource.writer.operation=upsert


spark-submit --deploy-mode client --class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer /usr/lib/spark/jars/hudi-utilities-bundle_2.12-0.10.0.jar --table-type COPY_ON_WRITE --source-ordering-field trx_seq --source-class org.apache.hudi.utilities.sources.ParquetDFSSource --target-base-path s3://da-black-belt-2021-datalakestack-silverlakebucket-112e2j6kous0x/rdbms_analytics/hammerdb_public_warehouse/ --target-table hammerdb_public_warehouse --transformer-class org.apache.hudi.utilities.transform.AWSDmsTransformer --payload-class org.apache.hudi.payload.AWSDmsAvroPayload --hoodie-conf hoodie.datasource.write.recordkey.field=w_id --hodie-conf hoodie.table.name=hammerdb_public_warehouse --hoodie-conf hoodie.datasource.write.precombine.field=trx_seq --hoodie-conf hoodie.datasource.hive_sync.database=rdbms_analytics --hoodie-conf hoodie.datasource.hive_sync.enable=true --hoodie-conf hoodie.datasource.hive_sync.table=hammerdb_public_warehouse --hoodie-conf hoodie.datasource.write.hive_style_partitioning=true --hoodie-conf hoodie.deltastreamer.source.dfs.root=s3://da-black-belt-2021-datalakestack-bronzelakebucket-19216ilyowszc/rdbms_analytics/cdc/hammerdb/public/warehouse/ --hoodie-conf hoodie.datasource.hive_sync.partition_extractor_class=org.apache.hudi.hive.NonPartitionedExtractor --hoodie-conf hoodie.datasource.writer.operation=upsert


spark-submit --deploy-mode client --class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer
/usr/lib/spark/jars/hudi-utilities-bundle_2.12-0.10.0.jar
--table-type COPY_ON_WRITE
--source-ordering-field trx_seq
--source-class org.apache.hudi.utilities.sources.ParquetDFSSource
--target-base-path s3://da-black-belt-2021-datalakestack-silverlakebucket-112e2j6kous0x/rdbms_analytics/hammerdb_public_warehouse/
--target-table hammerdb_public_warehouse
--transformer-class org.apache.hudi.utilities.transform.AWSDmsTransformer
--payload-class org.apache.hudi.payload.AWSDmsAvroPayload
--enable-hive-sync
--hoodie-conf hoodie.datasource.write.recordkey.field=w_id
--hoodie-conf hoodie.table.name=hammerdb_public_warehouse
--hoodie-conf hoodie.datasource.write.precombine.field=trx_seq
--hoodie-conf hoodie.datasource.hive_sync.database=rdbms_analytics
--hoodie-conf hoodie.datasource.hive_sync.enable=true
--hoodie-conf hoodie.datasource.hive_sync.table=hammerdb_public_warehouse
--hoodie-conf hoodie.deltastreamer.source.dfs.root=s3://da-black-belt-2021-datalakestack-bronzelakebucket-19216ilyowszc/rdbms_analytics/full/hammerdb/public/warehouse/
--hoodie-conf hoodie.datasource.write.keygenerator.class=org.apache.hudi.keygen.NonpartitionedKeyGenerator

--hoodie-conf hoodie.datasource.hive_sync.partition_extractor_class=org.apache.hudi.hive.NonPartitionedExtractor
--hoodie-conf hoodie.datasource.write.keygenerator.class=org.apache.hudi.keygen.SimpleKeyGenerator
--hoodie-conf hoodie.datasource.write.partitionpath.field=""

#--hoodie-conf hoodie.datasource.writer.operation=upsert
--hoodie-conf hoodie.datasource.write.hive_style_partitioning=true
--hoodie-conf hoodie.datasource.write.keygenerator.class=org.apache.hudi.keygen.SimpleKeyGenerator
--hoodie-conf hoodie.datasource.write.keygenerator.class=org.apache.hudi.keygen.NonpartitionedKeyGenerator







sudo -u hadoop -i spark-submit --deploy-mode client \
--class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer \
/usr/lib/hudi/hudi-utilities-bundle.jar \
--table-type COPY_ON_WRITE --source-ordering-field trx_seq \
--source-class org.apache.hudi.utilities.sources.ParquetDFSSource \
--target-base-path s3://da-black-belt-2021-datalakestack-silverlakebucket-112e2j6kous0x/rdbms_analytics/hammerdb_public_warehouse2/ \
--target-table hammerdb_public_warehouse --transformer-class org.apache.hudi.utilities.transform.AWSDmsTransformer \
--enable-hive-sync \
--hoodie-conf hoodie.datasource.write.recordkey.field=w_id \
--hoodie-conf hoodie.table.name=hammerdb_public_warehouse2 \
--hoodie-conf hoodie.datasource.write.precombine.field=trx_seq \
--hoodie-conf hoodie.datasource.hive_sync.database=rdbms_analytics \
--hoodie-conf hoodie.datasource.hive_sync.enable=true \
--hoodie-conf hoodie.datasource.hive_sync.table=hammerdb_public_warehouse2 \
--hoodie-conf hoodie.datasource.write.hive_style_partitioning=true \
--hoodie-conf hoodie.deltastreamer.source.dfs.root=s3://da-black-belt-2021-datalakestack-bronzelakebucket-19216ilyowszc/rdbms_analytics/cdc/hammerdb/public/warehouse/ \
--hoodie-conf hoodie.datasource.hive_sync.partition_extractor_class=org.apache.hudi.hive.NonPartitionedExtractor \
--hoodie-conf hoodie.datasource.write.keygenerator.class=org.apache.hudi.keygen.NonpartitionedKeyGenerator

s3://da-black-belt-2021-datalakestack-bronzelakebucket-19216ilyowszc/rdbms_analytics/cdc/hammerdb/public/warehouse/20220125/20220125-000620654.parquet

--hoodie-conf hoodie.datasource.write.keygenerator.class=org.apache.hudi.keygen.SimpleKeyGenerator \



--hoodie-conf hoodie.datasource.write.partitionpath.field=""
--checkpoint 0


--payload-class org.apache.hudi.payload.AWSDmsAvroPayload \

--hoodie-conf hoodie.datasource.writer.operation=upsert
--hoodie-conf hoodie.datasource.write.keygenerator.class=org.apache.hudi.keygen.SimpleKeyGenerator
--hoodie-conf hoodie.datasource.write.partitionpath.field=



 |-- Op: string (nullable = true)
 |-- w_id: integer (nullable = true)
 |-- w_name: string (nullable = true)
 |-- w_street_1: string (nullable = true)
 |-- w_street_2: string (nullable = true)
 |-- w_city: string (nullable = true)
 |-- w_state: string (nullable = true)
 |-- w_zip: string (nullable = true)
 |-- w_tax: decimal(4,4) (nullable = true)
 |-- w_ytd: decimal(12,2) (nullable = true)
 |-- trx_seq: string (nullable = true)
 |-- _hoodie_is_deleted: boolean (nullable = true)


root
 |-- _hoodie_commit_time: string (nullable = true)
 |-- _hoodie_commit_seqno: string (nullable = true)
 |-- _hoodie_record_key: string (nullable = true)
 |-- _hoodie_partition_path: string (nullable = true)
 |-- _hoodie_file_name: string (nullable = true)
 |-- w_id: integer (nullable = true)
 |-- w_name: string (nullable = true)
 |-- w_street_1: string (nullable = true)
 |-- w_street_2: string (nullable = true)
 |-- w_city: string (nullable = true)
 |-- w_state: string (nullable = true)
 |-- w_zip: string (nullable = true)
 |-- w_tax: decimal(4,4) (nullable = true)
 |-- w_ytd: decimal(12,2) (nullable = true)
 |-- Op: string (nullable = false)
 |-- _hoodie_is_deleted: boolean (nullable = false)
 |-- trx_seq: string (nullable = false)





root
 |-- Op: string (nullable = true)
 |-- w_id: integer (nullable = true)
 |-- w_name: string (nullable = true)
 |-- w_street_1: string (nullable = true)
 |-- w_street_2: string (nullable = true)
 |-- w_city: string (nullable = true)
 |-- w_state: string (nullable = true)
 |-- w_zip: string (nullable = true)
 |-- w_tax: decimal(4,4) (nullable = true)
 |-- w_ytd: decimal(12,2) (nullable = true)
 |-- trx_seq: string (nullable = true)
 |-- _hoodie_is_deleted: boolean (nullable = true)

|-- _hoodie_commit_time: string (nullable = true)
 |-- _hoodie_commit_seqno: string (nullable = true)
 |-- _hoodie_record_key: string (nullable = true)
 |-- _hoodie_partition_path: string (nullable = true)
 |-- _hoodie_file_name: string (nullable = true)
 |-- Op: string (nullable = false)
 |-- w_id: integer (nullable = true)
 |-- w_name: string (nullable = true)
 |-- w_street_1: string (nullable = true)
 |-- w_street_2: string (nullable = true)
 |-- w_city: string (nullable = true)
 |-- w_state: string (nullable = true)
 |-- w_zip: string (nullable = true)
 |-- w_tax: decimal(4,4) (nullable = true)
 |-- w_ytd: decimal(12,2) (nullable = true)
 |-- trx_seq: string (nullable = false)
 |-- _hoodie_is_deleted: boolean (nullable = false)


 --------------------------------

|-- Op: string (nullable = true)
 |-- w_id: integer (nullable = true)
 |-- w_name: string (nullable = true)
 |-- w_street_1: string (nullable = true)
 |-- w_street_2: string (nullable = true)
 |-- w_city: string (nullable = true)
 |-- w_state: string (nullable = true)
 |-- w_zip: string (nullable = true)
 |-- w_tax: decimal(4,4) (nullable = true)
 |-- w_ytd: decimal(12,2) (nullable = true)
 |-- trx_seq: string (nullable = true)
 |-- _hoodie_is_deleted: boolean (nullable = true)


 |-- _hoodie_commit_time: string (nullable = true)
 |-- _hoodie_commit_seqno: string (nullable = true)
 |-- _hoodie_record_key: string (nullable = true)
 |-- _hoodie_partition_path: string (nullable = true)
 |-- _hoodie_file_name: string (nullable = true)
 |-- Op: string (nullable = true)
 |-- w_id: integer (nullable = true)
 |-- w_name: string (nullable = true)
 |-- w_street_1: string (nullable = true)
 |-- w_street_2: string (nullable = true)
 |-- w_city: string (nullable = true)
 |-- w_state: string (nullable = true)
 |-- w_zip: string (nullable = true)
 |-- w_tax: decimal(4,4) (nullable = true)
 |-- w_ytd: decimal(12,2) (nullable = true)
 |-- trx_seq: string (nullable = true)
 |-- _hoodie_is_deleted: boolean (nullable = true)

