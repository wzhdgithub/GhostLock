import re, sys

KALL = r"D:\内核编译\extracted\kallsyms_ksym.txt.kallsyms"
BASE = 0xffffffc080000000

symbols = {}
with open(KALL, encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 3:
            addr = int(parts[0], 16)
            typ = parts[1]
            name = parts[2]
            if addr > 0:
                symbols.setdefault(name, (addr, typ))

print(f"total symbols: {len(symbols)}")

def find_exact(name):
    return symbols.get(name)

def find_substr(frag, exclude=()):
    out = []
    for name, (addr, typ) in symbols.items():
        if frag in name and all(e not in name for e in exclude):
            out.append((name, addr, typ))
    return sorted(out, key=lambda x: x[1])

SYMS = [
    "init_task", "init_cred", "init_uts_ns", "empty_zero_page", "root_task_group",
    "selinux_state", "kptr_restrict", "selinux_blob_sizes", "kmalloc_caches",
    "anon_pipe_buf_ops", "nfulnl_logger", "sysctl_bootid", "loggers",
    "configfs_bin_read_iter", "configfs_bin_write_iter", "copy_splice_read",
    "noop_llseek", "security_hook_heads", "ashmem_misc", "_stext", "_etext",
    "_edata", "_end",
]

print("\n=== exact symbols ===")
for s in SYMS:
    hit = find_exact(s)
    if hit:
        addr, typ = hit
        print(f"{s:<32} {typ} {addr:016x}  off=0x{addr-BASE:08x}")
    else:
        # substring search
        subs = find_substr(s)
        if subs:
            print(f"{s:<32} (substr)")
            for name, addr, typ in subs[:6]:
                print(f"    {name:<60} {typ} {addr:016x} off=0x{addr-BASE:08x}")
        else:
            print(f"{s:<32} NOT FOUND")

print("\n=== ashmem rust fops ===")
for frag in ["ashmem_rust6Ashmem", "6Ashmem"]:
    hits = [x for x in find_substr(frag) if "toggle" not in x[0].lower()]
    print(f"frag={frag}: {len(hits)} hits")
    for name, addr, typ in hits[:40]:
        print(f"    {name:<70} {typ} {addr:016x} off=0x{addr-BASE:08x}")

print("\n=== security_hook_active ===")
hits = find_substr("security_hook_active")
for name, addr, typ in hits[:20]:
    print(f"    {name:<70} {typ} {addr:016x} off=0x{addr-BASE:08x}")

print("\n=== selinux_state nearby (enforcing?) ===")
hits = find_substr("selinux")
for name, addr, typ in hits[:20]:
    print(f"    {name:<70} {typ} {addr:016x} off=0x{addr-BASE:08x}")
