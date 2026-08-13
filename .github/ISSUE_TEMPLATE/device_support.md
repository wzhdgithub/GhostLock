---
name: 设备支持请求
about: 请求添加对新设备的支持
title: '[DEVICE] '
labels: device-support
assignees: wzhdgithub
---

## 设备信息

- **设备型号：** [例如: Xiaomi 14]
- **制造商：** [例如: Xiaomi]
- **芯片组：** [例如: Snapdragon 8 Gen 3]
- **内核版本：** [例如: 6.1.43-android14-11-gc7f4e2c]
- **Android 版本：** [例如: Android 14]

## 已提取的信息

请提供你已经提取的信息：

- [ ] kallsyms 符号表
- [ ] BTF 信息（task_struct, cred, file_operations 等）
- [ ] 物理内存布局
- [ ] 内核镜像（boot.img）

### kallsyms 符号表

```
在这里粘贴 kallsyms 符号表
```

### BTF 信息

```
在这里粘贴 BTF 信息
```

### 物理内存布局

- **PAGE_OFFSET：** [例如: 0xffffffc000000000]
- **PHYS_OFFSET：** [例如: 0x40000000]
- **KIMAGE_TEXT_BASE：** [例如: 0xffffffc080000000]

## 测试结果

如果你已经尝试过 exploit，请描述结果：

- [ ] 成功获取 root
- [ ] 遇到错误（请描述）
- [ ] 设备重启
- [ ] 其他（请描述）

## 其他信息

添加任何其他有助于添加设备支持的信息。
