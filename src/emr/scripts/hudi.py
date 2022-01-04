import logging


def get_hudi_options(table_name, database_name, table_config, operation):
    primary_key = table_config['primary_key']
    precombine_field = table_config['watermark']
    glue_database = database_name

    hudi_options = {
        'hoodie.table.name': table_name,
        'hoodie.datasource.write.recordkey.field': primary_key,
        'hoodie.datasource.write.precombine.field': precombine_field,
        'hoodie.datasource.hive_sync.database': glue_database,
        'hoodie.datasource.hive_sync.enable': 'true',
        'hoodie.datasource.hive_sync.table': table_name
    }
    if operation == 'FULL':
        hudi_options['hoodie.datasource.write.operation'] = 'bulk_insert'
        # TODO: Figure out sorting options, in testing, sorting took a very very long time
        hudi_options['hoodie.bulkinsert.sort.mode'] = 'NONE'
    else:
        raise ValueError(f'Operation {operation} not yet supported.')

    if table_config['is_partitioned'] is False:
        extractor = 'org.apache.hudi.hive.NonPartitionedExtractor'
        hudi_options['hoodie.datasource.hive_sync.partition_extractor_class'] = extractor
    else:
        partition_path = table_config['partition_path']
        hudi_options['hoodie.datasource.write.partitionpath.field'] = partition_path

    #  Not required with latest Hudi libraries, should be inferred based on recordkey.field
    # 'hoodie.datasource.write.keygenerator.class': 'org.apache.hudi.keygen.ComplexKeyGenerator',
    logging.debug(hudi_options)

    return hudi_options
