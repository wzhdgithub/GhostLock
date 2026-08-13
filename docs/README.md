---
layout: default
title: GhostLock - CVE-2026-43499 本地提权漏洞利用
---

# GhostLock

## 漏洞概述

**CVE 编号：** CVE-2026-43499  
**漏洞类型：** futex PI（优先级继承）栈 UAF（Use-After-Free）  
**影响范围：** Linux 内核 6.1 ~ 6.12（Android GKI）  
**利用效果：** 本地提权 + SELinux 禁用，获取 root shell

## 工作原理

### 漏洞触发路径

```
用户空间 → pselect() → 内核栈上分配 rt_mutex_waiter
                      → futex PI 操作触发 waiter 释放
                      → 释放后的 waiter 内存被 fd_set 操作重用
                      → 通过精心构造的 fd_set 数据控制 waiter 字段
                      → rb_erase() 触发任意内核内存写入
```

### 利用链

1. **漏洞触发：** 通过 `pselect()` + futex PI 竞争释放内核栈上的 `rt_mutex_waiter`
2. **内存布局控制：** 用 `pipe_buffer` 喷射内核堆，构造 fake `rt_mutex_waiter`
3. **任意写入：** 利用 `rb_erase()` 的树操作，将控制的指针写入目标地址
4. **提权路径：** 
   - 修改 `cred` 结构体：uid/gid → 0，capabilities → 全部开启
   - 禁用 SELinux：`selinux_state.enforcing` → 0
5. **验证：** 重新扫描 `ashmem_fops` 确认 CFI 完整性

## 支持的设备

| 设备 | 内核版本 | 状态 |
|------|----------|------|
| OPPO Find X8 (MT6991) | 6.6.118-android15 | ✅ 已适配 |
| OnePlus Ace 6T | 6.1.x | ✅ 已验证 |
| OnePlus 15 | 6.1.x | ✅ 已验证 |
| OnePlus Pad 2 | 6.1.x | ✅ 已验证 |
| Realme RMX5070 | 6.1.x | ✅ 已验证 |

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

## 文档

- [完整文档](https://github.com/wzhdgithub/GhostLock/blob/main/README.md)
- [贡献指南](https://github.com/wzhdgithub/GhostLock/blob/main/CONTRIBUTING.md)
- [安全政策](https://github.com/wzhdgithub/GhostLock/blob/main/SECURITY.md)
- [更新日志](https://github.com/wzhdgithub/GhostLock/blob/main/CHANGELOG.md)

## 许可证

本项目采用 [MIT 许可证](https://github.com/wzhdgithub/GhostLock/blob/main/LICENSE)。

## 联系方式

- **作者：** wzh
- **邮箱：** yjhsbwssg@163.com
- **GitHub：** https://github.com/wzhdgithub
