---
layout: default
title: GhostLock
---

# GhostLock - CVE-2026-43499 本地提权漏洞利用

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/wzhdgithub/GhostLock.git
cd GhostLock

# 编译
make

# 推送到手机
adb push ghostlock /data/local/tmp/
adb shell chmod 755 /data/local/tmp/ghostlock

# 运行
adb shell /data/local/tmp/ghostlock
```

## 支持的设备

| 设备 | 内核版本 | 状态 |
|------|----------|------|
| OPPO Find X8 (MT6991) | 6.6.118-android15 | ✅ 已适配 |
| OnePlus Ace 6T | 6.1.x | ✅ 已验证 |
| OnePlus 15 | 6.1.x | ✅ 已验证 |
| OnePlus Pad 2 | 6.1.x | ✅ 已验证 |
| Realme RMX5070 | 6.1.x | ✅ 已验证 |

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
