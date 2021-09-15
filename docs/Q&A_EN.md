中文: [Chinese](Q&A)

## Q1 Questions about the cross compilation tool chain

A：Please check the tool-chains PATH setting, such as

```shell
set RTT_EXEC_PATH=your_toolchains
os.environ['RTT_EXEC_PATH'] = r'your_toolchains'
scons -j 6  
```

## Q2 Compilation problems - conflicts of the function definitions about `sleep`

A:

```shell
> scons -j6
...
LINK rtthread.elf
d:/project/k210_third_tools/xpack-riscv-none-embed-gcc-8.3.0-1.2/bin/../lib/gcc/riscv-none-embed/8.3.0/../../../../riscv-none-embed/bin/ld.exe: build\packages\kendryte-sdk-v0.5.6\kendryte-standalone-sdk\lib\bsp\sleep.o: in function `usleep':
sleep.c:(.text.usleep+0x0): multiple definition of `usleep'; build\kernel\components\libc\compilers\common\unistd.o:unistd.c:(.text.usleep+0x0): first defined here
d:/project/k210_third_tools/xpack-riscv-none-embed-gcc-8.3.0-1.2/bin/../lib/gcc/riscv-none-embed/8.3.0/../../../../riscv-none-embed/bin/ld.exe: build\packages\kendryte-sdk-v0.5.6\kendryte-standalone-sdk\lib\bsp\sleep.o: in function `sleep':
sleep.c:(.text.sleep+0x0): multiple definition of `sleep'; build\kernel\components\libc\compilers\common\unistd.o:unistd.c:(.text.sleep+0x0): first defined here
collect2.exe: error: ld returned 1 exit status
scons: *** [rtthread.elf] Error 1
scons: building terminated because of errors.
```

