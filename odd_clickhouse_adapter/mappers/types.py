from odd_contract.models import Type, DataEntityType


TYPES_SQL_TO_ODD = {
    "Date": Type.TYPE_DATETIME,
    "DateTime": Type.TYPE_DATETIME,
    "DateTime64": Type.TYPE_DATETIME,

    "String": Type.TYPE_STRING,
    "UUID": Type.TYPE_STRING,
    "IPv6": Type.TYPE_STRING,

    "Enum8": Type.TYPE_INTEGER,

    "Float32": Type.TYPE_NUMBER,
    "Float64": Type.TYPE_NUMBER,

    "Int8": Type.TYPE_INTEGER,
    "Int16": Type.TYPE_INTEGER,
    "Int32": Type.TYPE_INTEGER,
    "Int64": Type.TYPE_INTEGER,

    "UInt8": Type.TYPE_INTEGER,
    "UInt16": Type.TYPE_INTEGER,
    "UInt32": Type.TYPE_INTEGER,
    "UInt64": Type.TYPE_INTEGER,

    "Array": Type.TYPE_LIST
}
