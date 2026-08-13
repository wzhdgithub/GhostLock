import struct, sys

IMG = r"D:\内核编译\extracted\Image.bin"
data = open(IMG, 'rb').read()
btf = data.find(b'\x9f\xeb\x01\x00', 0x1000)
magic, version, flags, hdr_len, type_off, type_len, str_off, str_len = struct.unpack_from('<HBBIIIII', data[btf:], 0)
types_b = data[btf+hdr_len+type_off : btf+hdr_len+type_off+type_len]
strs_b  = data[btf+hdr_len+str_off : btf+hdr_len+str_off+str_len]

def sname(off):
    if off == 0 or off >= len(strs_b): return ''
    end = strs_b.find(b'\x00', off)
    return strs_b[off:end].decode('utf-8', 'replace')

K_INT=1; K_PTR=2; K_ARRAY=3; K_STRUCT=4; K_UNION=5; K_ENUM=6; K_FWD=7
K_TYPEDEF=8; K_VOLATILE=9; K_CONST=10; K_RESTRICT=11; K_FUNC=12; K_FUNC_PROTO=13; K_VAR=14
K_DATASEC=15; K_FLOAT=16; K_DECL_TAG=17; K_TYPE_TAG=18; K_ENUM64=19

types = []
off = 0
idx = 0
while off < len(types_b):
    name_off, info, size_type = struct.unpack_from('<III', types_b, off)
    kind = (info >> 24) & 0x1f
    vlen = info & 0xffff
    kflag = (info >> 31) & 1
    name = sname(name_off) if name_off else ''
    extra = {}
    end = off + 12
    if kind == K_INT: end += 4
    elif kind in (K_PTR, K_CONST, K_VOLATILE, K_RESTRICT, K_TYPEDEF, K_TYPE_TAG): pass
    elif kind == K_ARRAY: end += 12
    elif kind in (K_STRUCT, K_UNION):
        members = []
        boff = off + 12
        for i in range(vlen):
            m_name, m_type, m_raw = struct.unpack_from('<III', types_b, boff); boff += 12
            if kflag:
                size_bits = m_raw >> 24
                m_off = m_raw & 0xffffff
            else:
                size_bits = None
                m_off = m_raw
            members.append((sname(m_name), m_type, m_off, size_bits))
        extra['members'] = members
        end += 12 * vlen
    elif kind == K_ENUM: end += 8 * vlen
    elif kind == K_ENUM64: end += 12 * vlen
    elif kind == K_FUNC_PROTO: end += 8 * vlen
    elif kind == K_VAR: end += 4
    elif kind == K_DATASEC: end += 12 * vlen
    elif kind == K_DECL_TAG: end += 4
    types.append({'kind': kind, 'name': name, 'size': size_type, 'extra': extra,
                  'vlen': vlen, 'kflag': kflag, 'tid': idx})
    off = end
    idx += 1

WANT = ['file_operations', 'cred', 'pipe_buffer', 'pipe_inode_info', 'linux_binfmt', 'miscdevice', 'thread_info', 'task_struct']
for t in types:
    if t['kind'] == 4 and t['name'] in WANT:
        print(f"=== {t['name']} tid={t['tid']} size=0x{t['size']:x} vlen={t['vlen']} kflag={t['kflag']}")
        for m in t['extra']['members']:
            print(f"    {m[0]:<36} off=0x{m[2]//8:04x} bits={m[2]&7} szbits={m[3]}")