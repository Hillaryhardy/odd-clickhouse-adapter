from typing import List

import pytz
from odd_contract.models import DataEntity, DataSet, DataTransformer, DataEntityType
from oddrn_generator import ClickHouseGenerator

from . import MetadataNamedtuple, ColumnMetadataNamedtuple, _data_set_metadata_schema_url, \
    _data_set_metadata_excluded_keys
from .columns import map_column
from .metadata import _append_metadata_extension


def map_table(oddrn_generator: ClickHouseGenerator, tables: List[tuple], columns: List[tuple]) -> List[DataEntity]:
    data_entities: List[DataEntity] = []
    column_index: int = 0

    for table in tables:
        mtable: MetadataNamedtuple = MetadataNamedtuple(*table)
        table_name: str = mtable.name

        # DataEntity
        data_entity: DataEntity = DataEntity(
            oddrn=oddrn_generator.get_oddrn_by_path('tables', table_name),
            name=table_name,
            owner=None,
            description=None,
            metadata=[],
            type=DataEntityType.VIEW if mtable.engine == "View" else DataEntityType.TABLE,
        )
        data_entities.append(data_entity)

        _append_metadata_extension(data_entity.metadata, _data_set_metadata_schema_url, mtable,
                                   _data_set_metadata_excluded_keys)

        if "metadata_modification_time" in mtable and mtable.metadata_modification_time is not None:
            data_entity.updated_at = mtable.metadata_modification_time.replace(tzinfo=pytz.utc).isoformat()

        # Dataset
        data_entity.dataset = DataSet(
            parent_oddrn=oddrn_generator.get_oddrn_by_path('databases'),
            rows_number=int(mtable.total_rows) if mtable.total_rows is not None else None,
            field_list=[]
        )

        # DataTransformer
        if data_entity.type == 'VIEW':  # data_entity.dataset.subtype == 'DATASET_VIEW'
            data_entity.data_transformer = DataTransformer(
                inputs=[],
                outputs=[],
                sql=mtable.create_table_query,
            )

        # DatasetField
        while column_index < len(columns):
            column: tuple = columns[column_index]
            mcolumn: ColumnMetadataNamedtuple = ColumnMetadataNamedtuple(*column)

            if mcolumn.table == table_name:
                data_entity.dataset.field_list.append(map_column(mcolumn, oddrn_generator, data_entity.owner))
                column_index += 1
            else:
                break

    return data_entities
