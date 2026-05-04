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


# --------------------- DORIS 映射 ---------------------
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
    "smallint": TypeMapping("SMALLINT"),
    "integer": TypeMapping("INT"),
    "int": TypeMapping("INT"),
    "bigint": TypeMapping("BIGINT"),
    "bigserial": TypeMapping("BIGINT"),
    "real": TypeMapping("FLOAT"),
    "double precision": TypeMapping("DOUBLE"),
    "numeric": TypeMapping("DECIMAL", need_length=True),
    "decimal": TypeMapping("DECIMAL", need_length=True),
    "character": TypeMapping("CHAR", need_length=True),
    "char": TypeMapping("CHAR", need_length=True),
    "character varying": TypeMapping("VARCHAR", need_length=True),
    "varchar": TypeMapping("VARCHAR", need_length=True),
    "text": TypeMapping("STRING"),
    "date": TypeMapping("DATE"),
    "time": TypeMapping("DATETIME"),
    "time without time zone": TypeMapping("DATETIME"),
    "timestamp": TypeMapping("DATETIMEV2"),
    "timestamp without time zone": TypeMapping("DATETIMEV2"),
    "timestamp with time zone": TypeMapping("DATETIMEV2"),
    "timestamptz": TypeMapping("DATETIMEV2"),
    "boolean": TypeMapping("BOOLEAN"),
    "bool": TypeMapping("BOOLEAN"),
    "bytea": TypeMapping("STRING"),
    "json": TypeMapping("STRING"),
    "jsonb": TypeMapping("STRING"),
}

# Oracle -> Doris 类型映射
ORACLE_TO_DORIS: Dict[str, TypeMapping] = {
    "number": TypeMapping("DECIMAL", need_length=True),
    "float": TypeMapping("FLOAT"),
    "binary_float": TypeMapping("FLOAT"),
    "binary_double": TypeMapping("DOUBLE"),
    "char": TypeMapping("CHAR", need_length=True),
    "nchar": TypeMapping("CHAR", need_length=True),
    "varchar2": TypeMapping("VARCHAR", need_length=True),
    "nvarchar2": TypeMapping("VARCHAR", need_length=True),
    "clob": TypeMapping("STRING"),
    "nclob": TypeMapping("STRING"),
    "date": TypeMapping("DATETIME"),
    "timestamp": TypeMapping("DATETIMEV2"),
    "raw": TypeMapping("STRING"),
    "blob": TypeMapping("STRING"),
}

# SQL Server -> Doris 类型映射
SQLSERVER_TO_DORIS: Dict[str, TypeMapping] = {
    "tinyint": TypeMapping("TINYINT"),
    "smallint": TypeMapping("SMALLINT"),
    "int": TypeMapping("INT"),
    "bigint": TypeMapping("BIGINT"),
    "real": TypeMapping("FLOAT"),
    "float": TypeMapping("DOUBLE"),
    "decimal": TypeMapping("DECIMAL", need_length=True),
    "numeric": TypeMapping("DECIMAL", need_length=True),
    "money": TypeMapping("DECIMAL", need_length=True),
    "smallmoney": TypeMapping("DECIMAL", need_length=True),
    "char": TypeMapping("CHAR", need_length=True),
    "nchar": TypeMapping("CHAR", need_length=True),
    "varchar": TypeMapping("VARCHAR", need_length=True),
    "nvarchar": TypeMapping("VARCHAR", need_length=True),
    "text": TypeMapping("STRING"),
    "ntext": TypeMapping("STRING"),
    "date": TypeMapping("DATE"),
    "time": TypeMapping("DATETIME"),
    "datetime": TypeMapping("DATETIME"),
    "datetime2": TypeMapping("DATETIMEV2"),
    "smalldatetime": TypeMapping("DATETIME"),
    "datetimeoffset": TypeMapping("DATETIMEV2"),
    "binary": TypeMapping("STRING"),
    "varbinary": TypeMapping("STRING"),
    "image": TypeMapping("STRING"),
    "bit": TypeMapping("BOOLEAN"),
}

