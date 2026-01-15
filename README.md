# DataX Config Generator

一个基于Web的数据库DDL转换和同步配置生成工具，支持多种数据库之间的DDL转换，并能自动生成DataX和SeaTunnel同步配置文件。

## 🎯 项目功能

### 核心功能
- **DDL转换**：支持MySQL、PostgreSQL、Oracle、SQL Server等数据库之间的DDL转换
- **Doris优化**：针对Doris数据库进行特殊优化，支持UNIQUE模型
- **同步配置生成**：自动生成DataX和SeaTunnel同步配置文件
- **Web界面**：提供直观的Web界面进行操作
- **API接口**：提供RESTful API供程序调用

### 支持的数据库
- **源数据库**：MySQL、PostgreSQL、Oracle、SQL Server
- **目标数据库**：Doris、MySQL、PostgreSQL、Oracle、SQL Server
- **同步工具**：DataX、SeaTunnel

## 🏗️ 项目架构

### 技术栈
- **前端**：React + TypeScript + Ant Design + Vite
- **后端**：Python + FastAPI + Pydantic
- **数据库类型转换**：基于规则引擎的DDL解析和转换
- **配置生成**：模板引擎生成DataX/SeaTunnel配置

### 项目结构
```
datax-config/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── core/              # 核心配置
│   │   ├── models/            # 数据模型
│   │   ├── routers/           # API路由
│   │   ├── services/          # 业务逻辑
│   │   └── main.py            # 主程序入口
│   ├── requirements.txt       # Python依赖
│   └── venv/                  # 虚拟环境
├── frontend/                   # 前端应用
│   ├── src/
│   │   ├── components/        # React组件
│   │   ├── pages/             # 页面组件
│   │   ├── services/          # API服务
│   │   └── types/             # TypeScript类型定义
│   ├── package.json           # 前端依赖
│   └── vite.config.ts         # Vite配置
└── docs/                      # 文档
```

### 核心模块
- **DDL转换器**：解析源数据库DDL，转换为目标数据库语法
- **类型映射**：维护不同数据库间的数据类型映射关系
- **配置生成器**：根据表结构生成DataX/SeaTunnel配置文件
- **模型优化**：针对Doris等数据库的特殊模型优化

## 🚀 快速开始

### 环境要求
- **Python**：3.8+
- **Node.js**：16+
- **npm/yarn**：包管理器

### 1. 克隆项目
```bash
git clone https://github.com/your-username/datax-config.git
cd datax-config
```

### 2. 后端部署

#### 创建虚拟环境
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

#### 安装依赖
```bash
pip install -r requirements.txt
```

#### 启动后端服务
```bash
python -m app.main
```
后端服务将运行在：http://localhost:8000

### 3. 前端部署

#### 安装依赖
```bash
cd frontend
npm install
```

#### 启动开发服务器
```bash
npm run dev
```
前端服务将运行在：http://localhost:5173

### 4. 访问应用
打开浏览器访问：http://localhost:5173

## 📖 使用说明

### Web界面使用
1. **选择源数据库类型**：从下拉框选择源数据库类型
2. **输入DDL语句**：在文本框中输入源数据库的DDL语句
3. **选择目标数据库类型**：选择要转换到的目标数据库类型
4. **选择同步工具**：选择DataX或SeaTunnel
5. **点击转换**：系统将自动生成转换后的DDL和同步配置
6. **查看结果**：在结果区域查看生成的DDL和配置文件

### API接口使用

#### 转换DDL并生成配置
```bash
curl -X POST http://localhost:8000/api/convert \
  -H "Content-Type: application/json" \
  -d '{
    "source_db_type": "mysql",
    "target_db_type": "doris",
    "ddl": "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));",
    "sync_tool": "datax"
  }'
```

#### 响应示例
```json
{
  "success": true,
  "message": "转换成功",
  "converted_ddl": "CREATE TABLE IF NOT EXISTS `users` (\n  `id` INT NOT NULL,\n  `name` VARCHAR(100)\n)\nENGINE = OLAP\nUNIQUE KEY (`id`)\nDISTRIBUTED BY HASH(`id`) BUCKETS 10\nPROPERTIES (\n  \"replication_allocation\" = \"tag.location.default: 1\"\n)",
  "sync_config": "{\n  \"job\": {\n    \"setting\": {\n      \"speed\": {\n        \"channel\": 3\n      }\n    },\n    \"content\": [...]\n  }\n}",
  "table_info": {
    "table_name": "users",
    "columns": [...],
    "comment": null
  },
  "errors": []
}
```

## 🔧 配置说明

### 后端配置
后端配置文件位于 `backend/app/core/config.py`：
- **API端口**：默认8000
- **日志级别**：INFO
- **CORS配置**：允许前端跨域访问

### 前端配置
前端配置文件位于 `frontend/vite.config.ts`：
- **开发端口**：默认5173
- **代理配置**：API请求代理到后端服务

## 🎯 功能详解

### DDL转换规则
- **数据类型映射**：自动映射不同数据库间的数据类型
- **主键处理**：正确处理主键约束，支持复合主键
- **注释转换**：保留表和列的注释信息
- **默认值**：转换默认值表达式

### Doris特殊优化
- **UNIQUE模型**：有主键时自动使用UNIQUE模型
- **分布式配置**：自动生成DISTRIBUTED BY HASH配置
- **ENGINE类型**：设置为OLAP引擎
- **分桶数量**：默认10个分桶

### 同步配置生成
- **字段映射**：自动生成字段映射配置
- **批量设置**：配置合理的批量参数
- **错误处理**：设置错误重试机制
- **性能优化**：优化通道数和批处理大小

## 🐛 常见问题

### Q1: 后端启动失败
**问题**：端口被占用
**解决**：修改 `backend/app/core/config.py` 中的端口配置

### Q2: 前端无法连接后端
**问题**：跨域访问被阻止
**解决**：检查后端CORS配置，确保允许前端域名访问

### Q3: DDL转换失败
**问题**：复杂的DDL语句无法解析
**解决**：简化DDL语句，确保语法标准

### Q4: 生成的配置无法使用
**问题**：数据库连接信息不正确
**解决**：手动修改生成的配置文件中的连接信息

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目维护者：[Your Name]
- 邮箱：your.email@example.com
- 项目地址：https://github.com/your-username/datax-config

## 🙏 致谢

- [Apache DataX](https://github.com/alibaba/DataX) - 数据同步工具
- [Apache SeaTunnel](https://github.com/apache/seatunnel) - 数据集成平台
- [Apache Doris](https://doris.apache.org/) - 实时分析数据库
- [FastAPI](https://fastapi.tiangolo.com/) - 现代Python Web框架
- [React](https://reactjs.org/) - 前端UI库
- [Ant Design](https://ant.design/) - 企业级UI设计语言