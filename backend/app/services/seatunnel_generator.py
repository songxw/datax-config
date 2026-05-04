"""
SeaTunnel配置文件生成器
"""
from typing import Dict, Any
from app.core.logger import logger


class SeaTunnelGenerator:
    """SeaTunnel配置生成器"""

    # JDBC驱动映射
    DRIVER_MAPPING = {
        "mysql": "com.mysql.cj.jdbc.Driver",
        "postgresql": "org.postgresql.Driver",
        "oracle": "oracle.jdbc.OracleDriver",
        "sqlserver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
    }

    # 默认端口映射
    PORT_MAPPING = {
        "mysql": 3306,
        "postgresql": 5432,
        "oracle": 1521,
        "sqlserver": 1433
    }

    # Doris FE端口映射 (HTTP端口)
    DORIS_PORT_MAPPING = {
        "http": 8030,
        "jdbc": 9030
    }

    def generate(self, source_db_type: str, target_db_type: str,
                 table_info: Any) -> str:
        """
        生成SeaTunnel配置

        Args:
            source_db_type: 源数据库类型
            target_db_type: 目标数据库类型
            table_info: 表信息

        Returns:
            str: SeaTunnel配置字符串 (HOCON格式)
        """
        try:
            target_db_type = target_db_type.lower()
            driver = self.DRIVER_MAPPING.get(source_db_type.lower(),
                                             self.DRIVER_MAPPING["mysql"])
            source_port = self.PORT_MAPPING.get(source_db_type.lower(), 3306)

            # 构建列列表 - 使用字面量反引号，不使用f-string中的${}语法
            columns = ["`" + col.name + "`" for col in table_info.columns]

            # 构建列字符串（不使用f-string的join）
            columns_str = ', '.join(columns)

            sink_block = ""
            if target_db_type == "doris":
                sink_block = f"""    Doris {{
      fenodes = "doris_fe_host:8030"
      username = "doris_username"
      password = "doris_password"
      database = "target_database"
      table = "{table_info.name}"
      batch_max_rows = 1024
      batch_max_bytes = 10485760
      batch_interval_ms = 1000

      sink.properties.format = "json"
      sink.properties.strip_outer_array = "true"

      doris.config {{
        format = "json"
        read_json_by_line = "true"
      }}
    }}"""
            elif target_db_type == "clickhouse":
                sink_block = f"""    Clickhouse {{
      host = "clickhouse_host:8123"
      database = "target_database"
      table = "{table_info.name}"
      username = "clickhouse_username"
      password = "clickhouse_password"
      bulk_size = 20000
    }}"""
            elif target_db_type == "greenplum":
                sink_block = f"""    Jdbc {{
      driver = "org.postgresql.Driver"
      url = "jdbc:postgresql://greenplum_host:5432/target_database"
      username = "greenplum_username"
      password = "greenplum_password"
      generate_sink_sql = true
      database = "target_database"
      table = "{table_info.name}"
    }}"""

            config = f"""{{
  env {{
    execution.parallelism = 1
    job.mode = "BATCH"
  }}

  source {{
    Jdbc {{
      driver = "{driver}"
      url = "jdbc:{source_db_type}://source_host:{source_port}/source_database"
      username = "source_username"
      password = "source_password"
      table = "source_database.{table_info.name}"
      query = "SELECT {columns_str} FROM {table_info.name}"
    }}
  }}

  transform {{
    Sql {{
      source_table_name = "source_table"
      result_table_name = "result_table"
      query = "SELECT {columns_str} FROM source_table"
    }}
  }}

  sink {{
{sink_block}
  }}
}}
"""
            return config

        except Exception as e:
            logger.error(f"SeaTunnel配置生成失败: {str(e)}")
            raise

    def generate_with_params(self, source_db_type: str, target_db_type: str,
                            table_info: Any, params: Dict[str, Any]) -> str:
        """
        生成带具体参数的SeaTunnel配置
        """
        target_db_type = target_db_type.lower()
        driver = self.DRIVER_MAPPING.get(source_db_type.lower(),
                                         self.DRIVER_MAPPING["mysql"])

        # 获取参数
        source_host = params.get("source_host", "localhost")
        source_port = params.get("source_port", self.PORT_MAPPING.get(source_db_type.lower(), 3306))
        source_database = params.get("source_database", "database")
        source_username = params.get("source_username", "username")
        source_password = params.get("source_password", "password")

        target_host = params.get(f"{target_db_type}_host", params.get("target_host", "localhost"))
        target_port = params.get(f"{target_db_type}_port", params.get("target_port", 8030 if target_db_type == "doris" else (8123 if target_db_type == "clickhouse" else 5432)))
        target_database = params.get(f"{target_db_type}_database", params.get("target_database", "database"))
        target_username = params.get(f"{target_db_type}_username", params.get("target_username", "root"))
        target_password = params.get(f"{target_db_type}_password", params.get("target_password", ""))

        # 构建列列表 - 使用字面量反引号
        columns = ["`" + col.name + "`" for col in table_info.columns]

        # 构建列字符串
        columns_str = ', '.join(columns)

        sink_block = ""
        if target_db_type == "doris":
            sink_block = f"""    Doris {{
      fenodes = "{target_host}:{target_port}"
      username = "{target_username}"
      password = "{target_password}"
      database = "{target_database}"
      table = "{table_info.name}"
      batch_max_rows = 1024
      batch_max_bytes = 10485760
      batch_interval_ms = 1000

      sink.properties.format = "json"
      sink.properties.strip_outer_array = "true"

      doris.config {{
        format = "json"
        read_json_by_line = "true"
      }}
    }}"""
        elif target_db_type == "clickhouse":
            sink_block = f"""    Clickhouse {{
      host = "{target_host}:{target_port}"
      database = "{target_database}"
      table = "{table_info.name}"
      username = "{target_username}"
      password = "{target_password}"
      bulk_size = 20000
    }}"""
        elif target_db_type == "greenplum":
            sink_block = f"""    Jdbc {{
      driver = "org.postgresql.Driver"
      url = "jdbc:postgresql://{target_host}:{target_port}/{target_database}"
      username = "{target_username}"
      password = "{target_password}"
      generate_sink_sql = true
      database = "{target_database}"
      table = "{table_info.name}"
    }}"""

        config = f"""{{
  env {{
    execution.parallelism = 1
    job.mode = "BATCH"
  }}

  source {{
    Jdbc {{
      driver = "{driver}"
      url = "jdbc:{source_db_type}://{source_host}:{source_port}/{source_database}"
      username = "{source_username}"
      password = "{source_password}"
      table = "{source_database}.{table_info.name}"
      query = "SELECT {columns_str} FROM {table_info.name}"
    }}
  }}

  transform {{
    Sql {{
      source_table_name = "source_table"
      result_table_name = "result_table"
      query = "SELECT {columns_str} FROM source_table"
    }}
  }}

  sink {{
{sink_block}
  }}
}}
"""
        return config

    def generate_streaming_config(self, source_db_type: str, target_db_type: str,
                                  table_info: Any, params: Dict[str, Any]) -> str:
        """
        生成流式同步配置（基于Binlog/CDC）
        """
        target_db_type = target_db_type.lower()

        # 获取参数
        source_host = params.get("source_host", "localhost")
        source_port = params.get("source_port", self.PORT_MAPPING.get(source_db_type.lower(), 3306))
        source_database = params.get("source_database", "database")
        source_username = params.get("source_username", "username")
        source_password = params.get("source_password", "password")

        target_host = params.get(f"{target_db_type}_host", params.get("target_host", "localhost"))
        target_port = params.get(f"{target_db_type}_port", params.get("target_port", 8030 if target_db_type == "doris" else (8123 if target_db_type == "clickhouse" else 5432)))
        target_database = params.get(f"{target_db_type}_database", params.get("target_database", "database"))
        target_username = params.get(f"{target_db_type}_username", params.get("target_username", "root"))
        target_password = params.get(f"{target_db_type}_password", params.get("target_password", ""))

        # 构建列列表 - 使用字面量反引号
        columns = ["`" + col.name + "`" for col in table_info.columns]

        sink_block = ""
        if target_db_type == "doris":
            sink_block = f"""    Doris {{
      fenodes = "{target_host}:{target_port}"
      username = "{target_username}"
      password = "{target_password}"
      database = "{target_database}"
      table = "{table_info.name}"
      batch_max_rows = 1024
      batch_max_bytes = 10485760
      batch_interval_ms = 1000

      sink.properties.format = "json"
      sink.properties.strip_outer_array = "true"

      sink.properties.row.default_parser = "json"
      sink.properties.bulk_flush.max_bytes = 52428800
      sink.properties.bulk_flush.max_rows = 200000
      sink.properties.bulk_flush.max_ms = 60000
    }}"""
        elif target_db_type == "clickhouse":
            sink_block = f"""    Clickhouse {{
      host = "{target_host}:{target_port}"
      database = "{target_database}"
      table = "{table_info.name}"
      username = "{target_username}"
      password = "{target_password}"
      bulk_size = 20000
    }}"""
        elif target_db_type == "greenplum":
            sink_block = f"""    Jdbc {{
      driver = "org.postgresql.Driver"
      url = "jdbc:postgresql://{target_host}:{target_port}/{target_database}"
      username = "{target_username}"
      password = "{target_password}"
      generate_sink_sql = true
      database = "{target_database}"
      table = "{table_info.name}"
    }}"""

        # MySQL CDC配置
        if source_db_type.lower() == "mysql":
            cdc_config = f"""{{
  env {{
    execution.parallelism = 1
    job.mode = "STREAMING"
    checkpoint.interval = 3000
  }}

  source {{
    Mysql-CDC {{
      username = "{source_username}"
      password = "{source_password}"
      database-name = "{source_database}"
      table-names = ["{source_database}.{table_info.name}"]
      base-url = "jdbc:mysql://{source_host}:{source_port}"
      server-time-zone = "UTC"
      startup.mode = "initial"
      server-id = 5400-5404
    }}
  }}

  sink {{
{sink_block}
  }}
}}
"""
        else:
            # 其他数据库使用流式JDBC
            cdc_config = self.generate_with_params(
                source_db_type, target_db_type, table_info, params
            ).replace('job.mode = "BATCH"', 'job.mode = "STREAMING"')

        return cdc_config
