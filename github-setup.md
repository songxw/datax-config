# GitHub 仓库设置指南

## 1. 创建 GitHub 仓库

1. 登录 GitHub: https://github.com
2. 点击右上角的 "+" 图标，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `datax-config-generator`
   - **Description**: `A web-based DDL converter and sync config generator for DataX/SeaTunnel`
   - **Public/Private**: 选择 Public（公开仓库）
   - **Initialize repository**: 不要勾选任何选项
4. 点击 "Create repository"

## 2. 本地仓库连接

在本地项目目录执行以下命令：

```bash
# 添加远程仓库地址（替换为你的仓库地址）
git remote add origin https://github.com/songxw/datax-config-generator.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

## 3. 仓库配置建议

### 设置仓库主题
在仓库设置中添加以下主题标签：
- `datax`
- `seatunnel`
- `ddl-converter`
- `database-sync`
- `doris`
- `mysql`
- `postgresql`
- `oracle`
- `sqlserver`

### 启用功能
在仓库设置中启用：
- **Issues**: 用于问题跟踪
- **Discussions**: 用于社区讨论
- **Projects**: 用于项目管理
- **Wiki**: 用于文档（可选）

### 分支保护规则
建议设置分支保护规则：
1. 进入 Settings → Branches
2. 点击 "Add rule"
3. 分支名称模式: `main`
4. 启用：
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging

## 4. 发布 Release

当项目稳定后，可以创建 Release：

1. 进入仓库的 Releases 页面
2. 点击 "Create a new release"
3. 标签版本: `v1.0.0`
4. 发布标题: `DataX Config Generator v1.0.0`
5. 描述内容：

```markdown
# DataX Config Generator v1.0.0

## 🎉 新功能
- 支持 MySQL、PostgreSQL、Oracle、SQL Server 到 Doris 的 DDL 转换
- 自动生成 DataX 和 SeaTunnel 同步配置文件
- 优化 Doris UNIQUE 模型，支持主键识别和分布式配置
- 提供直观的 Web 界面和 RESTful API

## 🚀 快速开始
```bash
git clone https://github.com/songxw/datax-config-generator.git
cd datax-config-generator
./deploy.sh
```

访问 http://localhost:5173 开始使用！

## 📖 文档
- [项目文档](README.md)
- [架构说明](docs/architecture.md)
- [部署指南](github-setup.md)
```

## 5. 社区建设

### 添加贡献指南
创建 `.github/CONTRIBUTING.md` 文件：

```markdown
# 贡献指南

感谢您对 DataX Config Generator 项目的关注！

## 如何贡献

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 开发规范

- 代码风格：遵循 PEP 8（Python）和 ESLint（JavaScript）
- 提交信息：遵循 Conventional Commits 规范
- 测试：确保所有测试通过
- 文档：更新相关文档

## 问题报告

使用 GitHub Issues 报告问题，请包含：
- 问题描述
- 重现步骤
- 期望行为
- 实际行为
- 环境信息
```

### 添加 Issue 模板
在 `.github/ISSUE_TEMPLATE/` 目录下创建：
- `bug_report.md` - 错误报告模板
- `feature_request.md` - 功能请求模板
- `question.md` - 问题咨询模板

### 添加 Pull Request 模板
创建 `.github/pull_request_template.md`：

```markdown
## 描述
简要描述这个 PR 的目的和变化

## 类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 代码重构
- [ ] 文档更新

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] 通过了所有测试

## 相关 Issue
Fixes #(issue 编号)
```

## 6. 持续集成（可选）

### GitHub Actions
创建 `.github/workflows/ci.yml`：

```yaml
name: CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    - name: Run tests
      run: |
        cd backend
        pytest

  frontend-build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    - name: Install dependencies
      run: |
        cd frontend
        npm install
    - name: Build
      run: |
        cd frontend
        npm run build
```

## 7. 推广建议

### 社交媒体
- Twitter: 分享项目亮点和使用案例
- LinkedIn: 发布技术文章和项目更新
- 技术博客: 撰写详细的技术实现文章

### 技术社区
- Reddit: r/programming, r/dataengineering
- Stack Overflow: 回答相关问题并提及项目
- 掘金、CSDN: 发布中文技术文章

### 相关项目
- 在 DataX、SeaTunnel、Doris 的社区中分享
- 提交到 awesome-* 列表
- 参与相关技术会议和分享

记住定期更新项目，响应社区反馈，持续改进功能！