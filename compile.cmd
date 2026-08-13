@echo off
chcp 65001 >nul
setlocal
set NDK=D:\内核编译\ndk\android-ndk-r27c
set BIN=%NDK%\toolchains\llvm\prebuilt\windows-x86_64
"%BIN%\bin\clang.exe" --target=aarch64-linux-android35 @build.rsp
exit /b %errorlevel%