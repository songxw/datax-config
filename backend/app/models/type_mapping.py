"""
数据库类型映射规则
"""
from typing import Dict
from dataclasses import dataclass


@dataclass
class TypeMapping:
    """类型映射"""
    target_type: str
    need_length: bool = False  # 是否需要长度参数


# MySQL -> Doris 类型映射
MYSQL_TO_DORIS: Dict[str, TypeMapping] = {
    # 整数类型
    "tinyint": TypeMapping("TINYINT"),
    "smallint": TypeMapping("SMALLINT"),
    "int": TypeMapping("INT"),
    "integer": TypeMapping("INT"),
    "bigint": TypeMapping("BIGINT"),

    # 浮点类型
    "float": TypeMapping("FLOAT"),
    "double": TypeMapping("DOUBLE"),
    "decimal": TypeMapping("DECIMAL", need_length=True),
    "numeric": TypeMapping("DECIMAL", need_length=True),

    # 字符串类型
    "char": TypeMapping("CHAR", need_length=True),
    "varchar": TypeMapping("VARCHAR", need_length=True),
    "text": TypeMapping("STRING"),
    "tinytext": TypeMapping("STRING"),
    "mediumtext": TypeMapping("STRING"),
    "longtext": TypeMapping("STRING"),

    # 日期时间类型
    "date": TypeMapping("DATE"),
    "datetime": TypeMapping("DATETIME"),
    "timestamp": TypeMapping("DATETIMEV2"),
    "time": TypeMapping("DATETIME"),

    # 布尔类型
    "bool": TypeMapping("BOOLEAN"),
    "boolean": TypeMapping("BOOLEAN"),

    # 二进制类型
    "binary": TypeMapping("STRING"),
    "varbinary": TypeMapping("STRING"),
    "blob": TypeMapping("STRING"),
    "tinyblob": TypeMapping("STRING"),
    "mediumblob": TypeMapping("STRING"),
    "longblob": TypeMapping("STRING"),
}

# PostgreSQL -> Doris 类型映射
POSTGRESQL_TO_DORIS: Dict[str, TypeMapping] = {
    # 整数类型
    "smallint": TypeMapping("SMALLINT"),
    "integer": TypeMapping("INT"),
    "int": TypeMapping("INT"),
    "bigint": TypeMapping("BIGINT"),
    "bigserial": TypeMapping("BIGINT"),

    # 浮点类型
    "real": TypeMapping("FLOAT"),
    "double precision": TypeMapping("DOUBLE"),
    "numeric": TypeMapping("DECIMAL", need_length=True),
    "decimal": TypeMapping("DECIMAL", need_length=True),

    # 字符串类型
    "character": TypeMapping("CHAR", need_length=True),
    "char": TypeMapping("CHAR", need_length=True),
    "character varying": TypeMapping("VARCHAR", need_length=True),
    "varchar": TypeMapping("VARCHAR", need_length=True),
    "text": TypeMapping("STRING"),

    # 日期时间类型
    "date": TypeMapping("DATE"),
    "time": TypeMapping("DATETIME"),
    "time without time zone": TypeMapping("DATETIME"),
    "timestamp": TypeMapping("DATETIMEV2"),
    "timestamp without time zone": TypeMapping("DATETIMEV2"),
    "timestamp with time zone": TypeMapping("DATETIMEV2"),
    "timestamptz": TypeMapping("DATETIMEV2"),

    # 布尔类型
    "boolean": TypeMapping("BOOLEAN"),
    "bool": TypeMapping("BOOLEAN"),

    # 二进制类型
    "bytea": TypeMapping("STRING"),

    # JSON类型
    "json": TypeMapping("STRING"),
    "jsonb": TypeMapping("STRING"),
}

# Oracle -> Doris 类型映射
ORACLE_TO_DORIS: Dict[str, TypeMapping] = {
    # 整数类型
    "number": TypeMapping("DECIMAL", need_length=True),

    # 浮点类型
    "float": TypeMapping("FLOAT"),
    "binary_float": TypeMapping("FLOAT"),
    "binary_double": TypeMapping("DOUBLE"),

    # 字符串类型
    "char": TypeMapping("CHAR", need_length=True),
    "nchar": TypeMapping("CHAR", need_length=True),
    "varchar2": TypeMapping("VARCHAR", need_length=True),
    "nvarchar2": TypeMapping("VARCHAR", need_length=True),
    "clob": TypeMapping("STRING"),
    "nclob": TypeMapping("STRING"),

    # 日期时间类型
    "date": TypeMapping("DATETIME"),
    "timestamp": TypeMapping("DATETIMEV2"),

    # 二进制类型
    "raw": TypeMapping("STRING"),
    "blob": TypeMapping("STRING"),
}

# SQL Server -> Doris 类型映射
SQLSERVER_TO_DORIS: Dict[str, TypeMapping] = {
    # 整数类型
    "tinyint": TypeMapping("TINYINT"),
    "smallint": TypeMapping("SMALLINT"),
    "int": TypeMapping("INT"),
    "bigint": TypeMapping("BIGINT"),

    # 浮点类型
    "real": TypeMapping("FLOAT"),
    "float": TypeMapping("DOUBLE"),
    "decimal": TypeMapping("DECIMAL", need_length=True),
    "numeric": TypeMapping("DECIMAL", need_length=True),
    "money": TypeMapping("DECIMAL", need_length=True),
    "smallmoney": TypeMapping("DECIMAL", need_length=True),

    # 字符串类型
    "char": TypeMapping("CHAR", need_length=True),
    "nchar": TypeMapping("CHAR", need_length=True),
    "varchar": TypeMapping("VARCHAR", need_length=True),
    "nvarchar": TypeMapping("VARCHAR", need_length=True),
    "text": TypeMapping("STRING"),
    "ntext": TypeMapping("STRING"),

    # 日期时间类型
    "date": TypeMapping("DATE"),
    "time": TypeMapping("DATETIME"),
    "datetime": TypeMapping("DATETIME"),
    "datetime2": TypeMapping("DATETIMEV2"),
    "smalldatetime": TypeMapping("DATETIME"),
    "datetimeoffset": TypeMapping("DATETIMEV2"),

    # 二进制类型
    "binary": TypeMapping("STRING"),
    "varbinary": TypeMapping("STRING"),
    "image": TypeMapping("STRING"),

    # 布尔类型
    "bit": TypeMapping("BOOLEAN"),
}


def get_type_mapping(source_db: str) -> Dict[str, TypeMapping]:
    """获取数据库类型映射"""
    mappings = {
        "mysql": MYSQL_TO_DORIS,
        "postgresql": POSTGRESQL_TO_DORIS,
        "oracle": ORACLE_TO_DORIS,
        "sqlserver": SQLSERVER_TO_DORIS,
    }
    return mappings.get(source_db.lower(), {})
