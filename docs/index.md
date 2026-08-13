---
title: 项目介绍
description: GhostLock - CVE-2026-43499 futex PI 栈 UAF 本地提权漏洞利用
---

## 漏洞概述

GhostLock 是一个针对 CVE-2026-43499 漏洞的本地提权利用工具。该漏洞存在于 Linux 内核的 futex PI（优先级继承）机制中，通过 `pselect()` 系统调用触发的栈 UAF（Use-After-Free）可以实现任意内核内存写入，最终获得 root 权限并禁用 SELinux。

### 影响范围

- **漏洞类型：** futex PI 栈 UAF
- **影响内核：** Linux 6.1 ~ 6.12（Android GKI）
- **利用效果：** 本地提权 + SELinux 禁用
- **要求：** ADB 连接（USB 调试已开启）

### 支持的设备

| 设备 | 内核版本 | 状态 |
|------|----------|------|
| OPPO Find X8 (MT6991) | 6.6.118-android15 | ✅ 已适配 |
| OnePlus Ace 6T | 6.1.x | ✅ 已验证 |
| OnePlus 15 | 6.1.x | ✅ 已验证 |
| OnePlus Pad 2 | 6.1.x | ✅ 已验证 |
| Realme RMX5070 | 6.1.x | ✅ 已验证 |

## 工作原理

### 漏洞触发路径

```
用户空间 → pselect() → 内核栈上分配 rt_mutex_waiter
                      → futex PI 操作触发 waiter 释放
                      → 释放后的 waiter 内存被 fd_set 操作重用
                      → 通过精心构造的 fd_set 数据控制 waiter 字段
                      → rb_erase() 触发任意内核内存写入
```

### 利用链详解

1. **漏洞触发：** 通过 `pselect()` + futex PI 竞争释放内核栈上的 `rt_mutex_waiter`
2. **内存布局控制：** 用 `pipe_buffer` 喷射内核堆，构造 fake `rt_mutex_waiter`
3. **任意写入：** 利用 `rb_erase()` 的树操作，将控制的指针写入目标地址
4. **提权路径：** 
   - 修改 `cred` 结构体：uid/gid → 0，capabilities → 全部开启
   - 禁用 SELinux：`selinux_state.enforcing` → 0
5. **验证：** 重新扫描 `ashmem_fops` 确认 CFI 完整性

## 快速开始

### 编译

```bash
# 设置 NDK 路径
export ANDROID_NDK_HOME=/path/to/android-ndk-r27c

# 编译
make
```

### 使用

```bash
# 推送到手机
adb push ghostlock /data/local/tmp/
adb shell chmod 755 /data/local/tmp/ghostlock

# 运行
adb shell /data/local/tmp/ghostlock
```

## 相关链接

- [GitHub 仓库](https://github.com/wzhdgithub/GhostLock)
- [漏洞分析]({{ '/vulnerability' | relative_url }})
- [利用原理]({{ '/exploitation' | relative_url }})
- [使用指南]({{ '/usage' | relative_url }})

## 完整文档

### 快速开始

- [快速开始]({{ '/quickstart' | relative_url }}) - 5 分钟内开始使用 GhostLock
- [编译指南]({{ '/compilation' | relative_url }}) - 从源代码编译 GhostLock
- [工具脚本]({{ '/tools' | relative_url }}) - BTF 分析和 kallsyms 提取工具

### 技术文档

- [漏洞分析]({{ '/vulnerability' | relative_url }}) - CVE-2026-43499 漏洞的详细分析
- [利用原理]({{ '/exploitation' | relative_url }}) - 漏洞利用的技术原理
- [内部机制]({{ '/internals' | relative_url }}) - GhostLock 内部工作原理

### 设备支持

- [支持的设备]({{ '/devices' | relative_url }}) - 已适配的设备列表
- [添加新设备]({{ '/add-device' | relative_url }}) - 为 GhostLock 添加新设备支持

### 社区

- [贡献指南]({{ '/contributing' | relative_url }}) - 如何为项目做出贡献
- [更新日志]({{ '/changelog' | relative_url }}) - 版本历史和更新记录
- [安全政策]({{ '/security' | relative_url }}) - 安全漏洞报告指南
- [行为准则]({{ '/code-of-conduct' | relative_url }}) - 社区行为规范
