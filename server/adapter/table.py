from odd_contract.models import DataEntity, DataSet, DataTransformer
from adapter import MetadataNamedtuple, ColumnMetadataNamedtuple, \
    _data_set_metadata_schema_url, _data_set_metadata_excluded_keys
from adapter.column import _map_column
from adapter.metadata import _append_metadata_extension
from app.oddrn import generate_database_oddrn, generate_table_oddrn

import pytz

from typing import List


def _map_table(tables: List[tuple], columns: List[tuple]) -> List[DataEntity]:
    data_entities: List[DataEntity] = []
    column_index: int = 0

    for table in tables:
        mtable: MetadataNamedtuple = MetadataNamedtuple(*table)

        database_name: str = mtable.database
        table_name: str = mtable.name

        database_oddrn: str = generate_database_oddrn(database_name)
        table_oddrn: str = generate_table_oddrn(database_name, table_name)

        # DataEntity
        data_entity: DataEntity = DataEntity()
        data_entities.append(data_entity)

        data_entity.oddrn = table_oddrn
        data_entity.name = table_name
        data_entity.owner = None
        data_entity.description = None

        data_entity.metadata = []
        _append_metadata_extension(data_entity.metadata, _data_set_metadata_schema_url, mtable,
                                   _data_set_metadata_excluded_keys)

        if "metadata_modification_time" in mtable and mtable.metadata_modification_time is not None:
            data_entity.updated_at = mtable.metadata_modification_time.replace(tzinfo=pytz.utc).isoformat()

        # Dataset
        data_entity.dataset = DataSet()

        data_entity.dataset.parent_oddrn = database_oddrn

        if mtable.total_rows is not None:
            data_entity.dataset.rows_number = int(mtable.total_rows)

        if mtable.engine == "View":
            data_entity.type = "VIEW"
        else:
            data_entity.type = "TABLE"

        data_entity.dataset.field_list = []

        # DataTransformer
        if data_entity.type == 'VIEW':  # data_entity.dataset.subtype == 'DATASET_VIEW'
            data_entity.data_transformer = DataTransformer()

            # data_entity.data_transformer.source_code_url = None
            data_entity.data_transformer.sql = mtable.create_table_query

            data_entity.data_transformer.inputs = []
            data_entity.data_transformer.outputs = []

        # DatasetField
        while column_index < len(columns):
            column: tuple = columns[column_index]
            mcolumn: ColumnMetadataNamedtuple = ColumnMetadataNamedtuple(*column)

            if mcolumn.database == database_name and mcolumn.table == table_name:
                data_entity.dataset.field_list.extend(_map_column(mcolumn, data_entity.owner, data_entity.oddrn))
                column_index += 1
            else:
                break

    return data_entities