# --------------------- CLICKHOUSE 映射 ---------------------
# MySQL -> ClickHouse
MYSQL_TO_CLICKHOUSE: Dict[str, TypeMapping] = {
    "tinyint": TypeMapping("Int8"),
    "smallint": TypeMapping("Int16"),
    "int": TypeMapping("Int32"),
    "integer": TypeMapping("Int32"),
    "bigint": TypeMapping("Int64"),
    "float": TypeMapping("Float32"),
    "double": TypeMapping("Float64"),
    "decimal": TypeMapping("Decimal", need_length=True),
    "numeric": TypeMapping("Decimal", need_length=True),
    "char": TypeMapping("String"),
    "varchar": TypeMapping("String"),
    "text": TypeMapping("String"),
    "tinytext": TypeMapping("String"),
    "mediumtext": TypeMapping("String"),
    "longtext": TypeMapping("String"),
    "date": TypeMapping("Date"),
    "datetime": TypeMapping("DateTime"),
    "timestamp": TypeMapping("DateTime"),
    "time": TypeMapping("String"),
    "bool": TypeMapping("UInt8"),
    "boolean": TypeMapping("UInt8"),
    "binary": TypeMapping("String"),
    "varbinary": TypeMapping("String"),
    "blob": TypeMapping("String"),
    "tinyblob": TypeMapping("String"),
    "mediumblob": TypeMapping("String"),
    "longblob": TypeMapping("String"),
}

# PostgreSQL -> ClickHouse
POSTGRESQL_TO_CLICKHOUSE: Dict[str, TypeMapping] = {
    "smallint": TypeMapping("Int16"),
    "integer": TypeMapping("Int32"),
    "int": TypeMapping("Int32"),
    "bigint": TypeMapping("Int64"),
    "bigserial": TypeMapping("Int64"),
    "real": TypeMapping("Float32"),
    "double precision": TypeMapping("Float64"),
    "numeric": TypeMapping("Decimal", need_length=True),
    "decimal": TypeMapping("Decimal", need_length=True),
    "character": TypeMapping("String"),
    "char": TypeMapping("String"),
    "character varying": TypeMapping("String"),
    "varchar": TypeMapping("String"),
    "text": TypeMapping("String"),
    "date": TypeMapping("Date"),
    "time": TypeMapping("String"),
    "time without time zone": TypeMapping("String"),
    "timestamp": TypeMapping("DateTime"),
    "timestamp without time zone": TypeMapping("DateTime"),
    "timestamp with time zone": TypeMapping("DateTime"),
    "timestamptz": TypeMapping("DateTime"),
    "boolean": TypeMapping("UInt8"),
    "bool": TypeMapping("UInt8"),
    "bytea": TypeMapping("String"),
    "json": TypeMapping("String"),
    "jsonb": TypeMapping("String"),
}

# Oracle -> ClickHouse
ORACLE_TO_CLICKHOUSE: Dict[str, TypeMapping] = {
    "number": TypeMapping("Decimal", need_length=True),
    "float": TypeMapping("Float64"),
    "binary_float": TypeMapping("Float32"),
    "binary_double": TypeMapping("Float64"),
    "char": TypeMapping("String"),
    "nchar": TypeMapping("String"),
    "varchar2": TypeMapping("String"),
    "nvarchar2": TypeMapping("String"),
    "clob": TypeMapping("String"),
    "nclob": TypeMapping("String"),
    "date": TypeMapping("DateTime"),
    "timestamp": TypeMapping("DateTime"),
    "raw": TypeMapping("String"),
    "blob": TypeMapping("String"),
}

