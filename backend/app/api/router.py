"""
API路由
"""
from fastapi import APIRouter, HTTPException
from app.api.schemas import ConvertRequest, ConvertResponse, TableInfo as SchemaTableInfo
from app.services.ddl_converter import DDLConverter
from app.services.datax_generator import DataXGenerator
from app.services.seatunnel_generator import SeaTunnelGenerator
from app.core.logger import logger

api_router = APIRouter()


@api_router.post("/convert", response_model=ConvertResponse)
async def convert_ddl(request: ConvertRequest) -> ConvertResponse:
    """
    DDL转换接口

    - **source_db_type**: 源数据库类型 (mysql, postgresql, oracle, sqlserver)
    - **ddl**: 源数据库DDL语句
    - **target_db_type**: 目标数据库类型 (默认doris)
    - **sync_tool**: 同步工具类型 (datax, seatunnel)
    """
    try:
        logger.info(f"收到转换请求: {request.source_db_type} -> {request.target_db_type}, 工具: {request.sync_tool}")

        # 1. 转换DDL
        converter = DDLConverter(request.source_db_type, request.target_db_type)
        result = converter.convert(request.ddl)

        if not result.success:
            return ConvertResponse(
                success=False,
                message="DDL转换失败",
                errors=result.errors
            )

        # 2. 生成同步配置
        if request.sync_tool == "datax":
            generator = DataXGenerator()
        else:
            generator = SeaTunnelGenerator()

        sync_config = generator.generate(
            source_db_type=request.source_db_type,
            target_db_type=request.target_db_type,
            table_info=result.table_info
        )

        # 将ddl_converter中的TableInfo转换为schemas中的TableInfo
        # 需要将dataclass转换为字典
        columns_list = [
            {
                "name": col.name,
                "source_type": col.source_type,
                "target_type": col.target_type,
                "comment": col.comment,
                "is_primary": col.is_primary
            }
            for col in result.table_info.columns
        ]

        schema_table_info = SchemaTableInfo(
            table_name=result.table_info.name,
            columns=columns_list,
            comment=result.table_info.comment
        )

        return ConvertResponse(
            success=True,
            message="转换成功",
            converted_ddl=result.converted_ddl,
            sync_config=sync_config,
            table_info=schema_table_info,
            errors=[]
        )

    except Exception as e:
        logger.error(f"转换失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"转换失败: {str(e)}")


@api_router.get("/supported-db")
async def get_supported_databases():
    """
    获取支持的数据库类型列表
    """
    return {
        "source_databases": [
            {"value": "mysql", "label": "MySQL"},
            {"value": "postgresql", "label": "PostgreSQL"},
            {"value": "oracle", "label": "Oracle"},
            {"value": "sqlserver", "label": "SQL Server"}
        ],
        "target_databases": [
            {"value": "doris", "label": "Apache Doris"},
            {"value": "clickhouse", "label": "ClickHouse"},
            {"value": "greenplum", "label": "Greenplum"}
        ],
        "sync_tools": [
            {"value": "datax", "label": "DataX"},
            {"value": "seatunnel", "label": "SeaTunnel"}
        ]
    }
