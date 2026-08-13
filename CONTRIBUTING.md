# 贡献指南

感谢你对 GhostLock 项目的关注！本指南将帮助你了解如何为项目做出贡献。

## 如何贡献

### 报告问题

如果你发现了 bug 或者有改进建议，请通过以下方式报告：

1. 在 GitHub 上创建 Issue
2. 提供详细的问题描述
3. 包含复现步骤（如果适用）
4. 提供相关的日志或错误信息

### 提交代码

1. **Fork 项目**
   ```bash
   git clone https://github.com/your-username/GhostLock.git
   cd GhostLock
   ```

2. **创建特性分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **进行修改**
   - 遵循现有的代码风格
   - 添加必要的注释
   - 更新相关文档

4. **测试你的修改**
   - 确保编译通过
   - 在支持的设备上测试
   - 验证 exploit 仍然有效

5. **提交更改**
   ```bash
   git add .
   git commit -m "描述你的修改"
   ```

6. **推送到你的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **创建 Pull Request**
   - 提供清晰的修改说明
   - 引用相关的 Issue（如果有）
   - 等待代码审查

## 代码规范

### C 代码风格

- 使用 4 空格缩进
- 函数名使用 snake_case
- 常量使用 UPPER_CASE
- 行宽限制在 80 字符以内
- 添加必要的注释说明复杂逻辑

### 提交信息

- 使用中文编写提交信息
- 简明扼要地描述修改内容
- 使用祈使语气（如"添加"、"修复"、"更新"）

示例：
```
添加 OPPO Find X8 设备支持

- 添加 findx8/offsets.h 设备条目
- 更新 README.md 文档
- 验证 BTF 偏移量正确性
```

## 添加新设备支持

如果你想要为新设备添加支持，请参考：

1. **README.md** 中的"设备适配"章节
2. **src/devices/** 目录下的现有设备条目
3. **tools/** 目录下的 BTF 分析脚本

### 必需信息

- 内核版本（uname -r）
- kallsyms 符号表
- BTF 信息（task_struct, cred, file_operations 等）
- 物理内存布局

### 测试要求

新设备支持必须在真实设备上测试验证。

## 安全注意事项

⚠️ **重要：** 本项目仅用于安全研究和授权测试。

- 不要在未经授权的设备上测试
- 不要在生产环境中使用
- 遵守当地法律法规
- 负责任地披露漏洞

## 代码审查

所有 Pull Request 都需要经过代码审查。审查重点包括：

- 代码质量和可读性
- 安全性考虑
- 文档完整性
- 测试覆盖

## 获取帮助

如果你有任何问题，可以通过以下方式获取帮助：

- 在 GitHub 上创建 Issue
- 查看现有文档
- 参考示例代码

## 行为准则

请遵循以下行为准则：

- 尊重所有贡献者
- 提供建设性的反馈
- 专注于技术讨论
- 遵守社区 guidelines

感谢你的贡献！
