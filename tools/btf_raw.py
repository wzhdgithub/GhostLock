import struct

IMG = r"D:\内核编译\extracted\Image.bin"
data = open(IMG, 'rb').read()
btf = data.find(b'\x9f\xeb\x01\x00', 0x1000)

def parse_btf(btf_data):
    magic, version, flags, hdr_len, type_off, type_len, str_off, str_len = struct.unpack_from('<HBBIIIII', btf_data, 0)
    return btf_data[hdr_len+type_off : hdr_len+type_off+type_len], btf_data[hdr_len+str_off : hdr_len+str_off+str_len]

types_b, strs_b = parse_btf(data[btf:])

def sname(off):
    if off == 0 or off >= len(strs_b): return ''
    end = strs_b.find(b'\x00', off)
    return strs_b[off:end].decode('utf-8', 'replace')

# Walk all types, find rt_mutex_waiter with raw info dump
wanted = b'rt_mutex_waiter'
tid = None
off = 0
while off < len(types_b):
    name_off, info, size_type = struct.unpack_from('<III', types_b, off)
    kind = (info >> 24) & 0x1f
    vlen = info & 0xffff
    kflag = (info >> 31) & 1
    name = sname(name_off)
    hdr_end = off + 12
    if kind in (4, 5):  # STRUCT/UNION
        if name == 'rt_mutex_waiter':
            tid = name_off
            print(f"struct rt_mutex_waiter at type-offset 0x{off:x} tid-regexp")
            print(f"  info=0x{info:08x} kind={kind} vlen={vlen} kflag={kflag} size={size_type}")
            mem_off = hdr_end
            for i in range(vlen):
                raw = types_b[mem_off:mem_off+16 if kflag else mem_off+12]
                if not kflag:
                    m_name, m_type, m_boff = struct.unpack_from('<III', types_b, mem_off)
                    print(f"  member[{i}] name_off={m_name} name='{sname(m_name)}' type={m_type} boff={m_boff} byte=0x{m_boff//8:x} raw={raw.hex()}")
                    mem_off += 12
                else:
                    m_name, m_type, m_boff, m_size = struct.unpack_from('<IIiI', types_b, mem_off)
                    print(f"  member[{i}] name_off={m_name} name='{sname(m_name)}' type={m_type} boff={m_boff} (0x{m_boff:x}) size={m_size} raw={raw.hex()}")
                    mem_off += 16
            break
    # advance
    if kind == 1: off = hdr_end + 4
    elif kind in (2,8,9,10,11,12,18): off = hdr_end
    elif kind == 3: off = hdr_end + 12
    elif kind in (4,5): off = hdr_end + (16*vlen if kflag else 12*vlen)
    elif kind == 6: off = hdr_end + 8*vlen
    elif kind == 7: off = hdr_end
    elif kind == 13: off = hdr_end + 8*vlen
    elif kind == 14: off = hdr_end + 4
    elif kind == 15: off = hdr_end + 12*vlen
    elif kind == 16: off = hdr_end
    elif kind == 17: off = hdr_end + 4
    elif kind == 19: off = hdr_end + 12*vlen
    else: off = hdr_end

if tid is None:
    print("rt_mutex_waiter not found")

# Also find the tree member type at tid 8994: dump it
def get_type_at(debug=False):
    # simpler: re-walk and print types whose index == 8994, 8995, 8947
    find = {8994, 8995, 8947, 53, 315}
    off = 0
    idx = 0
    res = {}
    while off < len(types_b):
        name_off, info, size_type = struct.unpack_from('<III', types_b, off)
        kind = (info >> 24) & 0x1f
        vlen = info & 0xffff
        kflag = (info >> 31) & 1
        name = sname(name_off)
        if idx in find:
            res[idx] = (kind, name, size_type, vlen, kflag, off)
        if kind == 1: off += 12 + 4
        elif kind in (2,8,9,10,11,12,18): off += 12
        elif kind == 3: off += 12 + 12
        elif kind in (4,5): off += 12 + (16*vlen if kflag else 12*vlen)
        elif kind == 6: off += 12 + 8*vlen
        elif kind == 7: off += 12
        elif kind == 13: off += 12 + 8*vlen
        elif kind == 14: off += 12 + 4
        elif kind == 15: off += 12 + 12*vlen
        elif kind == 16: off += 12
        elif kind == 17: off += 12 + 4
        elif kind == 19: off += 12 + 12*vlen
        else: off += 12
        idx += 1
    for k, v in sorted(res.items()):
        kind, name, size, vlen, kflag, off = v
        print(f"tid {k}: kind={kind} name='{name}' size={size} vlen={vlen} kflag={kflag} at 0x{off:x}")

get_type_at()