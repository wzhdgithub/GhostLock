import struct

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

WANT = {
    "thread_info","__state","saved_state","stack","usage","flags","ptrace","on_cpu",
    "wake_entry","wakee_flips","wakee_flip_decay_ts","last_wakee","recent_used_cpu",
    "wake_cpu","on_rq","static_prio","normal_prio","rt_priority","se","rt","dl",
    "sched_class","sched_info","policy","nr_cpus_allowed","cpus_ptr","cpus_mask",
    "migration_disabled","mm","active_mm","vmacache","exit_state","exit_code",
    "exit_signal","pdeath_signal","pid","tgid","real_parent","parent","children",
    "sibling","group_leader","ptraced","ptrace_entry","thread_group","thread_node",
    "vfork_done","set_child_tid","clear_child_tid","utime","stime","gtime","prev_cputime",
    "nvcsw","nivcsw","min_flt","maj_flt","fs_excl","start_time","start_boottime","mm_security",
    "maj_flt_security","cpu","sched_inherit_cpus_allowed","cpu_allowmask","real_cred",
    "cred","comm","nameidata","sysvsem","sysvshm","last_switch_count","fs","files",
    "signal","sighand","blocked","real_blocked","saved_sigmask","pending","sas_ss_sp",
    "sas_ss_size","sas_ss_flags","task_works","rcu","rcu_users","wake_q","pi_lock",
    "pi_waiters","pi_top_task","pi_blocked_on","blocked_on","task_work","futex_exit_mutex",
    "futex_state","ptrace_message","last_siginfo","ioac","acct_rss_mem1","acct_vm_mem1",
    "acct_timexpd","memcg_oom_gfp_mask","memcg_in_oom","memcg_oom_order","memcg_nr_pages_over_high",
    "user","ucounts","ucounts_list","memory_failure","cpuset_mem_spread_rotor","cgroups","cgroup_list",
    "cg_list","no_cgroup_migration","robust_list","compat_robust_list","pi_state_cache",
    "perf_event_mutex","perf_event_list","numa_faults","numa_faults_locality","total_numa_faults",
    "numa_faults_locality_mem","numa_group","seccomp","parent_exec_id","self_exec_id",
    "alloc_lock","reclaim_state","backing_dev_info","io_context","capture_control","ptrace_bp_refcnt",
    "oom_reaper_list","rcev","android_kabi_reserved5","android_kabi_reserved6","android_kabi_reserved7",
    "android_kabi_reserved8","thread","address_limit","thread_info","scs_base","scs_sp","scs_alloc",
    "pending_lock","lazy_pending","timer_slack_ns","default_timer_slack_ns","sysvshm_list",
    "sysvsem_undo_list","sysvsem_remove_list","posix_timers","posix_cputimers","posix_cputimers_work",
    "task_ctx_info","bpf_ctx","bpf_stuff","bpf_uid_gid_map","bpf_rtable","faults_disabled_mapping",
    "faults_disabled","faults_disabled_0","faults_disabled_1","faults_disabled_2","faults_disabled_3",
    "faults_disabled_4","faults_disabled_5","faults_disabled_6","faults_disabled_7","faults_disabled_8",
    "temporal_control","temporal_state","temporal_count","build_id","audit_utime","audit_stime",
    "audit_arch","security","secid","crypto","voluntary_ctx_switch_count","nonvoluntary_ctx_switch_count",
    "sched_remote_wakeup","sched_contributes_to_load","sched_migrated","in_iowait","in_user_fault",
    "in_eventfd","frozen","arch_irq_work_signal","switch_type","death_signal","wakeup_idle",
    "wake_up_klogd","nrcpuset","task_dirty","mm_released","preferred_on_cpu","last_switch_count",
    "ss_off","resolve_stack","thr_preempt_scan","thr_fork_scan","thr_cpu_affinity",
    "ne_pud_present","ne_pmd_present","ne_pte_present","signal_group_exit","frozen_group_exit",
    "exit_signaled","exit_killed","exit_mm_released","is_robust","restore_sigmask","pid_reaped",
    "user_work","sched_core_control","sched_core_task_meta","sched_core_contributor",
    "sched_core_nominate","sched_core_migrating","sched_core_sched_group","reused_sibling",
    "reused_sibling_cnt","sched_core_idle","task_group","thread_group_node","blocked_on",
    "np_min","np_max","unsafe_fp_flags","placed_on_cpu","task_rq","cpu_ms_affinity",
    "of_data","oflags","nof_cpus","of_prio","of_ramp","of_boost","of_freq",
    "throttle_disk","set_prio","set_normal_prio","ctl","cpu_time","flags_prs",
}
for t in types:
    if t['kind'] == 4 and t['name'] == 'task_struct':
        print(f"=== task_struct tid={t['tid']} size={t['size']} vlen={t['vlen']} kflag={t['kflag']}")
        for i, m in enumerate(t['extra']['members']):
            b = m[2] // 8
            sfx = f" size={m[3]}" if m[3] else ""
            print(f"  [{i:3}] {m[0]:<34} off=0x{b:04x}{sfx} tid={m[1]}")
        break