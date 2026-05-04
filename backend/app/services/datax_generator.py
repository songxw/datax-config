"""
DataX配置文件生成器
"""
import json
from typing import Dict, Any
from app.core.logger import logger


class DataXGenerator:
    """DataX配置生成器"""

    # Reader插件映射
    READER_MAPPING = {
        "mysql": "mysqlreader",
        "postgresql": "postgresqlreader",
        "oracle": "oraclereader",
        "sqlserver": "sqlserverreader"
    }

    # 默认端口映射
    PORT_MAPPING = {
        "mysql": 3306,
        "postgresql": 5432,
        "oracle": 1521,
        "sqlserver": 1433
    }

    # JDBC URL数据库类型映射
    JDBC_TYPE_MAPPING = {
        "mysql": "mysql",
        "postgresql": "postgres", 
        "oracle": "oracle",
        "sqlserver": "sqlserver"
    }

    def generate(self, source_db_type: str, target_db_type: str,
                 table_info: Any) -> str:
        """
        生成DataX配置

        Args:
            source_db_type: 源数据库类型
            target_db_type: 目标数据库类型
            table_info: 表信息

        Returns:
            str: DataX配置JSON字符串
        """
        try:
            target_db_type = target_db_type.lower()
            reader_name = self.READER_MAPPING.get(source_db_type.lower(), "mysqlreader")
            source_port = self.PORT_MAPPING.get(source_db_type.lower(), 3306)
            jdbc_type = self.JDBC_TYPE_MAPPING.get(source_db_type.lower(), "mysql")

            # 构建列列表 - 纯字符串，不使用引号包裹
            column_list = [col.name for col in table_info.columns]

            writer_name = "doriswriter"
            writer_parameter = {
                "username": f"{target_db_type}_username",
                "password": f"{target_db_type}_password",
                "column": column_list,
                "preSql": [],  # 可添加预执行SQL
            }

            if target_db_type == "doris":
                writer_name = "doriswriter"
                writer_parameter.update({
                    "connection": [
                        {
                            "jdbcUrl": "jdbc:mysql://doris_fe_host:9030/target_database",
                            "table": [f"{table_info.name}"]
                        }
                    ],
                    "loadProps": {
                        "format": "json",
                        "strip_outer_array": True
                    },
                    "writeMode": "insert",
                    "batchSize": 1024,
                    "maxRetries": 3,
                    "label": f"datax_{source_db_type}_{table_info.name}"
                })
            elif target_db_type == "clickhouse":
                writer_name = "clickhousewriter"
                writer_parameter.update({
                    "connection": [
                        {
                            "jdbcUrl": "jdbc:clickhouse://clickhouse_host:8123/target_database",
                            "table": [f"{table_info.name}"]
                        }
                    ],
                    "batchSize": 2048,
                    "writeMode": "insert"
                })
            elif target_db_type == "greenplum":
                writer_name = "postgresqlwriter"
                writer_parameter.update({
                    "connection": [
                        {
                            "jdbcUrl": "jdbc:postgresql://greenplum_host:5432/target_database",
                            "table": [f"{table_info.name}"]
                        }
                    ],
                    "writeMode": "insert"
                })

            # 构建配置 - 参考标准DataX格式
            config = {
                "job": {
                    "setting": {
                        "speed": {
                            "channel": 3  # 默认3个通道，可根据需要调整
                        }
                    },
                    "content": [
                        {
                            "reader": {
                                "name": reader_name,
                                "parameter": {
                                    "username": "source_username",
                                    "password": "source_password",
                                    "column": column_list,
                                    "where": "",  # 可添加where条件
                                    "splitPk": "",  # 可添加分片字段
                                    "connection": [
                                        {
                                            "table": [table_info.name],
                                            "jdbcUrl": [
                                                f"jdbc:{jdbc_type}://source_host:{source_port}/source_database"
                                            ]
                                        }
                                    ]
                                }
                            },
                            "writer": {
                                "name": writer_name,
                                "parameter": writer_parameter
                            }
                        }
                    ]
                }
            }

            # 美化JSON输出
            return json.dumps(config, indent=2, ensure_ascii=False)

        except Exception as e:
            logger.error(f"DataX配置生成失败: {str(e)}")
            raise

    def _build_doris_table_meta(self, table_info: Any) -> str:
        """构建Doris表元数据"""
        cols = []
        for col in table_info.columns:
            col_def = f'"{col.name}" {col.target_type}'
            if col.comment:
                col_def += f" COMMENT '{col.comment}'"
            cols.append(col_def)

        # 主键
        if table_info.primary_keys:
            pk = ", PRIMARY KEY (" + ", ".join([f'"{pk}"' for pk in table_info.primary_keys]) + ")"
        else:
            pk = ""

        return ",\n".join(cols) + pk + ")"

    def generate_with_params(self, source_db_type: str, target_db_type: str,
                             table_info: Any, params: Dict[str, Any]) -> str:
        """
        生成带具体参数的DataX配置
        """
        reader_name = self.READER_MAPPING.get(source_db_type.lower(), "mysqlreader")
        target_db_type = target_db_type.lower()
        jdbc_type = self.JDBC_TYPE_MAPPING.get(source_db_type.lower(), "mysql")

        # 构建列列表 - 纯字符串，不使用引号包裹
        column_list = [col.name for col in table_info.columns]

        # 获取源数据库参数
        source_host = params.get("source_host", "localhost")
        source_port = params.get("source_port", self.PORT_MAPPING.get(source_db_type.lower(), 3306))
        source_database = params.get("source_database", "database")
        source_username = params.get("source_username", "username")
        source_password = params.get("source_password", "password")

        # 获取目标数据库参数 (fallback to 'target' params)
        target_host = params.get(f"{target_db_type}_host", params.get("target_host", "localhost"))
        target_port = params.get(f"{target_db_type}_port", params.get("target_port", 9030 if target_db_type == "doris" else (8123 if target_db_type == "clickhouse" else 5432)))
        target_database = params.get(f"{target_db_type}_database", params.get("target_database", "database"))
        target_username = params.get(f"{target_db_type}_username", params.get("target_username", "root"))
        target_password = params.get(f"{target_db_type}_password", params.get("target_password", ""))

        writer_name = "doriswriter"
        writer_parameter = {
            "username": target_username,
            "password": target_password,
            "column": column_list,
        }

        if target_db_type == "doris":
            writer_name = "doriswriter"
            writer_parameter.update({
                "connection": [
                    {
                        "jdbcUrl": f"jdbc:mysql://{target_host}:{target_port}/{target_database}",
                        "table": [table_info.name]
                    }
                ],
                "loadProps": {
                    "format": "json",
                    "strip_outer_array": True
                },
                "writeMode": "insert",
                "batchSize": 1024,
                "maxRetries": 3,
                "label": f"datax_{source_db_type}_{table_info.name}"
            })
        elif target_db_type == "clickhouse":
            writer_name = "clickhousewriter"
            writer_parameter.update({
                "connection": [
                    {
                        "jdbcUrl": f"jdbc:clickhouse://{target_host}:{target_port}/{target_database}",
                        "table": [table_info.name]
                    }
                ],
                "batchSize": 2048,
                "writeMode": "insert"
            })
        elif target_db_type == "greenplum":
            writer_name = "postgresqlwriter"
            writer_parameter.update({
                "connection": [
                    {
                        "jdbcUrl": f"jdbc:postgresql://{target_host}:{target_port}/{target_database}",
                        "table": [table_info.name]
                    }
                ],
                "writeMode": "insert"
            })

        # 构建配置
        config = {
            "job": {
                "content": [
                    {
                        "reader": {
                            "name": reader_name,
                            "parameter": {
                                "username": source_username,
                                "password": source_password,
                                "column": column_list,
                                "connection": [
                                    {
                                        "table": [table_info.name],
                                        "jdbcUrl": [
                                            f"jdbc:{jdbc_type}://{source_host}:{source_port}/{source_database}"
                                        ]
                                    }
                                ]
                            }
                        },
                        "writer": {
                            "name": writer_name,
                            "parameter": writer_parameter
                        }
                    }
                ],
                "setting": {
                    "speed": {
                        "channel": 1,
                        "byte": 1048576
                    },
                    "errorLimit": {
                        "record": 0,
                        "percentage": 0.02
                    }
                }
            }
        }

        # 只有doris才添加tableMeta
        if target_db_type == "doris":
            table_meta = self._build_doris_table_meta(table_info)
            if "tableMeta" not in config["job"]["content"][0]["writer"]["parameter"]["connection"][0]:
                config["job"]["content"][0]["writer"]["parameter"]["connection"][0]["tableMeta"] = table_meta
            else:
                config["job"]["content"][0]["writer"]["parameter"]["connection"][0]["tableMeta"] += table_meta

        return json.dumps(config, indent=2, ensure_ascii=False)
