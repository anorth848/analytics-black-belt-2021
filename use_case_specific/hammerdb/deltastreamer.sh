#  Non-Partitioned deltastreamer example
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
