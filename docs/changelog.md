---
title: 更新日志
description: GhostLock 项目的版本历史和更新记录
---

## 版本历史

### v1.0.0 - 2026年8月13日

#### 功能特性

- **CVE-2026-43499** futex PI 栈 UAF 漏洞利用
- 支持 **Android GKI 内核** 6.1 ~ 6.12
- 支持 **5 款设备**：OPPO Find X8、OnePlus Ace 6T/15、OnePlus Pad 2、Realme RMX5070
- **运行时偏移表机制** - 自动适配不同内核版本
- **BTF 结构体解析** - 从 BTF 信息提取结构体偏移
- **kallsyms 符号提取** - 从内核镜像提取符号表
- **pipe_buffer 喷射** - 控制内核堆布局
- **文件操作劫持** - 劫持 ashmem 文件操作
- **提权** - 修改 cred 结构体
- **SELinux 禁用** - 禁用强制访问控制
- **CFI 绕过** - 绕过 Control Flow Integrity 保护
- **KASLR 绕过** - 处理内核地址随机化

#### 技术特性

- 使用 `pselect()` + futex PI 竞争触发 UAF
- 利用 `rb_erase()` 实现任意内核内存写入
- 通过 `fd_set` 数据控制释放的 waiter 内存
- 验证 `ashmem_fops` 地址确保 CFI 完整性

#### 设备支持

| 设备 | 内核版本 | 状态 |
|------|----------|------|
| OPPO Find X8 (MT6991) | 6.6.118-android15 | ✅ 已适配 |
| OnePlus Ace 6T | 6.1.x | ✅ 已验证 |
| OnePlus 15 | 6.1.x | ✅ 已验证 |
| OnePlus Pad 2 | 6.1.x | ✅ 已验证 |
| Realme RMX5070 | 6.1.x | ✅ 已验证 |

#### 更新内容

- 添加 OPPO Find X8 设备支持
- 添加 BTF 分析脚本集合
- 添加 kallsyms 提取工具
- 添加 Windows 编译支持
- 添加详细中文文档
- 修复 MM_STRUCT_SZ 编译期硬编码问题
- 修复 Windows 编译路径编码问题

## 后续版本计划

### v1.1.0（计划中）

- 添加更多设备支持
- 优化 exploit 稳定性
- 添加图形界面工具
- 完善错误处理

### v1.2.0（计划中）

- 支持无线 ADB
- 添加自动化测试
- 支持更多内核版本
- 性能优化

## 版本规范

本项目遵循语义化版本规范：

```
主版本.次版本.修订号

主版本: 不兼容的 API 修改
次版本: 向后兼容的功能性新增
修订号: 向后兼容的问题修正
```

## 相关链接

- [GitHub Releases](https://github.com/wzhdgithub/GhostLock/releases)
- [项目主页](https://github.com/wzhdgithub/GhostLock)
- [安全政策](/security)
