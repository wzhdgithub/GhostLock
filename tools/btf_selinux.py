import struct
IMG = r'D:\内核编译\extracted\Image.bin'
data = open(IMG, 'rb').read()
btf = data.find(b'\x9f\xeb\x01\x00', 0x1000)
magic, version, flags, hdr_len, type_off, type_len, str_off, str_len = struct.unpack_from('<HBBIIIII', data[btf:], 0)
types_b = data[btf+hdr_len+type_off : btf+hdr_len+type_off+type_len]
strs_b  = data[btf+hdr_len+str_off : btf+hdr_len+str_off+str_len]

def sname(off):
    if off == 0 or off >= len(strs_b): return ''
    end = strs_b.find(b'\x00', off)
    return strs_b[off:end].decode('utf-8', 'replace')

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
    if kind in (4, 5):
        members = []
        boff = off + 12
        for i in range(vlen):
            m_name, m_type, m_raw = struct.unpack_from('<III', types_b, boff); boff += 12
            m_off = (m_raw & 0xffffff) if kflag else m_raw
            members.append((sname(m_name), m_type, m_off))
        extra['members'] = members
        end += 12 * vlen
    elif kind == 1: end += 4
    elif kind == 3: end += 12
    elif kind == 6: end += 8 * vlen
    elif kind == 13: end += 8 * vlen
    elif kind == 14: end += 4
    elif kind == 15: end += 12 * vlen
    elif kind == 17: end += 4
    types.append({'kind': kind, 'name': name, 'size': size_type, 'extra': extra, 'vlen': vlen})
    off = end
    idx += 1

want = ('selinux_state', 'selinux_cred', 'security_hook_heads', 'selinux_blob_sizes',
        'cap_capable_active_enu', 'mm_struct', 'rt_mutex_waiter')
for t in types:
    if t['kind'] == 4 and t['name'] in want:
        print("=== %s size=0x%x vlen=%d kflag? " % (t['name'], t['size'], t['vlen']))
        for m in t['extra']['members']:
            print("    %-36s off=0x%04x" % (m[0], m[2]//8))