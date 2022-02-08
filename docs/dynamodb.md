## Runtime Config table

The runtime config table contains items with configuration data related to:   
- Spark JDBC datasources and related configs
- EMR Pipelines and related configs
- Tables and related configs

### Partition Key/Sort Key

The PK/SK are:

```
identifier ( STRING, Partition key )
config  (STRING, Sort key)
```

- *identifier*: This attribute is meant to uniquely identify a group of config records related to a set of pipelines.   
  - ***This must match UseCase from the Parent stacks for the first configured pipeline***   
  - Additional pipelines can be arbitrarily named
- *config*: This attribute must be one of [database::config, pipeline::config::<pipeline type>, table::config::<table name>].

#### Item specifics

In order for the system to function, each `identifier` group of items must have at least 3 items.
Using `rdbms_analytics` as our identifier(UseCase), here is an example of the minimum number of items in DynamoDB if you just wanted to load the customer table:   

|identifier|config|
|----------|------|
|rdbms_analytics|database::config|
|rdbms_analytics|pipeline::config::full_load|
|rdbms_analytics|table::public.customer|

##### Item schema

Each config entry type has its own expected schema

##### database::config

Currently only one jdbc datasource can be configured per pipeline. To add more jdbc data sources, you would configure a new identifier and group of pipelines/tables.

```
{
    "config": "database::config",
    "identifier": "rdbms_analytics",
    "secret": "secrets/manager/secret/name",    // This is the path to the connection information in AWS Secrets Manager
    "target_db_name": "use_case",               // This is the target glue database name 
    "target_table_prefix": "hammberdb"          // This is the prefix all glue tables will be created with EG: public.customer becomes hammerdb_public_customer

}
```

#### pipeline::config::\<pipeline type>

The currently supported pipeline types are full_load, seed_hudi, incremental_hudi and continuous_hudi.    
pipeline::config items are meant to tell the pipeline how to launch the EMR cluster. (EG: Number of nodes, node type, parallelism, etc)

```
{
    "config": "pipeline::config::full_load",    // Pipeline type, must be one of [full_load|seed_hudi|incremental_hudi|continuous_hudi]
    "identifier": "<UseCase>",
    "emr_config": {                             // These configs get passed into the StepFunction and are used when creating the EMR cluster
                                                // At present, cluster instance options are limited, need to add Spot and Autoscaling support
        "release_label": "emr-6.5.0",
        "master": {
            "instance_type": "m5.xlarge"
        },
        "worker": {
            "count": "6",
            "instance_type": "r5.2xlarge"
        },
        "step_parallelism": 4                   // NOTE: Make sure your worker settings can handle the parallelism you choose
                                                //       This is especially important for continuous_load
    },
    "next_pipeline": {                          // When this pipeline completes, whether or not to launch the next pipeline
        "pipeline_type": "seed_hudi",           // Must be one of [ seed_hudi|incremental_hudi|continuous_hudi ]
        "enabled": true                         // set to false to disable launching the next pipeline
    }
}
```

#### table::\<table name>

These items indicate how the pipeline should handle processing each table.   
This include Spark JDBC Options, EMR Job Step options, and Hudi options.

```
{
    "config": "table::<table_name>",            // One item per table
    "identifier": "<UseCase>",
    "enabled": [true|false],                      // Enable or Disable the table 
    "hudi_config": {
        "primary_key": "<c,s,v>",               // Comma-separated list of primary key columns on the table       
        "watermark": "trx_seq",                 // The "tie-breaker" column, used as the precombine field for merging rows in Hudi
                                                // Currently only trx_seq (AR_H_CHANGE_SEQ from AWS DMS) is supported
                                                // https://aws.amazon.com/blogs/database/capture-key-source-table-headers-data-using-aws-dms-and-use-it-for-amazon-s3-data-lake-operations/
        "is_partitioned": [true|false],         // Whether or not to partition the Hudi table
        "partition_path": "<column>",           // Required only if is_partitioned is true, the column to partition on
        "partition_extractor_class": "<cls>"    // The Hive partition extractor class EG: org.apache.hudi.hive.MultiPartKeysValueExtractor
        "transformer_class": "<cls"             // [OPTIONAL] The DeltaStreamer partition class EG: org.apache.hudi.utilities.transform.SqlQueryBasedTransformer
        "transformer_sql": "<SQL STATEMENT AS s>// [OPTIONAL] The sql statement (must be set if transformer_class is SqlQueryBasedTransformer
    },
    "spark_jdbc_config": {                      // [OPTIONAL] this stanza is only used by full_load pipeline and is passed directly to spark jdbc. 
                                                // Any option found here can be set: https://spark.apache.org/docs/latest/sql-data-sources-jdbc.html
        "<option>": "<value>"
    },
    "spark_conf": {                             // [OPTIONAL] this stanza is used to pass spark configurations to the emr job step
                                                // Any option found here can be set:  https://spark.apache.org/docs/latest/configuration.html#available-properties
        "<pipeline_type>": {                    // <pipeline type> must be one of: [ full_load|seed_hudi|incremental_hudi|continuous_hudi ]
            "<option>": "<value"
        }
    }
}
```

Example record for public.order_line in rdbms_analytics grouping:    

```
{
    "config": "table::public.order_line",
    "identifier": "rdbms_analytics",
    "enabled": true,
    "hudi_config": {
        "primary_key": "ol_w_id,ol_d_id,ol_o_id,ol_number",
        "watermark": "trx_seq",
        "is_partitioned": true,
        "partition_path": "ol_w_id",
        "partition_extractor_class": "org.apache.hudi.hive.MultiPartKeysValueExtractor"
    },
    "spark_jdbc_config": {
        "dbtable": "public.order_line",
        "partitionColumn": "ol_w_id",
        "lowerBound": "0",
        "upperBound": "300",
        "numPartitions": "30"
    },
    "spark_conf": {
        "full_load": {
            "spark.executor.cores": "2",
            "spark.executor.memory": "8g",
            "spark.executor.heartbeatInterval": "120s",
            "spark.network.timeout": "1200s",
            "spark.dynamicAllocation.enabled": "false",
            "spark.executor.instances": "12"
        },
        "seed_hudi": {
            "spark.executor.cores": "2",
            "spark.executor.memory": "8g",
            "spark.executor.heartbeatInterval": "90s",
            "spark.network.timeout": "900s",
            "spark.dynamicAllocation.enabled": "false",
            "spark.executor.instances": "12"
        },
        "incremental_hudi": {
            "spark.executor.cores": "2",
            "spark.executor.memory": "6g",
            "spark.executor.heartbeatInterval": "30s",
            "spark.network.timeout": "600s",
            "spark.dynamicAllocation.minExecutors": "2",
            "spark.dynamicAllocation.maxExecutors": "12"
        },
        "continuous_hudi": {
            "spark.executor.cores": "1",
            "spark.executor.memory": "4g",
            "spark.executor.heartbeatInterval": "30s",
            "spark.network.timeout": "300s",
            "spark.dynamicAllocation.minExecutors": "2",
            "spark.dynamicAllocation.maxExecutors": "6"
        }
    }
}
```
