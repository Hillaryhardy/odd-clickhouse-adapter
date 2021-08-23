import re
from odd_contract.models import DataSetField, DataSetFieldType
from adapter import ColumnMetadataNamedtuple, \
    _data_set_field_metadata_schema_url, _data_set_field_metadata_excluded_keys
from adapter.type import TYPES_SQL_TO_ODD
from adapter.metadata import _append_metadata_extension

from typing import List
from app.oddrn import generate_column_oddrn, generate_table_oddrn

def _map_column(mcolumn: ColumnMetadataNamedtuple, owner: str, is_key: bool = False, is_value: bool = False) -> List[DataSetField]:
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

    dsf.type = DataSetFieldType()
    dsf.type.type, dsf.type.is_nullable = _get_column_type(mcolumn.type)
    dsf.type.logical_type = mcolumn.type
    dsf.is_key = is_key
    dsf.is_value = is_value
    dsf.default_value = mcolumn.default_kind
    dsf.description = ""

    result.append(dsf)
    return result

def _get_column_type(data_type: str):
    is_nullable = True if data_type.startswith("Nullable") else False

    # trim Nullable
    trimmed = re.search("Nullable\((.+?)\)", data_type)
    if trimmed:
        data_type = trimmed.group(1)

    # trim LowCardinality
    trimmed = re.search("LowCardinality\((.+?)\)", data_type)
    if trimmed:
        data_type = trimmed.group(1)

    if data_type.startswith("Array"):
        data_type = "Array"
    elif data_type.startswith("Enum8"):
        data_type = "Enum8"

    if data_type in TYPES_SQL_TO_ODD:
        d_type = TYPES_SQL_TO_ODD[data_type]
    else:
        d_type = 'TYPE_UNKNOWN'
    return d_type, is_nullable
