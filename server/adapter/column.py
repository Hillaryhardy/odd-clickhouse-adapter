from odd_contract.models import DataSetField, DataSetFieldType
from adapter import ColumnMetadataNamedtuple, \
    _data_set_field_metadata_schema_url, _data_set_field_metadata_excluded_keys
from adapter.type import TYPES_SQL_TO_ODD
from adapter.metadata import _append_metadata_extension

from typing import List
from app.oddrn import generate_column_oddrn, generate_table_oddrn

def _map_column(mcolumn: ColumnMetadataNamedtuple, owner: str, is_key: bool = None, is_value: bool = None) -> List[DataSetField]:
    result: List[DataSetField] = []

    database_name: str = mcolumn.database
    table_name: str = mcolumn.table
    column_name: str = mcolumn.name

    dsf: DataSetField = DataSetField()

    dsf.oddrn = generate_column_oddrn(database_name, table_name, column_name)
    dsf.name = column_name
    dsf.owner = owner

    dsf.metadata = []
    _append_metadata_extension(dsf.metadata, _data_set_field_metadata_schema_url, mcolumn,
                               _data_set_field_metadata_excluded_keys)

    dsf.parent_field_oddrn = generate_table_oddrn(database_name, table_name)

    dsf.type = DataSetFieldType()
    data_type: str = mcolumn.type
    dsf.type.type = TYPES_SQL_TO_ODD[data_type] if data_type in TYPES_SQL_TO_ODD else 'TYPE_UNKNOWN'
    dsf.type.logical_type = mcolumn.type
    #dsf.type.is_nullable = True if mcolumn.is_nullable == 'YES' else False

    dsf.is_key = bool(is_key)
    dsf.is_value = bool(is_value)
    dsf.default_value = mcolumn.default_kind
    dsf.description = ""

    result.append(dsf)
    return result
