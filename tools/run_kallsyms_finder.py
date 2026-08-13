import sys, runpy, os
REPO = r"C:\Users\yjhsb\AppData\Local\Temp\opencode\vmlinux-to-elf"
sys.path.insert(0, REPO)
script = os.path.join(REPO, "vmlinux_to_elf", "scripts", "kallsyms_finder.py")
sys.argv = ["kallsyms_finder.py"] + sys.argv[1:]
runpy.run_path(script, run_name="__main__")