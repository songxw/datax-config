# 测试说明

## 测试框架

本项目使用 `pytest` 作为测试框架。

## 安装测试依赖

```bash
cd backend
pip install -r requirements.txt
```

## 运行测试

### 运行所有测试
```bash
pytest
```

### 运行特定测试文件
```bash
pytest tests/test_ddl_converter.py
```

### 运行特定测试类
```bash
pytest tests/test_ddl_converter.py::TestDDLConverter
```

### 运行特定测试方法
```bash
pytest tests/test_ddl_converter.py::TestDDLConverter::test_mysql_to_doris_simple_table
```

### 运行并显示详细输出
```bash
pytest -v
```

### 生成覆盖率报告
```bash
pytest --cov=app --cov-report=html
```

覆盖率报告将生成在 `htmlcov/index.html`

### 查看覆盖率统计
```bash
pytest --cov=app --cov-report=term-missing
```

## 测试文件说明

| 文件 | 说明 | 测试数量 |
|------|------|----------|
| test_ddl_converter.py | DDL转换器单元测试 | 20+ |
| test_datax_generator.py | DataX配置生成器测试 | 20+ |
| test_seatunnel_generator.py | SeaTunnel配置生成器测试 | 20+ |
| test_api.py | API接口测试 | 25+ |

## 测试覆盖范围

### DDL转换器 (ddl_converter.py)
- MySQL到Doris的简单表转换
- 带注释的表转换
- 数据类型映射
- PostgreSQL/Oracle/SQL Server转换
- 复合主键
- 反引号处理
- IF NOT EXISTS处理
- 无效DDL处理
- 所有MySQL类型测试
- Doris表属性生成
- 可空列处理

### DataX配置生成器 (datax_generator.py)
- MySQL/PostgreSQL/Oracle/SQL Server到Doris配置
- 带参数的配置生成
- 默认连接信息
- 作业设置验证
- Doris写入器属性
- 表元数据生成
- 标签生成
- 默认端口
- 复杂表配置
- JSON输出验证
- 配置结构完整性

### SeaTunnel配置生成器 (seatunnel_generator.py)
- MySQL/PostgreSQL/Oracle/SQL Server到Doris配置
- 环境配置
- 源表列配置
- 带参数的配置生成
- 默认连接信息
- 默认端口
- Doris sink配置
- doris.config配置块
- 表名配置
- transform SQL配置
- 流式同步配置
- HOCON格式验证
- 查询语句生成
- 配置结构完整性

### API接口 (api.py)
- 根路径和健康检查
- 支持的数据库列表
- 各种数据库的转换
- DataX和SeaTunnel配置
- 复杂表转换
- 复合主键
- 无效DDL处理
- 带注释的表
- 默认值
- 可空列
- 请求验证

## CI/CD 集成

可以在GitHub Actions或其他CI系统中集成测试：

```yaml
- name: Run tests
  run: |
    cd backend
    pytest --cov=app --cov-report=xml
```

## 编写新测试

### 单元测试示例

```python
import pytest
from app.services.your_service import YourClass

class TestYourClass:
    def test_your_method(self):
        obj = YourClass()
        result = obj.your_method(input_data)
        assert result == expected_output
```

### API测试示例

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_your_endpoint():
    response = client.post("/api/your-endpoint", json={...})
    assert response.status_code == 200
```

## 测试最佳实践

1. **命名规范**：测试函数以 `test_` 开头
2. **独立性**：每个测试应该独立运行
3. **清晰的断言**：使用明确的断言消息
4. **覆盖边界情况**：包括正常和异常情况
5. **保持简单**：每个测试只测试一个功能点
