---
title: 贡献指南
description: 如何为 GhostLock 项目做出贡献
---

## 贡献方式

你可以通过以下方式为 GhostLock 项目做出贡献：

- **报告 Bug** - 发现问题时提交 Issue
- **请求功能** - 提出新功能建议
- **提交代码** - 修复 bug 或添加新功能
- **添加设备支持** - 为新的设备添加支持
- **改进文档** - 完善项目文档
- **翻译** - 翻译文档到其他语言

## 报告问题

### 报告 Bug

1. 打开 [GitHub Issues](https://github.com/wzhdgithub/GhostLock/issues)
2. 点击 "New issue"
3. 选择 "Bug 报告" 模板
4. 填写以下信息：
   - 设备型号
   - 内核版本
   - Android 版本
   - 复现步骤
   - 日志输出

### 请求功能

1. 打开 [GitHub Issues](https://github.com/wzhdgithub/GhostLock/issues)
2. 点击 "New issue"
3. 选择 "功能请求" 模板
4. 描述你需要的功能

### 请求设备支持

1. 打开 [GitHub Issues](https://github.com/wzhdgithub/GhostLock/issues)
2. 点击 "New issue"
3. 选择 "设备支持请求" 模板
4. 提供设备信息

## 提交代码

### 工作流程

1. **Fork 仓库**

```bash
# 在 GitHub 上点击 Fork 按钮
git clone https://github.com/your-username/GhostLock.git
cd GhostLock

# 添加上游仓库
git remote add upstream https://github.com/wzhdgithub/GhostLock.git
```

2. **创建分支**

```bash
# 同步最新代码
git fetch upstream
git checkout -b feature/your-feature-name upstream/main
```

3. **进行修改**

```bash
# 编写代码
# 添加测试
# 更新文档
```

4. **提交更改**

```bash
git add .
git commit -m "描述你的修改"
```

5. **推送到你的 Fork**

```bash
git push origin feature/your-feature-name
```

6. **创建 Pull Request**

```bash
# 在 GitHub 上创建 PR
# 选择你的分支 → main 分支
# 填写 PR 描述
```

### 分支命名规范

| 类型 | 前缀 | 示例 |
|------|------|------|
| 功能 | `feature/` | `feature/device-support` |
| 修复 | `fix/` | `fix/offsets-bug` |
| 文档 | `docs/` | `docs/readme-update` |
| 重构 | `refactor/` | `refactor/util-cleanup` |
| 测试 | `test/` | `test/add-unit-tests` |

### 提交信息规范

```bash
# 格式
<类型>: <描述>

# 示例
feat: 添加 OPPO Find X8 设备支持
fix: 修复 MM_STRUCT_SZ 运行时偏移问题
docs: 更新 README 文档
refactor: 重构 pipe 喷射代码
test: 添加单元测试
```

### 代码规范

#### C 语言规范

```c
// 缩进: 4 空格
// 命名: snake_case
// 常量: UPPER_CASE

// 正确示例
int calculate_offset(uint64_t address) {
    const int MAX_BUFFER = 1024;
    return (int)(address & 0xff);
}

// 错误示例
int calculateOffset(INT addr) {
    const INT MaxBuffer = 1024;
    return (int)(addr & 0xff);
}
```

#### Python 规范

```python
# 缩进: 4 空格
# 命名: snake_case
# 使用类型提示

def parse_btf(btf_data: bytes) -> dict:
    """解析 BTF 数据"""
    result = {}
    # ...
    return result
```

## 代码审查

所有 Pull Request 都需要经过代码审查。

### 审查标准

- **正确性** - 代码逻辑是否正确
- **安全性** - 是否有安全漏洞
- **效率** - 是否高效
- **可读性** - 是否易于理解
- **一致性** - 是否符合项目风格

### 审查流程

1. 提交 PR 后，维护者会审查
2. 如果有问题，会提出修改意见
3. 你根据意见修改
4. 通过审查后合并

## 添加设备支持

添加新设备支持的流程：

1. 参考 [添加新设备]({{ '/add-device' | relative_url }}) 指南
2. 提取内核信息
3. 创建设备条目
4. 测试验证
5. 提交 PR

### 设备条目检查清单

- [ ] 内核版本（uname -r）正确
- [ ] KIMAGE_TEXT_BASE 正确
- [ ] 符号偏移量正确
- [ ] task_struct 偏移量正确
- [ ] cred 偏移量正确
- [ ] file_operations 偏移量正确
- [ ] rt_mutex_waiter 偏移量正确
- [ ] mm_struct_sz 正确
- [ ] PSELECT 表选择正确
- [ ] 在真实设备上测试通过

## 测试

### 添加测试

```bash
# 测试目录
test/
├── unit/          # 单元测试
├── integration/   # 集成测试
└── devices/       # 设备测试
```

### 运行测试

```bash
# 编译
make

# 运行测试（需要真机）
adb push ghostlock /data/local/tmp/
adb shell /data/local/tmp/ghostlock --test
```

## 文档贡献

### 改进 README

- 修正错误
- 补充缺失内容
- 改进排版

### 添加 FAQ

- 常见问题
- 解决方案

### 翻译

- 将文档翻译为其他语言
- 创建 `README.zh-CN.md` 等

## 行为准则

请遵循 [行为准则](https://github.com/wzhdgithub/GhostLock/blob/main/CODE_OF_CONDUCT.md) 中的规定：

- 尊重所有贡献者
- 提供建设性的反馈
- 专注于技术讨论
- 遵守社区规范

## 获取帮助

- 在 [GitHub Issues](https://github.com/wzhdgithub/GhostLock/issues) 提问
- 查看 [快速开始]({{ '/quickstart' | relative_url }})
- 查看 [使用指南]({{ '/usage' | relative_url }})
- 参考 [内部机制]({{ '/internals' | relative_url }})

## 致谢

感谢所有为 GhostLock 项目做出贡献的人！

---

**作者：** wzh  
**联系：** yjhsbwssg@163.com  
**项目：** https://github.com/wzhdgithub/GhostLock
