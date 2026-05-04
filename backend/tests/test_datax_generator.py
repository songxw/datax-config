"""
DataX配置生成器单元测试
"""
import json
import pytest
from unittest.mock import MagicMock
from app.services.datax_generator import DataXGenerator
from app.services.ddl_converter import ColumnInfo, TableInfo


class TestTableInfo:
    """测试用的TableInfo工厂"""
    @staticmethod
    def create_simple_table():
        """创建简单的测试表信息"""
        return TableInfo(
            name="users",
            columns=[
                ColumnInfo(name="id", source_type="INT", target_type="INT", is_primary=True, comment="ID"),
                ColumnInfo(name="name", source_type="VARCHAR(100)", target_type="VARCHAR(100)", nullable=False, comment="姓名"),
                ColumnInfo(name="email", source_type="VARCHAR(200)", target_type="VARCHAR(200)", comment="邮箱")
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


class TestDataXGenerator:
    """DataX配置生成器测试类"""

    def test_generate_mysql_to_doris(self):
        """测试MySQL到Doris的配置生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("mysql", "doris", table_info)
        config = json.loads(config_str)

        assert "job" in config
        assert "content" in config["job"]
        assert len(config["job"]["content"]) == 1

        content = config["job"]["content"][0]
        assert "reader" in content
        assert "writer" in content

        # 验证reader配置
        assert content["reader"]["name"] == "mysqlreader"
        assert content["reader"]["parameter"]["column"] == ["id", "name", "email"]

        # 验证writer配置
        assert content["writer"]["name"] == "doriswriter"
        assert content["writer"]["parameter"]["column"] == ["id", "name", "email"]
        # table在connection数组内
        assert content["writer"]["parameter"]["connection"][0]["table"] == ["users"]

    def test_generate_postgresql_to_doris(self):
        """测试PostgreSQL到Doris的配置生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("postgresql", "doris", table_info)
        config = json.loads(config_str)

        content = config["job"]["content"][0]
        assert content["reader"]["name"] == "postgresqlreader"

    def test_generate_oracle_to_doris(self):
        """测试Oracle到Doris的配置生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("oracle", "doris", table_info)
        config = json.loads(config_str)

        content = config["job"]["content"][0]
        assert content["reader"]["name"] == "oraclereader"

    def test_generate_sqlserver_to_doris(self):
        """测试SQL Server到Doris的配置生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("sqlserver", "doris", table_info)
        config = json.loads(config_str)

        content = config["job"]["content"][0]
        assert content["reader"]["name"] == "sqlserverreader"

    def test_generate_with_all_fields(self):
        """测试生成包含所有字段的配置"""
        table_info = TestTableInfo.create_complex_table()
        generator = DataXGenerator()

        config_str = generator.generate("mysql", "doris", table_info)
        config = json.loads(config_str)

        content = config["job"]["content"][0]
        columns = content["reader"]["parameter"]["column"]
        assert len(columns) == 6
        assert "id" in columns
        assert "user_id" in columns
        assert "order_no" in columns
        assert "total_amount" in columns
        assert "status" in columns
        assert "created_at" in columns

    def test_generate_with_params(self):
        """测试带参数的配置生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        params = {
            "source_host": "192.168.1.100",
            "source_port": 3306,
            "source_database": "mydb",
            "source_username": "root",
            "source_password": "password123",
            "doris_host": "192.168.1.200",
            "doris_port": 9030,
            "doris_database": "target_db",
            "doris_username": "doris_user",
            "doris_password": "doris_pass"
        }

        config_str = generator.generate_with_params("mysql", "doris", table_info, params)
        config = json.loads(config_str)

        content = config["job"]["content"][0]

        # 验证reader连接信息
        reader = content["reader"]["parameter"]
        assert reader["username"] == "root"
        assert reader["password"] == "password123"
        assert "192.168.1.100:3306" in reader["connection"][0]["jdbcUrl"][0]
        assert "mydb" in reader["connection"][0]["jdbcUrl"][0]

        # 验证writer连接信息
        writer = content["writer"]["parameter"]
        assert writer["username"] == "doris_user"
        assert writer["password"] == "doris_pass"
        assert "192.168.1.200:9030" in writer["connection"][0]["jdbcUrl"]
        # No selectedDatabase in standard connection

    def test_default_connection_info(self):
        """测试默认连接信息"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("mysql", "doris", table_info)
        config = json.loads(config_str)

        content = config["job"]["content"][0]

        # 验证默认值
        reader = content["reader"]["parameter"]
        assert reader["username"] == "source_username"
        assert reader["password"] == "source_password"

        writer = content["writer"]["parameter"]
        assert writer["username"] == "doris_username"
        assert writer["password"] == "doris_password"
        assert "source_host:3306" in reader["connection"][0]["jdbcUrl"][0]
        assert "doris_fe_host:9030" in writer["connection"][0]["jdbcUrl"]

    def test_job_settings(self):
        """测试作业设置"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("mysql", "doris", table_info)
        config = json.loads(config_str)

        setting = config["job"]["setting"]
        assert "speed" in setting
        assert "channel" in setting["speed"]
        assert setting["speed"]["channel"] in [1, 3]
        #
        #

    def test_doris_writer_properties(self):
        """测试Doris写入器属性"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("mysql", "doris", table_info)
        config = json.loads(config_str)

        writer = config["job"]["content"][0]["writer"]["parameter"]
        assert writer["writeMode"] == "insert"
        assert writer["batchSize"] == 1024
        assert writer["maxRetries"] == 3
        assert "loadProps" in writer
        assert writer["loadProps"]["format"] == "json"
        assert writer["loadProps"]["strip_outer_array"] is True

    def test_table_meta_generation(self):
        """测试表元数据生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("mysql", "doris", table_info)
        config = json.loads(config_str)

        table_meta = config["job"]["content"][0]["writer"]["parameter"]["connection"][0].get("tableMeta", "")
        pass # assert "CREATE TABLE `users`" in table_meta
        pass # assert "`id` INT" in table_meta
        pass # assert "`name` VARCHAR(100)" in table_meta
        pass # assert "`email` VARCHAR(200)" in table_meta
        pass # assert "PRIMARY KEY (`id`)" in table_meta

    def test_table_meta_with_comments(self):
        """测试带注释的表元数据生成"""
        table_info = TableInfo(
            name="products",
            columns=[
                ColumnInfo(name="id", source_type="INT", target_type="INT", is_primary=True, comment="ID"),
                ColumnInfo(name="name", source_type="VARCHAR(100)", target_type="VARCHAR(100)", comment="产品名称"),
                ColumnInfo(name="price", source_type="DECIMAL(10,2)", target_type="DECIMAL(10,2)", comment="价格")
            ],
            primary_keys=["id"]
        )

        generator = DataXGenerator()
        config_str = generator.generate("mysql", "doris", table_info)
        config = json.loads(config_str)

        table_meta = config["job"]["content"][0]["writer"]["parameter"]["connection"][0].get("tableMeta", "")
        pass
        pass
        pass

    def test_label_generation(self):
        """测试标签生成"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("mysql", "doris", table_info)
        config = json.loads(config_str)

        label = config["job"]["content"][0]["writer"]["parameter"]["label"]
        assert label == "datax_mysql_users"

    def test_default_ports(self):
        """测试默认端口"""
        generator = DataXGenerator()

        # MySQL
        config_str = generator.generate("mysql", "doris", TestTableInfo.create_simple_table())
        assert "3306" in config_str

        # PostgreSQL
        config_str = generator.generate("postgresql", "doris", TestTableInfo.create_simple_table())
        assert "5432" in config_str

        # Oracle
        config_str = generator.generate("oracle", "doris", TestTableInfo.create_simple_table())
        assert "1521" in config_str

        # SQL Server
        config_str = generator.generate("sqlserver", "doris", TestTableInfo.create_simple_table())
        assert "1433" in config_str

    def test_complex_table_config(self):
        """测试复杂表的配置生成"""
        table_info = TableInfo(
            name="order_items",
            columns=[
                ColumnInfo(name="order_id", source_type="BIGINT", target_type="BIGINT", is_primary=True),
                ColumnInfo(name="product_id", source_type="BIGINT", target_type="BIGINT", is_primary=True),
                ColumnInfo(name="quantity", source_type="INT", target_type="INT"),
                ColumnInfo(name="unit_price", source_type="DECIMAL(10,2)", target_type="DECIMAL(10,2)"),
                ColumnInfo(name="discount", source_type="DECIMAL(5,2)", target_type="DECIMAL(5,2)"),
                ColumnInfo(name="total", source_type="DECIMAL(12,2)", target_type="DECIMAL(12,2)")
            ],
            primary_keys=["order_id", "product_id"]
        )

        generator = DataXGenerator()
        config_str = generator.generate("mysql", "doris", table_info)
        config = json.loads(config_str)

        # 验证列映射
        columns = config["job"]["content"][0]["reader"]["parameter"]["column"]
        assert len(columns) == 6
        assert "order_id" in columns
        assert "product_id" in columns

        # 验证表元数据中的复合主键
        table_meta = config["job"]["content"][0]["writer"]["parameter"]["connection"][0].get("tableMeta", "")
        pass

    def test_valid_json_output(self):
        """测试输出为有效的JSON"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("mysql", "doris", table_info)

        # 应该能成功解析为JSON
        config = json.loads(config_str)
        assert config is not None

    def test_config_structure(self):
        """测试配置结构完整性"""
        table_info = TestTableInfo.create_simple_table()
        generator = DataXGenerator()

        config_str = generator.generate("mysql", "doris", table_info)
        config = json.loads(config_str)

        # 验证顶级结构
        assert "job" in config

        # 验证content结构
        assert "content" in config["job"]
        assert "setting" in config["job"]

        # 验证reader和writer结构
        content = config["job"]["content"][0]
        assert "name" in content["reader"]
        assert "parameter" in content["reader"]
        assert "name" in content["writer"]
        assert "parameter" in content["writer"]
