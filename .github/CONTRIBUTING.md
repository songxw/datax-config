# 贡献指南

感谢您对 DataX Config Generator 项目的关注！我们欢迎各种形式的贡献，包括错误修复、功能改进、文档更新等。

## 🚀 快速开始

1. Fork 本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 📋 贡献类型

### 🐛 错误修复
- 修复代码中的错误
- 改善错误处理
- 修复文档中的错误

### ✨ 新功能
- 添加新的数据库支持
- 添加新的同步工具支持
- 改进用户界面
- 添加新的配置选项

### 📚 文档改进
- 更新 README 文件
- 添加代码注释
- 改进 API 文档
- 添加使用示例

### ⚡ 性能优化
- 优化算法性能
- 减少内存使用
- 提高响应速度

## 📝 开发规范

### 代码风格

#### Python (后端)
- 遵循 [PEP 8](https://pep8.org/) 编码规范
- 使用类型提示
- 编写清晰的函数和变量名
- 添加必要的注释

```python
# 好的示例
def convert_ddl(
    source_ddl: str,
    source_type: str,
    target_type: str
) -> ConversionResult:
    """转换DDL语句到目标数据库格式"""
    # 实现代码
    pass
```

#### TypeScript/JavaScript (前端)
- 遵循 ESLint 配置
- 使用 TypeScript 类型
- 组件命名使用 PascalCase
- 函数命名使用 camelCase

```typescript
// 好的示例
interface TableInfo {
  name: string;
  columns: ColumnInfo[];
  comment?: string;
}

const convertDDL = async (ddl: string): Promise<ConversionResult> => {
  // 实现代码
};
```

### 提交信息规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` 错误修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具的变动

示例：
```
feat: 添加 PostgreSQL 到 Doris 的 DDL 转换支持

- 添加 PostgreSQL 类型映射
- 支持 PostgreSQL 特有语法
- 添加相关测试用例

Fixes #123
```

## 🧪 测试

### 运行测试

后端测试：
```bash
cd backend
pytest -v
```

前端测试：
```bash
cd frontend
npm test
```

### 测试要求

- 新功能必须包含相应的测试
- 错误修复必须添加回归测试
- 保持测试覆盖率
- 测试命名要清晰描述测试内容

## 📖 文档要求

### 代码文档
- 为公共 API 添加文档字符串
- 复杂的算法需要详细注释
- 更新相关的 README 文件

### 用户文档
- 新功能需要更新使用说明
- 添加配置示例
- 更新 API 文档

## 🔍 代码审查

### 审查清单
- [ ] 代码符合项目规范
- [ ] 测试已经通过
- [ ] 文档已经更新
- [ ] 没有引入新的错误
- [ ] 性能影响可以接受

### 审查过程
1. 至少需要一个审查者批准
2. 所有 CI 检查必须通过
3. 解决所有审查意见
4. 保持代码质量

## 🐛 问题报告

使用 GitHub Issues 报告问题，请包含：

- 清晰的问题描述
- 重现步骤
- 期望行为
- 实际行为
- 环境信息
- 相关代码或配置

## 💡 功能建议

欢迎提出新功能建议：

- 描述功能需求
- 说明使用场景
- 提供实现建议（如果有）
- 讨论可行性和优先级

## 📞 联系方式

如果您有任何问题或建议，请通过以下方式联系我们：

- 创建 GitHub Issue
- 参与 GitHub Discussions
- 提交 Pull Request

## 🙏 致谢

感谢所有为项目做出贡献的开发者！您的贡献将帮助更多的开发者提高工作效率。

## 📄 许可证

通过贡献代码，您同意您的贡献将在与项目相同的 MIT 许可证下发布。