---
title: 编译指南
description: 从源代码编译 GhostLock 的详细指南
---

## 环境要求

### 操作系统

GhostLock 支持以下操作系统：

- **Linux**（推荐）
- **macOS**
- **Windows**（通过编译脚本）

### 工具链

需要以下工具：

- **Android NDK r27c** 或更高版本
- **Clang**（NDK 自带）
- **Make**（Linux/macOS 可选）
- **Python 3.x**（用于 BTF 分析，可选）

## 安装 NDK

### 方法 A：Android Studio

1. 打开 Android Studio
2. 进入 SDK Manager
3. 选择 "SDK Tools" 标签
4. 勾选 "NDK (Side by side)"
5. 点击 "Apply" 安装

### 方法 B：命令行下载

```bash
# Linux/macOS
curl -O https://dl.google.com/android/repository/android-ndk-r27c-linux.zip
unzip android-ndk-r27c-linux.zip

# Windows
# 下载: https://dl.google.com/android/repository/android-ndk-r27c-windows.zip
# 解压到 D:\ndk\
```

### 方法 C：使用包管理器

```bash
# Ubuntu/Debian
sudo apt install android-sdk-platform-tools

# 或者使用 sdkmanager
sdkmanager "ndk;27.0.12077973"
```

## Linux/macOS 编译

### 设置环境变量

```bash
# 设置 NDK 路径
export ANDROID_NDK_HOME=/path/to/android-ndk-r27c

# 或者设置 ANDROID_NDK_ROOT
export ANDROID_NDK_ROOT=/path/to/android-ndk-r27c
```

### 编译

```bash
# 克隆仓库
git clone https://github.com/wzhdgithub/GhostLock.git
cd GhostLock

# 编译（自动检测 NDK）
make

# 指定 NDK 路径编译
make NDK_ROOT=/path/to/android-ndk-r27c

# 指定 API 级别
make API=35

# 清理
make clean
```

### 编译产物

编译成功后，会生成 `ghostlock` 二进制文件：

```bash
$ file ghostlock
ghostlock: ELF 64-bit LSB pie executable, ARM aarch64, version 1 (SYSV)

$ ls -la ghostlock
-rwxr-xr-x 1 user user 113216 Aug 13 12:16 ghostlock
```

## Windows 编译

### 方法 A：使用编译脚本

```cmd
:: 确保 NDK 已解压到 D:\ndk\
:: 运行编译脚本
compile.cmd

:: 或者直接调用 clang
D:\ndk\android-ndk-r27c\toolchains\llvm\prebuilt\windows-x86_64\bin\aarch64-linux-android35-clang.cmd ^
  --target=aarch64-linux-android35 ^
  -O2 -Wall -Wno-unused-parameter -Wno-sign-compare -Wno-unused-function ^
  -Isrc/core -Isrc/devices ^
  -DTARGET_CONFIG_H=\"target.h\" ^
  -fPIE -pie -pthread ^
  src/core/main.c src/core/util.c src/core/slide.c ^
  src/core/fops.c src/core/pipe.c src/core/root.c src/core/miniadb.c ^
  -o ghostlock
```

### 方法 B：使用 WSL

```bash
# 在 WSL 中
# 1. 安装 NDK
cd ~
wget https://dl.google.com/android/repository/android-ndk-r27c-linux.zip
unzip android-ndk-r27c-linux.zip

# 2. 设置环境变量
export ANDROID_NDK_HOME=~/android-ndk-r27c

# 3. 编译
cd /mnt/d/GhostLock
make
```

### 方法 C：使用 MSYS2/Git Bash

```bash
# 在 Git Bash 中
# 1. 设置 NDK 路径
export ANDROID_NDK_HOME=/d/ndk/android-ndk-r27c

# 2. 编译
make
```

## 直接编译命令

如果你不想使用 Makefile，可以直接使用以下命令：

```bash
# 设置 NDK 工具链路径
NDK=/path/to/android-ndk-r27c
CC=$NDK/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android35-clang

# 编译
$CC \
  --target=aarch64-linux-android35 \
  -O2 -Wall \
  -Wno-unused-parameter \
  -Wno-sign-compare \
  -Wno-unused-function \
  -Isrc/core \
  -Isrc/devices \
  -DTARGET_CONFIG_H=\"target.h\" \
  -fPIE -pie -pthread \
  src/core/main.c \
  src/core/util.c \
  src/core/slide.c \
  src/core/fops.c \
  src/core/pipe.c \
  src/core/root.c \
  src/core/miniadb.c \
  -o ghostlock
```

## 编译选项说明

### API 级别

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `API` | 35 | Android API 级别 |
| `NDK_ROOT` | 自动检测 | NDK 安装路径 |
| `NDK_CC` | 自动计算 | 编译器路径 |

### 编译器标志

| 标志 | 说明 |
|------|------|
| `-O2` | 优化级别 |
| `-Wall` | 启用所有警告 |
| `-fPIE` | 生成位置无关代码 |
| `-pie` | 生成可执行文件（PIE） |
| `-pthread` | 启用线程支持 |

## 验证编译

### 检查二进制

```bash
# 检查文件类型
file ghostlock

# 检查架构
readelf -h ghostlock | grep -E "(Class|Machine)"

# 检查动态链接
readelf -d ghostlock | grep -E "(NEEDED|FLAGS)"
```

### 检查符号

```bash
# 检查设备条目
nm ghostlock | grep -E "findx8|op15|ace6t"

# 检查关键函数
nm ghostlock | grep -E "(exploit|trigger|patch_cred)"
```

## 常见编译错误

### 错误 1：找不到 dirent.h

**原因：** 未正确设置 sysroot

**解决方案：**
```bash
# 确保使用 NDK 的 clang（自动设置 sysroot）
# 而不是系统 clang
$CC --target=aarch64-linux-android35
```

### 错误 2：TARGET_CONFIG_H 未定义

**原因：** 编译参数错误

**解决方案：**
```bash
# 确保传递正确的参数
-DTARGET_CONFIG_H=\"target.h\"
```

### 错误 3：链接失败

**原因：** 缺少 pthread 支持

**解决方案：**
```bash
# 添加 -pthread 标志
-pthread
```

### 错误 4：MM_STRUCT_SZ 未定义

**原因：** 设备条目未包含 mm_struct_sz 字段

**解决方案：**
```bash
# 在设备条目中添加
.mm_struct_sz=0x4C0,
```

## 交叉编译说明

### Android 架构

| 架构 | ABI | 编译器前缀 |
|------|-----|-----------|
| arm64-v8a | aarch64 | aarch64-linux-android |
| armeabi-v7a | arm | armv7a-linux-androideabi |
| x86_64 | x86_64 | x86_64-linux-android |

### 编译 32 位版本

```bash
# 设置 API 级别
make API=28

# 或者直接指定编译器
armv7a-linux-androideabi28-clang --target=armv7a-linux-androideabi28
```

## 相关链接

- [快速开始]({{ '/quickstart' | relative_url }})
- [工具脚本]({{ '/tools' | relative_url }})
- [添加新设备]({{ '/add-device' | relative_url }})
