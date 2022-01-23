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
--hoodie-conf hoodie.datasource.write.recordkey.field=w_id
--hoodie-conf hoodie.table.name=hammerdb_public_warehouse
--hoodie-conf hoodie.datasource.write.precombine.field=trx_seq
--hoodie-conf hoodie.datasource.hive_sync.database=rdbms_analytics
--hoodie-conf hoodie.datasource.hive_sync.enable=true
--hoodie-conf hoodie.datasource.hive_sync.table=hammerdb_public_warehouse
--hoodie-conf hoodie.datasource.write.hive_style_partitioning=true
--hoodie-conf hoodie.deltastreamer.source.dfs.root=s3://da-black-belt-2021-datalakestack-bronzelakebucket-19216ilyowszc/rdbms_analytics/cdc/hammerdb/public/warehouse/
--hoodie-conf hoodie.datasource.hive_sync.partition_extractor_class=org.apache.hudi.hive.NonPartitionedExtractor
--hoodie-conf hoodie.datasource.writer.operation=upsert
--hoodie-conf hoodie.datasource.write.keygenerator.class=org.apache.hudi.keygen.ComplexKeyGenerator