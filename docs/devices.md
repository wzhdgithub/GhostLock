---
title: 支持的设备
description: GhostLock 支持的设备列表和内核版本
---

## 支持状态说明

| 状态 | 说明 |
|------|------|
| <span class="status-supported">✅ 已适配</span> | 已有完整的设备条目，偏移量已验证 |
| <span class="status-testing">🧪 测试中</span> | 有设备条目但尚未在真机验证 |
| <span class="status-planned">📋 计划中</span> | 已了解设备信息但尚未创建设备条目 |

## 已适配设备

### OPPO Find X8

| 属性 | 值 |
|------|-----|
| **芯片组** | Dimensity 9400 (MT6991) |
| **内核版本** | 6.6.118-android15-8-gebdfad32d749-ab15099304-4k |
| **Android 版本** | 15 |
| **页大小** | 4K |
| **VA_BITS** | 39 |
| **状态** | <span class="status-supported">✅ 已适配</span> |

**内核信息：**

- **KIMAGE_TEXT_BASE：** `0xffffffc080000000`
- **PAGE_OFFSET：** `0xffffffc000000000`
- **PHYS_OFFSET：** `0x40000000`
- **KERNEL_PHYS_LOAD：** `0xC0000000`
- **DIRECT_MAP_END：** `0xffffffc400000000` (16GB RAM)

**关键符号偏移：**

| 符号 | 偏移 |
|------|------|
| init_task | 0x0211E280 |
| init_cred | 0x02130748 |
| init_uts_ns | 0x022A3448 |
| empty_zero_page | 0x0230F000 |
| root_task_group | 0x02317580 |
| selinux_enforcing | 0x02358EE0 |
| kptr_restrict | 0x0211BCF8 |
| selinux_blob_sizes | 0x0167AE90 |
| security_hook_heads | 0x0167A758 |
| kmalloc_caches | 0x0167A298 |
| anon_pipe_buf_ops | 0x0116E848 |
| ashmem_misc_fops | 0x0227C528 |
| ashmem_fops | 0x012EF5C0 |

### OnePlus Ace 6T

| 属性 | 值 |
|------|-----|
| **芯片组** | Snapdragon 8 Elite |
| **内核版本** | 6.1.x |
| **Android 版本** | 14/15 |
| **状态** | <span class="status-supported">✅ 已适配</span> |

### OnePlus 15

| 属性 | 值 |
|------|-----|
| **芯片组** | Snapdragon 8s Elite |
| **内核版本** | 6.1.x |
| **Android 版本** | 15 |
| **状态** | <span class="status-supported">✅ 已适配</span> |

### OnePlus Pad 2

| 属性 | 值 |
|------|-----|
| **芯片组** | Snapdragon 8 Gen 3 |
| **内核版本** | 6.1.x |
| **Android 版本** | 14/15 |
| **状态** | <span class="status-supported">✅ 已适配</span> |

### Realme RMX5070

| 属性 | 值 |
|------|-----|
| **芯片组** | Snapdragon 6 Gen 4 |
| **内核版本** | 6.1.x |
| **Android 版本** | 14 |
| **状态** | <span class="status-supported">✅ 已适配</span> |

## 设备支持矩阵

### 芯片组支持

| 芯片组 | 厂商 | 状态 |
|--------|------|------|
| Dimensity 9400 (MT6991) | MediaTek | ✅ 已适配 |
| Snapdragon 8 Elite | Qualcomm | ✅ 已适配 |
| Snapdragon 8s Elite | Qualcomm | ✅ 已适配 |
| Snapdragon 8 Gen 3 | Qualcomm | ✅ 已适配 |
| Snapdragon 6 Gen 4 | Qualcomm | ✅ 已适配 |

### 内核版本支持

| 内核版本 | 状态 |
|----------|------|
| 6.1.x | ✅ 已适配 |
| 6.6.x | ✅ 已适配（Find X8） |
| 6.12.x | 🧪 测试中 |

## 如何添加新设备

如果你的设备不在支持列表中，可以参考 [添加新设备]({{ '/add-device' | relative_url }}) 指南。

## 请求设备支持

你可以在 GitHub 上请求添加新设备支持：

1. 打开 [GitHub Issues](https://github.com/wzhdgithub/GhostLock/issues)
2. 点击 "New issue"
3. 选择 "设备支持请求" 模板
4. 填写设备信息
5. 提交

我们会在 1-2 周内回复你的请求。

## 相关链接

- [添加新设备]({{ '/add-device' | relative_url }})
- [编译指南]({{ '/compilation' | relative_url }})
- [工具脚本]({{ '/tools' | relative_url }})