# SQL Server -> ClickHouse
SQLSERVER_TO_CLICKHOUSE: Dict[str, TypeMapping] = {
    "tinyint": TypeMapping("UInt8"),
    "smallint": TypeMapping("Int16"),
    "int": TypeMapping("Int32"),
    "bigint": TypeMapping("Int64"),
    "real": TypeMapping("Float32"),
    "float": TypeMapping("Float64"),
    "decimal": TypeMapping("Decimal", need_length=True),
    "numeric": TypeMapping("Decimal", need_length=True),
    "money": TypeMapping("Decimal", need_length=True),
    "smallmoney": TypeMapping("Decimal", need_length=True),
    "char": TypeMapping("String"),
    "nchar": TypeMapping("String"),
    "varchar": TypeMapping("String"),
    "nvarchar": TypeMapping("String"),
    "text": TypeMapping("String"),
    "ntext": TypeMapping("String"),
    "date": TypeMapping("Date"),
    "time": TypeMapping("String"),
    "datetime": TypeMapping("DateTime"),
    "datetime2": TypeMapping("DateTime"),
    "smalldatetime": TypeMapping("DateTime"),
    "datetimeoffset": TypeMapping("DateTime"),
    "binary": TypeMapping("String"),
    "varbinary": TypeMapping("String"),
    "image": TypeMapping("String"),
    "bit": TypeMapping("UInt8"),
}

# --------------------- GREENPLUM 映射 ---------------------
# MySQL -> Greenplum
MYSQL_TO_GREENPLUM: Dict[str, TypeMapping] = {
    "tinyint": TypeMapping("SMALLINT"),
    "smallint": TypeMapping("SMALLINT"),
    "int": TypeMapping("INTEGER"),
    "integer": TypeMapping("INTEGER"),
    "bigint": TypeMapping("BIGINT"),
    "float": TypeMapping("REAL"),
    "double": TypeMapping("DOUBLE PRECISION"),
    "decimal": TypeMapping("NUMERIC", need_length=True),
    "numeric": TypeMapping("NUMERIC", need_length=True),
    "char": TypeMapping("CHAR", need_length=True),
    "varchar": TypeMapping("VARCHAR", need_length=True),
    "text": TypeMapping("TEXT"),
    "tinytext": TypeMapping("TEXT"),
    "mediumtext": TypeMapping("TEXT"),
    "longtext": TypeMapping("TEXT"),
    "date": TypeMapping("DATE"),
    "datetime": TypeMapping("TIMESTAMP"),
    "timestamp": TypeMapping("TIMESTAMP"),
    "time": TypeMapping("TIME"),
    "bool": TypeMapping("BOOLEAN"),
    "boolean": TypeMapping("BOOLEAN"),
    "binary": TypeMapping("BYTEA"),
    "varbinary": TypeMapping("BYTEA"),
    "blob": TypeMapping("BYTEA"),
    "tinyblob": TypeMapping("BYTEA"),
    "mediumblob": TypeMapping("BYTEA"),
    "longblob": TypeMapping("BYTEA"),
}

# PostgreSQL -> Greenplum (基本上是 1:1)
POSTGRESQL_TO_GREENPLUM: Dict[str, TypeMapping] = {
    "smallint": TypeMapping("SMALLINT"),
    "integer": TypeMapping("INTEGER"),
    "int": TypeMapping("INTEGER"),
    "bigint": TypeMapping("BIGINT"),
    "bigserial": TypeMapping("BIGINT"),
    "real": TypeMapping("REAL"),
    "double precision": TypeMapping("DOUBLE PRECISION"),
    "numeric": TypeMapping("NUMERIC", need_length=True),
    "decimal": TypeMapping("DECIMAL", need_length=True),
    "character": TypeMapping("CHAR", need_length=True),
    "char": TypeMapping("CHAR", need_length=True),
    "character varying": TypeMapping("VARCHAR", need_length=True),
    "varchar": TypeMapping("VARCHAR", need_length=True),
    "text": TypeMapping("TEXT"),
    "date": TypeMapping("DATE"),
    "time": TypeMapping("TIME"),
    "time without time zone": TypeMapping("TIME"),
    "timestamp": TypeMapping("TIMESTAMP"),
    "timestamp without time zone": TypeMapping("TIMESTAMP"),
    "timestamp with time zone": TypeMapping("TIMESTAMP WITH TIME ZONE"),
    "timestamptz": TypeMapping("TIMESTAMP WITH TIME ZONE"),
    "boolean": TypeMapping("BOOLEAN"),
    "bool": TypeMapping("BOOLEAN"),
    "bytea": TypeMapping("BYTEA"),
    "json": TypeMapping("JSON"),
    "jsonb": TypeMapping("JSONB"),
}

