---
title: 工具脚本
description: GhostLock 提供的辅助工具脚本
---

## 工具概述

GhostLock 提供以下辅助工具：

- **BTF 分析脚本** - 解析内核 BTF 信息
- **kallsyms 提取** - 从内核镜像提取符号表
- **偏移量导出** - 导出设备偏移量

## BTF 分析脚本

### 前置条件

```bash
# 安装 Python 依赖
pip install elftools
pip install requests

# 需要提取的 vmlinux
# 使用 vmlinux-to-elf 从 boot.img 提取
python3 -m vmlinux_to_elf extracted/boot.img
```

### btf_task2.py

解析 `task_struct` 结构体的完整成员列表。

```bash
# 用法
python3 tools/btf_task2.py > task_struct.txt

# 输出示例
# === task_struct tid=318 size=4800 vlen=217 kflag=1
#   [  0] thread_info    off=0x0000 tid=322
#   [  1] __state        off=0x0030 tid=53
#   [  2] stack          off=0x0038 tid=23
#   [  3] usage          off=0x0040 tid=301
#   [  4] flags          off=0x0044 tid=53
#   [ 15] prio           off=0x0084 tid=13
#   [ 16] static_prio    off=0x0088 tid=13
#   [ 17] normal_prio    off=0x008c tid=13
#   [ 19] se             off=0x00c0 tid=325
#   [ 22] sched_class    off=0x0340 tid=355
#   [ 23] sched_task_group off=0x0348 tid=357
#   [ 52] tasks          off=0x0550 tid=38
#   [ 78] atomic_flags   off=0x05d8 tid=14
#   [ 80] pid            off=0x0618 tid=1164
#   [ 81] tgid           off=0x061c tid=1164
#   [ 83] real_parent    off=0x0628 tid=966
#   [113] real_cred      off=0x0818 tid=1175
#   [114] cred           off=0x0820 tid=1175
#   [116] comm           off=0x0830 tid=1176
#   [137] seccomp        off=0x08e8 tid=1218
#   [142] pi_lock        off=0x090c tid=66
#   [145] pi_waiters     off=0x0920 tid=350
#   [146] pi_top_task    off=0x0930 tid=315
#   [147] pi_blocked_on  off=0x0938 tid=1223
```

### btf_structs2.py

解析关键结构体的成员偏移。

```bash
# 用法
python3 tools/btf_structs2.py > structs.txt

# 支持的结构体
# - file_operations
# - cred
# - pipe_buffer
# - pipe_inode_info
# - linux_binfmt
# - miscdevice
# - thread_info
# - task_struct
```

### btf_selinux.py

解析 SELinux 相关的结构体。

```bash
# 用法
python3 tools/btf_selinux.py > selinux.txt

# 支持的结构体
# - selinux_state
# - selinux_cred
# - security_hook_heads
# - mm_struct
# - rt_mutex_waiter
```

### btf_mm.py

解析 mm_struct 结构体。

```bash
# 用法
python3 tools/btf_mm.py > mm.txt

# 输出示例
# === mm_struct tid=XXX size=0x4c0 vlen=XXX
#   [  0] mmap          off=0x0000
#   [  1] mm_rb         off=0x0008
#   ...
#   [N] cpu_bitmap     off=0x4c0
```

### btf_raw.py

输出原始 BTF 数据（用于调试）。

```bash
# 用法
python3 tools/btf_raw.py > raw.txt
```

## kallsyms 提取

### run_kallsyms_finder.py

从内核镜像中提取 kallsyms 符号表。

```bash
# 用法
python3 tools/run_kallsyms_finder.py extracted/Image.bin > kallsyms.txt

# 输出格式
# ffffffc080000000 T _text
# ffffffc080000000 T _stext
# ffffffc0800211e280 D init_task
# ffffffc08002130748 D init_cred
# ffffffc080022a3448 D init_uts_ns
```

### 查找关键符号

```bash
# 使用 grep 搜索
grep -E "(init_task|init_cred|selinux_state)" kallsyms.txt

# 计算偏移量
# 偏移 = 地址 - KIMAGE_TEXT_BASE
# 例如: init_task 偏移 = 0xffffffc0800211e280 - 0xffffffc080000000 = 0x211e280
```

## 偏移量导出

### dump_offsets.py

导出设备偏移量为 C 头文件格式。

```bash
# 用法
python3 tools/dump_offsets.py > offsets.h

# 输出示例
// OPPO Find X8 设备偏移量
#define KIMAGE_TEXT_BASE 0xffffffc080000000ULL
#define INIT_TASK_OFF   0x0211E280
#define INIT_CRED_OFF   0x02130748
#define SELINUX_ENFORCING_OFF 0x02358EE0
```

### extract_btf.py

从 vmlinux 提取 BTF 信息并转换为设备条目。

```bash
# 用法
python3 tools/extract_btf.py vmlinux

# 输出
# 生成 src/devices/<device>/offsets.h
```

## 完整工作流程

### 从 boot.img 到设备条目

```bash
# 1. 提取内核镜像
payload-dumper-go -o extracted firmware.bin
python3 -m vmlinux_to_elf extracted/boot.img

# 2. 提取 kallsyms
python3 tools/run_kallsyms_finder.py extracted/Image.bin > kallsyms.txt

# 3. 提取 BTF
python3 tools/btf_task2.py > task_struct.txt
python3 tools/btf_structs2.py > structs.txt
python3 tools/btf_selinux.py > selinux.txt
python3 tools/btf_mm.py > mm.txt

# 4. 生成偏移量
python3 tools/dump_offsets.py > offsets.h

# 5. 创建设备条目
mkdir -p src/devices/mydevice
cp findx8/offsets.h mydevice/
# 编辑 mydevice/offsets.h 填入正确的偏移量

# 6. 注册设备
# 编辑 src/devices/offsets.h
# 添加: #include "mydevice/offsets.h"

# 7. 编译
make

# 8. 测试
adb push ghostlock /data/local/tmp/
adb shell /data/local/tmp/ghostlock
```

## 相关链接

- [添加新设备](/add-device)
- [编译指南](/compilation)
- [支持的设备](/devices)
