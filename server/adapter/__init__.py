from collections import namedtuple

_METADATA_SCHEMA_URL_PREFIX: str = \
    'https://raw.githubusercontent.com/opendatadiscovery/opendatadiscovery-specification/main/specification/' \
    'extensions/postgresql.json#/definitions/Postgresql'

_data_set_metadata_schema_url: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetExtension'
_data_set_field_metadata_schema_url: str = _METADATA_SCHEMA_URL_PREFIX + 'DataSetFieldExtension'

_data_set_metadata_excluded_keys: set = {'name', "database"}

_table_metadata: str = \
    'name, database, engine, uuid, total_rows, ' \
    'total_bytes, metadata_path, data_paths, is_temporary, ' \
    'create_table_query, metadata_modification_time'

_table_select = '''
select t.name,
    t.database,
    t.engine,
    t.uuid,
    t.total_rows,
    t.total_bytes,
    t.metadata_path,
    t.data_paths,
    t.is_temporary,
    t.create_table_query,
    t.metadata_modification_time
from system.tables t
where t.database = %(database)s
'''

_data_set_field_metadata_excluded_keys: set = \
    {'database', 'table', 'name', 'type',
     'default_kind', 'default_expression'}

_column_metadata: str = \
    'database, table, name, type, position, default_kind, default_expression, ' \
    'data_compressed_bytes, data_uncompressed_bytes, marks_bytes, ' \
    'comment, is_in_partition_key, is_in_sorting_key, ' \
    'is_in_primary_key, is_in_sampling_key, compression_codec'

_column_select: str = '''
select 
    c.database, 
    c.table, 
    c.name, 
    c.type, 
    c.position, 
    c.default_kind, 
    c.default_expression, 
    c.data_compressed_bytes, 
    c.data_uncompressed_bytes,
    c.marks_bytes,
    c.comment,
    c.is_in_partition_key,
    c.is_in_sorting_key,
    c.is_in_primary_key,
    c.is_in_sampling_key,
    c.compression_codec
from system.columns c
where c.database = %(database)s
'''

MetadataNamedtuple = namedtuple('MetadataNamedtuple', _table_metadata)
ColumnMetadataNamedtuple = namedtuple('ColumnMetadataNamedtuple', _column_metadata)
