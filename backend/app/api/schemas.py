"""
API数据模型定义
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class SourceDBType(str, Enum):
    """源数据库类型"""
    MYSQL = "mysql"
    POSTGRESQL = "postgresql"
    ORACLE = "oracle"
    SQLSERVER = "sqlserver"


class TargetDBType(str, Enum):
    """目标数据库类型"""
    DORIS = "doris"


class SyncToolType(str, Enum):
    """同步工具类型"""
    DATAX = "datax"
    SEATUNNEL = "seatunnel"


class ColumnInfo(BaseModel):
    """列信息"""
    name: str = Field(..., description="列名")
    source_type: str = Field(..., description="源数据库类型")
    target_type: str = Field(..., description="目标数据库类型")
    comment: Optional[str] = Field(None, description="列注释")
    is_primary: bool = Field(False, description="是否主键")


class TableInfo(BaseModel):
    """表信息"""
    table_name: str = Field(..., description="表名")
    columns: List[ColumnInfo] = Field(default_factory=list, description="列信息列表")
    comment: Optional[str] = Field(None, description="表注释")


class ConvertRequest(BaseModel):
    """转换请求"""
    source_db_type: SourceDBType = Field(..., description="源数据库类型")
    ddl: str = Field(..., description="源数据库DDL")
    target_db_type: TargetDBType = Field(default=TargetDBType.DORIS, description="目标数据库类型")
    sync_tool: SyncToolType = Field(..., description="同步工具类型")

    class Config:
        json_schema_extra = {
            "example": {
                "source_db_type": "mysql",
                "ddl": "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));",
                "target_db_type": "doris",
                "sync_tool": "datax"
            }
        }


class ConvertResponse(BaseModel):
    """转换响应"""
    success: bool = Field(..., description="是否成功")
    message: str = Field(..., description="消息")
    converted_ddl: Optional[str] = Field(None, description="转换后的DDL")
    sync_config: Optional[str] = Field(None, description="同步配置文件内容")
    table_info: Optional[TableInfo] = Field(None, description="表信息")
    errors: List[str] = Field(default_factory=list, description="错误信息列表")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "转换成功",
                "converted_ddl": "CREATE TABLE users (...)",
                "sync_config": "{...}",
                "table_info": {
                    "table_name": "users",
                    "columns": [...]
                },
                "errors": []
            }
        }
