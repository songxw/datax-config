"""
API接口测试
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestRootAPI:
    """根API测试"""

    def test_root_endpoint(self):
        """测试根路径"""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"
        assert data["docs"] == "/docs"

    def test_health_endpoint(self):
        """测试健康检查接口"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestSupportedDBAPI:
    """支持的数据库API测试"""

    def test_get_supported_databases(self):
        """测试获取支持的数据库列表"""
        response = client.get("/api/supported-db")
        assert response.status_code == 200

        data = response.json()
        assert "source_databases" in data
        assert "target_databases" in data
        assert "sync_tools" in data

        # 验证源数据库
        source_dbs = data["source_databases"]
        assert len(source_dbs) == 4
        db_values = [db["value"] for db in source_dbs]
        assert "mysql" in db_values
        assert "postgresql" in db_values
        assert "oracle" in db_values
        assert "sqlserver" in db_values

        # 验证目标数据库
        target_dbs = data["target_databases"]
        assert len(target_dbs) == 1
        assert target_dbs[0]["value"] == "doris"

        # 验证同步工具
        sync_tools = data["sync_tools"]
        assert len(sync_tools) == 2
        tool_values = [tool["value"] for tool in sync_tools]
        assert "datax" in tool_values
        assert "seatunnel" in tool_values


