"""
SeaTunnel配置生成器单元测试
"""
import pytest
from app.services.seatunnel_generator import SeaTunnelGenerator
from app.services.ddl_converter import ColumnInfo, TableInfo


class TestTableInfo:
    """测试用的TableInfo工厂"""
    @staticmethod
    def create_simple_table():
        """创建简单的测试表信息"""
        return TableInfo(
            name="users",
            columns=[
                ColumnInfo(name="id", source_type="INT", target_type="INT", is_primary=True),
                ColumnInfo(name="name", source_type="VARCHAR(100)", target_type="VARCHAR(100)"),
                ColumnInfo(name="email", source_type="VARCHAR(200)", target_type="VARCHAR(200)")
            ],
            primary_keys=["id"]
        )

    @staticmethod
    def create_complex_table():
        """创建复杂的测试表信息"""
        return TableInfo(
            name="orders",
            columns=[
                ColumnInfo(name="id", source_type="BIGINT", target_type="BIGINT", is_primary=True),
                ColumnInfo(name="user_id", source_type="BIGINT", target_type="BIGINT"),
                ColumnInfo(name="order_no", source_type="VARCHAR(50)", target_type="VARCHAR(50)"),
                ColumnInfo(name="total_amount", source_type="DECIMAL(10,2)", target_type="DECIMAL(10,2)"),
                ColumnInfo(name="status", source_type="INT", target_type="INT"),
                ColumnInfo(name="created_at", source_type="DATETIME", target_type="DATETIME")
            ],
            primary_keys=["id"]
        )


