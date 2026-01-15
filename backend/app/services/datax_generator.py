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
            reader_name = self.READER_MAPPING.get(source_db_type.lower(), "mysqlreader")
            source_port = self.PORT_MAPPING.get(source_db_type.lower(), 3306)
            jdbc_type = self.JDBC_TYPE_MAPPING.get(source_db_type.lower(), "mysql")

            # 构建列列表 - 纯字符串，不使用引号包裹
            column_list = [col.name for col in table_info.columns]

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
                                "name": "doriswriter",
                                "parameter": {
                                    "username": "doris_username",
                                    "password": "doris_password",
                                    "column": column_list,
                                    "preSql": [],  # 可添加预执行SQL
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
                                }
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

        Args:
            source_db_type: 源数据库类型
            target_db_type: 目标数据库类型
            table_info: 表信息
            params: 连接参数
                - source_host: 源数据库主机
                - source_port: 源数据库端口
                - source_database: 源数据库名
                - source_username: 源数据库用户名
                - source_password: 源数据库密码
                - doris_host: Doris FE主机
                - doris_port: Doris FE端口 (默认9030)
                - doris_database: 目标数据库
                - doris_username: Doris用户名
                - doris_password: Doris密码

        Returns:
            str: DataX配置JSON字符串
        """
        reader_name = self.READER_MAPPING.get(source_db_type.lower(), "mysqlreader")

        # 构建列列表 - 纯字符串，不使用引号包裹
        column_list = [col.name for col in table_info.columns]

        # 获取参数
        source_host = params.get("source_host", "localhost")
        source_port = params.get("source_port", self.PORT_MAPPING.get(source_db_type.lower(), 3306))
        source_database = params.get("source_database", "database")
        source_username = params.get("source_username", "username")
        source_password = params.get("source_password", "password")

        doris_host = params.get("doris_host", "localhost")
        doris_port = params.get("doris_port", 9030)
        doris_database = params.get("doris_database", "database")
        doris_username = params.get("doris_username", "root")
        doris_password = params.get("doris_password", "")

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
                                            f"jdbc:mysql://{source_host}:{source_port}/{source_database}"
                                        ]
                                    }
                                ]
                            }
                        },
                        "writer": {
                            "name": "doriswriter",
                            "parameter": {
                                "username": doris_username,
                                "password": doris_password,
                                "column": column_list,
                                "connection": [
                                    {
                                        "jdbcUrl": f"jdbc:mysql://{doris_host}:{doris_port}/{doris_database}",
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
                            }
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

        # 添加列定义到tableMeta
        table_meta = self._build_doris_table_meta(table_info)
        config["job"]["content"][0]["writer"]["parameter"]["connection"][0]["tableMeta"] += table_meta

        return json.dumps(config, indent=2, ensure_ascii=False)