class TestConvertAPI:
    """转换API测试"""

    def test_convert_mysql_to_doris_with_datax(self):
        """测试MySQL到Doris转换，使用DataX"""
        request = {
            "source_db_type": "mysql",
            "ddl": "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));",
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "converted_ddl" in data
        assert "sync_config" in data
        assert "table_info" in data
        assert "CREATE TABLE IF NOT EXISTS" in data["converted_ddl"]

    def test_convert_mysql_to_doris_with_seatunnel(self):
        """测试MySQL到Doris转换，使用SeaTunnel"""
        request = {
            "source_db_type": "mysql",
            "ddl": "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));",
            "target_db_type": "doris",
            "sync_tool": "seatunnel"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "converted_ddl" in data
        assert "sync_config" in data
        assert "env {" in data["sync_config"]  # SeaTunnel配置特征

    def test_convert_postgresql_to_doris(self):
        """测试PostgreSQL到Doris转换"""
        request = {
            "source_db_type": "postgresql",
            "ddl": "CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(100));",
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "converted_ddl" in data
        assert data["table_info"]["table_name"] == "products"

    def test_convert_oracle_to_doris(self):
        """测试Oracle到Doris转换"""
        request = {
            "source_db_type": "oracle",
            "ddl": "CREATE TABLE employees (id NUMBER PRIMARY KEY, name VARCHAR2(100));",
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "converted_ddl" in data
        assert data["table_info"]["table_name"] == "employees"

    def test_convert_sqlserver_to_doris(self):
        """测试SQL Server到Doris转换"""
        request = {
            "source_db_type": "sqlserver",
            "ddl": "CREATE TABLE customers (id INT PRIMARY KEY, name NVARCHAR(100));",
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert "converted_ddl" in data
        assert data["table_info"]["table_name"] == "customers"

    def test_convert_complex_table(self):
        """测试复杂表转换"""
        ddl = """
        CREATE TABLE orders (
            id BIGINT PRIMARY KEY,
            user_id BIGINT NOT NULL,
            order_no VARCHAR(50),
            total_amount DECIMAL(10,2),
            status INT DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        ) COMMENT='订单表';
        """

        request = {
            "source_db_type": "mysql",
            "ddl": ddl,
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert len(data["table_info"]["columns"]) == 6
        assert data["table_info"]["comment"] == "订单表"

    def test_convert_with_composite_primary_key(self):
        """测试复合主键转换"""
        ddl = """
        CREATE TABLE order_items (
            order_id INT,
            product_id INT,
            quantity INT,
            price DECIMAL(10,2),
            PRIMARY KEY (order_id, product_id)
        )
        """

        request = {
            "source_db_type": "mysql",
            "ddl": ddl,
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert data["table_info"]["primary_keys"] == ["order_id", "product_id"]

    def test_convert_invalid_ddl(self):
        """测试无效DDL"""
        request = {
            "source_db_type": "mysql",
            "ddl": "INVALID SQL STATEMENT",
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is False
        assert "errors" in data
        assert len(data["errors"]) > 0

    def test_convert_empty_ddl(self):
        """测试空DDL"""
        request = {
            "source_db_type": "mysql",
            "ddl": "",
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is False

    def test_convert_with_all_mysql_types(self):
        """测试包含所有MySQL类型"""
        ddl = """
        CREATE TABLE all_types (
            id INT PRIMARY KEY,
            tiny_col TINYINT,
            small_col SMALLINT,
            big_col BIGINT,
            float_col FLOAT,
            double_col DOUBLE,
            decimal_col DECIMAL(10,2),
            char_col CHAR(10),
            varchar_col VARCHAR(100),
            text_col TEXT,
            date_col DATE,
            datetime_col DATETIME,
            timestamp_col TIMESTAMP,
            bool_col BOOLEAN
        )
        """

        request = {
            "source_db_type": "mysql",
            "ddl": ddl,
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert len(data["table_info"]["columns"]) == 14

    def test_convert_datax_config_structure(self):
        """测试DataX配置结构"""
        request = {
            "source_db_type": "mysql",
            "ddl": "CREATE TABLE test (id INT PRIMARY KEY);",
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True

        # 验证DataX配置结构
        sync_config = data["sync_config"]
        assert "job" in sync_config
        assert "content" in sync_config["job"]
        assert "mysqlreader" in sync_config
        assert "doriswriter" in sync_config

    def test_convert_seatunnel_config_structure(self):
        """测试SeaTunnel配置结构"""
        request = {
            "source_db_type": "mysql",
            "ddl": "CREATE TABLE test (id INT PRIMARY KEY);",
            "target_db_type": "doris",
            "sync_tool": "seatunnel"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True

        # 验证SeaTunnel配置结构
        sync_config = data["sync_config"]
        assert "env" in sync_config
        assert "source" in sync_config
        assert "transform" in sync_config
        assert "sink" in sync_config

    def test_convert_with_table_comments(self):
        """测试带表注释的转换"""
        ddl = """
        CREATE TABLE products (
            id INT PRIMARY KEY,
            name VARCHAR(100) COMMENT '产品名称'
        ) COMMENT='产品表'
        """

        request = {
            "source_db_type": "mysql",
            "ddl": ddl,
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True
        assert data["table_info"]["comment"] == "产品表"

        # 验证列注释
        name_col = next((c for c in data["table_info"]["columns"] if c["name"] == "name"), None)
        assert name_col is not None
        assert name_col["comment"] == "产品名称"

    def test_convert_with_default_values(self):
        """测试带默认值的转换"""
        ddl = """
        CREATE TABLE test (
            id INT PRIMARY KEY,
            status INT DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """

        request = {
            "source_db_type": "mysql",
            "ddl": ddl,
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True

        # 验证默认值
        status_col = next((c for c in data["table_info"]["columns"] if c["name"] == "status"), None)
        assert status_col is not None
        assert status_col["default_value"] == "0"

    def test_convert_with_nullable(self):
        """测试可空列转换"""
        ddl = """
        CREATE TABLE test (
            id INT PRIMARY KEY,
            required_col VARCHAR(100) NOT NULL,
            optional_col VARCHAR(100)
        )
        """

        request = {
            "source_db_type": "mysql",
            "ddl": ddl,
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 200

        data = response.json()
        assert data["success"] is True

        # 验证nullable属性
        required_col = next((c for c in data["table_info"]["columns"] if c["name"] == "required_col"), None)
        assert required_col is not None
        assert required_col["nullable"] is False

        optional_col = next((c for c in data["table_info"]["columns"] if c["name"] == "optional_col"), None)
        assert optional_col is not None
        assert optional_col["nullable"] is True

    def test_request_validation_invalid_db_type(self):
        """测试无效数据库类型"""
        request = {
            "source_db_type": "invalid_db",
            "ddl": "CREATE TABLE test (id INT);",
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        # Pydantic验证错误
        assert response.status_code == 422

    def test_request_validation_invalid_sync_tool(self):
        """测试无效同步工具"""
        request = {
            "source_db_type": "mysql",
            "ddl": "CREATE TABLE test (id INT);",
            "target_db_type": "doris",
            "sync_tool": "invalid_tool"
        }

        response = client.post("/api/convert", json=request)
        # Pydantic验证错误
        assert response.status_code == 422

    def test_missing_required_fields(self):
        """测试缺少必填字段"""
        # 缺少ddl字段
        request = {
            "source_db_type": "mysql",
            "target_db_type": "doris",
            "sync_tool": "datax"
        }

        response = client.post("/api/convert", json=request)
        assert response.status_code == 422
