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
            driver = self.DRIVER_MAPPING.get(source_db_type.lower(),
                                             self.DRIVER_MAPPING["mysql"])
            source_port = self.PORT_MAPPING.get(source_db_type.lower(), 3306)

            # 构建列列表 - 使用字面量反引号，不使用f-string中的${}语法
            columns = ["`" + col.name + "`" for col in table_info.columns]

            # 构建字段映射
            field_mapping = {"`" + col.name + "`": "`" + col.name + "`"
                            for col in table_info.columns}

            # 构建列字符串（不使用f-string的join）
            columns_str = ', '.join(columns)

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
    Doris {{
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
    }}
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
                - doris_port: Doris FE HTTP端口 (默认8030)
                - doris_database: 目标数据库
                - doris_username: Doris用户名
                - doris_password: Doris密码

        Returns:
            str: SeaTunnel配置字符串 (HOCON格式)
        """
        driver = self.DRIVER_MAPPING.get(source_db_type.lower(),
                                         self.DRIVER_MAPPING["mysql"])

        # 获取参数
        source_host = params.get("source_host", "localhost")
        source_port = params.get("source_port", self.PORT_MAPPING.get(source_db_type.lower(), 3306))
        source_database = params.get("source_database", "database")
        source_username = params.get("source_username", "username")
        source_password = params.get("source_password", "password")

        doris_host = params.get("doris_host", "localhost")
        doris_port = params.get("doris_port", 8030)
        doris_database = params.get("doris_database", "database")
        doris_username = params.get("doris_username", "root")
        doris_password = params.get("doris_password", "")

        # 构建列列表 - 使用字面量反引号
        columns = ["`" + col.name + "`" for col in table_info.columns]

        # 构建列字符串
        columns_str = ', '.join(columns)

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
    Doris {{
      fenodes = "{doris_host}:{doris_port}"
      username = "{doris_username}"
      password = "{doris_password}"
      database = "{doris_database}"
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
    }}
  }}
}}
"""
        return config

    def generate_streaming_config(self, source_db_type: str, target_db_type: str,
                                  table_info: Any, params: Dict[str, Any]) -> str:
        """
        生成流式同步配置（基于Binlog/CDC）

        Args:
            source_db_type: 源数据库类型
            target_db_type: 目标数据库类型
            table_info: 表信息
            params: 连接参数

        Returns:
            str: SeaTunnel流式配置字符串
        """
        # 获取参数
        source_host = params.get("source_host", "localhost")
        source_port = params.get("source_port", self.PORT_MAPPING.get(source_db_type.lower(), 3306))
        source_database = params.get("source_database", "database")
        source_username = params.get("source_username", "username")
        source_password = params.get("source_password", "password")

        doris_host = params.get("doris_host", "localhost")
        doris_port = params.get("doris_port", 8030)
        doris_database = params.get("doris_database", "database")
        doris_username = params.get("doris_username", "root")
        doris_password = params.get("doris_password", "")

        # 构建列列表 - 使用字面量反引号
        columns = ["`" + col.name + "`" for col in table_info.columns]

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
    Doris {{
      fenodes = "{doris_host}:{doris_port}"
      username = "{doris_username}"
      password = "{doris_password}"
      database = "{doris_database}"
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
    }}
  }}
}}
"""
        else:
            # 其他数据库使用流式JDBC
            cdc_config = self.generate_with_params(
                source_db_type, target_db_type, table_info, params
            ).replace('job.mode = "BATCH"', 'job.mode = "STREAMING"')

        return cdc_config