class TestSeaTunnelGenerator:
    """SeaTunnel配置生成器测试类"""

    def test_generate_mysql_to_doris(self):
        """测试MySQL到Doris的配置生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证基本结构
        assert "env {" in config_str
        assert "source {" in config_str
        assert "transform {" in config_str
        assert "sink {" in config_str

        # 验证MySQL JDBC配置
        assert "Jdbc {" in config_str
        assert "com.mysql.cj.jdbc.Driver" in config_str
        assert "jdbc:mysql://" in config_str

        # 验证Doris配置
        assert "Doris {" in config_str
        assert "fenodes" in config_str

    def test_generate_postgresql_to_doris(self):
        """测试PostgreSQL到Doris的配置生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("postgresql", "doris", table_info)

        # 验证PostgreSQL JDBC驱动
        assert "org.postgresql.Driver" in config_str
        assert "jdbc:postgresql://" in config_str

    def test_generate_oracle_to_doris(self):
        """测试Oracle到Doris的配置生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("oracle", "doris", table_info)

        # 验证Oracle JDBC驱动
        assert "oracle.jdbc.OracleDriver" in config_str
        assert "jdbc:oracle:" in config_str

    def test_generate_sqlserver_to_doris(self):
        """测试SQL Server到Doris的配置生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("sqlserver", "doris", table_info)

        # 验证SQL Server JDBC驱动
        assert "com.microsoft.sqlserver.jdbc.SQLServerDriver" in config_str
        assert "jdbc:sqlserver:" in config_str

    def test_env_config(self):
        """测试环境配置"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证env配置
        assert "execution.parallelism = 1" in config_str
        assert "job.mode = \"BATCH\"" in config_str

    def test_source_columns(self):
        """测试源表列配置"""
        table_info = TestTableInfo.create_complex_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证列配置
        assert "`id`" in config_str
        assert "`user_id`" in config_str
        assert "`order_no`" in config_str
        assert "`total_amount`" in config_str
        assert "`status`" in config_str
        assert "`created_at`" in config_str

    def test_generate_with_params(self):
        """测试带参数的配置生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        params = {
            "source_host": "192.168.1.100",
            "source_port": 3306,
            "source_database": "mydb",
            "source_username": "root",
            "source_password": "password123",
            "doris_host": "192.168.1.200",
            "doris_port": 8030,
            "doris_database": "target_db",
            "doris_username": "doris_user",
            "doris_password": "doris_pass"
        }

        config_str = generator.generate_with_params("mysql", "doris", table_info, params)

        # 验证源数据库连接
        assert "192.168.1.100:3306" in config_str
        assert "root" in config_str
        assert "password123" in config_str
        assert "mydb" in config_str

        # 验证Doris连接
        assert "192.168.1.200:8030" in config_str
        assert "doris_user" in config_str
        assert "doris_pass" in config_str
        assert "target_db" in config_str

    def test_default_connection_info(self):
        """测试默认连接信息"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证默认值
        assert "source_host:3306" in config_str
        assert "source_username" in config_str
        assert "doris_fe_host:8030" in config_str
        assert "doris_username" in config_str

    def test_default_ports(self):
        """测试默认端口"""
        generator = SeaTunnelGenerator()

        # MySQL
        config_str = generator.generate("mysql", "doris", TestTableInfo.create_simple_table())
        assert ":3306" in config_str

        # PostgreSQL
        config_str = generator.generate("postgresql", "doris", TestTableInfo.create_simple_table())
        assert ":5432" in config_str

        # Oracle
        config_str = generator.generate("oracle", "doris", TestTableInfo.create_simple_table())
        assert ":1521" in config_str

        # SQL Server
        config_str = generator.generate("sqlserver", "doris", TestTableInfo.create_simple_table())
        assert ":1433" in config_str

    def test_doris_sink_config(self):
        """测试Doris sink配置"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证Doris sink属性
        assert "batch_max_rows = 1024" in config_str
        assert "batch_max_bytes = 10485760" in config_str
        assert "batch_interval_ms = 1000" in config_str
        assert 'sink.properties.format = "json"' in config_str
        assert 'sink.properties.strip_outer_array = "true"' in config_str

    def test_doris_config_block(self):
        """测试doris.config配置块"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证doris.config配置
        assert "doris.config {" in config_str
        assert 'format = "json"' in config_str
        assert 'read_json_by_line = "true"' in config_str

    def test_table_name_in_config(self):
        """测试表名配置"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证表名
        assert 'table = "users"' in config_str
        assert "source_database.users" in config_str

    def test_transform_sql(self):
        """测试transform SQL配置"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证transform配置
        assert "Sql {" in config_str
        assert "source_table_name = \"source_table\"" in config_str
        assert "result_table_name = \"result_table\"" in config_str

    def test_streaming_config_mysql_cdc(self):
        """测试MySQL流式同步配置"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        params = {
            "source_host": "192.168.1.100",
            "source_port": 3306,
            "source_database": "mydb",
            "source_username": "root",
            "source_password": "password123",
            "doris_host": "192.168.1.200",
            "doris_port": 8030,
            "doris_database": "target_db",
            "doris_username": "doris_user",
            "doris_password": "doris_pass"
        }

        config_str = generator.generate_streaming_config("mysql", "doris", table_info, params)

        # 验证流式配置
        assert 'job.mode = "STREAMING"' in config_str
        assert "checkpoint.interval = 3000" in config_str

        # 验证MySQL CDC配置
        assert "Mysql-CDC {" in config_str
        assert "table-names" in config_str

    def test_streaming_config_non_mysql(self):
        """测试非MySQL的流式配置"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        params = {
            "source_host": "localhost",
            "source_port": 5432,
            "source_database": "mydb",
            "source_username": "postgres",
            "source_password": "pass",
            "doris_host": "localhost",
            "doris_port": 8030,
            "doris_database": "target",
            "doris_username": "root",
            "doris_password": ""
        }

        config_str = generator.generate_streaming_config("postgresql", "doris", table_info, params)

        # 非MySQL应该使用JDBC，但模式为STREAMING
        assert 'job.mode = "STREAMING"' in config_str
        assert "Jdbc {" in config_str

    def test_complex_table_config(self):
        """测试复杂表的配置生成"""
        table_info = TestTableInfo.create_complex_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证所有列都在配置中
        assert "`id`" in config_str
        assert "`user_id`" in config_str
        assert "`order_no`" in config_str
        assert "`total_amount`" in config_str
        assert "`status`" in config_str
        assert "`created_at`" in config_str

    def test_hocon_format(self):
        """测试HOCON格式正确性"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证HOCON格式的基本特征
        assert config_str.startswith("{")
        assert config_str.strip().endswith("}")
        assert "env {" in config_str
        assert "source {" in config_str
        assert "}" in config_str

    def test_query_statement(self):
        """测试查询语句生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证查询语句
        assert "query = " in config_str
        assert "SELECT" in config_str
        assert "FROM" in config_str

    def test_all_columns_in_query(self):
        """测试所有列都在查询中"""
        table_info = TestTableInfo.create_complex_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证所有列名都在配置中
        assert "`id`" in config_str
        assert "`user_id`" in config_str
        assert "`order_no`" in config_str
        assert "`total_amount`" in config_str
        assert "`status`" in config_str
        assert "`created_at`" in config_str

    def test_multiple_tables_scenario(self):
        """测试多表场景配置（虽然每次只处理一个表）"""
        # 模拟不同的表
        table_names = ["users", "products", "orders", "order_items"]

        for table_name in table_names:
            table_info = TableInfo(
                name=table_name,
                columns=[
                    ColumnInfo(name="id", source_type="INT", target_type="INT", is_primary=True),
                    ColumnInfo(name="name", source_type="VARCHAR(100)", target_type="VARCHAR(100)")
                ],
                primary_keys=["id"]
            )

            generator = SeaTunnelGenerator()
            config_str = generator.generate("mysql", "doris", table_info)

            assert f'table = "{table_name}"' in config_str

    def test_config_structure_completeness(self):
        """测试配置结构完整性"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证所有必需的配置块都存在
        required_blocks = [
            "env {",
            "source {",
            "transform {",
            "sink {",
            "Jdbc {",
            "Sql {",
            "Doris {"
        ]

        for block in required_blocks:
            assert block in config_str

    def test_json_output_properties(self):
        """测试JSON输出属性"""
        table_info = TestTableInfo.create_simple_table()
        generator = SeaTunnelGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 验证JSON相关配置
        assert 'format = "json"' in config_str
        assert 'strip_outer_array = "true"' in config_str