# Oracle -> Greenplum
ORACLE_TO_GREENPLUM: Dict[str, TypeMapping] = {
    "number": TypeMapping("NUMERIC", need_length=True),
    "float": TypeMapping("DOUBLE PRECISION"),
    "binary_float": TypeMapping("REAL"),
    "binary_double": TypeMapping("DOUBLE PRECISION"),
    "char": TypeMapping("CHAR", need_length=True),
    "nchar": TypeMapping("CHAR", need_length=True),
    "varchar2": TypeMapping("VARCHAR", need_length=True),
    "nvarchar2": TypeMapping("VARCHAR", need_length=True),
    "clob": TypeMapping("TEXT"),
    "nclob": TypeMapping("TEXT"),
    "date": TypeMapping("TIMESTAMP"),
    "timestamp": TypeMapping("TIMESTAMP"),
    "raw": TypeMapping("BYTEA"),
    "blob": TypeMapping("BYTEA"),
}

# SQL Server -> Greenplum
SQLSERVER_TO_GREENPLUM: Dict[str, TypeMapping] = {
    "tinyint": TypeMapping("SMALLINT"),
    "smallint": TypeMapping("SMALLINT"),
    "int": TypeMapping("INTEGER"),
    "bigint": TypeMapping("BIGINT"),
    "real": TypeMapping("REAL"),
    "float": TypeMapping("DOUBLE PRECISION"),
    "decimal": TypeMapping("NUMERIC", need_length=True),
    "numeric": TypeMapping("NUMERIC", need_length=True),
    "money": TypeMapping("NUMERIC", need_length=True),
    "smallmoney": TypeMapping("NUMERIC", need_length=True),
    "char": TypeMapping("CHAR", need_length=True),
    "nchar": TypeMapping("CHAR", need_length=True),
    "varchar": TypeMapping("VARCHAR", need_length=True),
    "nvarchar": TypeMapping("VARCHAR", need_length=True),
    "text": TypeMapping("TEXT"),
    "ntext": TypeMapping("TEXT"),
    "date": TypeMapping("DATE"),
    "time": TypeMapping("TIME"),
    "datetime": TypeMapping("TIMESTAMP"),
    "datetime2": TypeMapping("TIMESTAMP"),
    "smalldatetime": TypeMapping("TIMESTAMP"),
    "datetimeoffset": TypeMapping("TIMESTAMP WITH TIME ZONE"),
    "binary": TypeMapping("BYTEA"),
    "varbinary": TypeMapping("BYTEA"),
    "image": TypeMapping("BYTEA"),
    "bit": TypeMapping("BOOLEAN"),
}

def get_type_mapping(source_db: str, target_db: str = "doris") -> Dict[str, TypeMapping]:
    """获取数据库类型映射"""
    source_db = source_db.lower()
    target_db = target_db.lower()

    mappings = {
        "doris": {
            "mysql": MYSQL_TO_DORIS,
            "postgresql": POSTGRESQL_TO_DORIS,
            "oracle": ORACLE_TO_DORIS,
            "sqlserver": SQLSERVER_TO_DORIS,
        },
        "clickhouse": {
            "mysql": MYSQL_TO_CLICKHOUSE,
            "postgresql": POSTGRESQL_TO_CLICKHOUSE,
            "oracle": ORACLE_TO_CLICKHOUSE,
            "sqlserver": SQLSERVER_TO_CLICKHOUSE,
        },
        "greenplum": {
            "mysql": MYSQL_TO_GREENPLUM,
            "postgresql": POSTGRESQL_TO_GREENPLUM,
            "oracle": ORACLE_TO_GREENPLUM,
            "sqlserver": SQLSERVER_TO_GREENPLUM,
        }
    }

    target_mappings = mappings.get(target_db, mappings["doris"])
    return target_mappings.get(source_db, {})
