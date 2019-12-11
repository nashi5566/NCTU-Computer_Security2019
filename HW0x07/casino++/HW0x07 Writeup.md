# HW0x07 Writeup

![](https://i.imgur.com/cp2ADlA.png)


## Casino++

### 思路 1
一開始想試著將 rop chain 堆在 `name` 之後的 .data 段，利用原先已知的 GOT hijacking 的洞，想辦法跳到 rop chain 所在的位置。
但發現不可行，因為 GOT 的位置只有 8 bytes 可以使用，無法控制 ret 的位置。

### 思路 2
後來想到在 `read_chk` 中有機會碰到 rbp ，如果改掉 `stack_chk` 在 GOT 的位置，這樣即便蓋到 canary 也不會讓程式停下來。
所以我將 `puts` 改為 `casino` 的位置，讓程式能夠無限的 loop ，就能繼續 IO ，更改 GOT 中的其他位置。
但後來發現 `read_init` 只讀 16 bytes ，距離 canary 及 ret address 還有 16 bytes ，塞再長的 payload 都永遠蓋不到。

### 思路 3
基於前面提到將 `puts` 改為 `casino` ，讓他能夠無限的 loop 之後，如果反覆修改 GOT ，像是程式中有使用到 `printf` ，那就可以將某個 fuction GOT 改成 `printf` 就有機會可以 leak libc ，再從已知的 libc.so 版本中的 offset 一起得到 `system` 的位置，這樣之後就可以將他寫在 GOT 中進而 get shell。

而如果要讓 `printf` 印出我們想要的東西，必須找到緊鄰 `call` 可以控 `rdi` 的地方，於是就找到了 `init` 中有對 `rdi`、 `rax` 做操作，`rsi` 又剛好被歸零，接著就會呼叫 `setvbuf` ，剛好可以改成 `printf` 而 `rdi` 取得的值是 GOT 中的內容，因此改 GOT 就能控到 `rdi`。而為了讓程式不要出錯， `stderr` 是唯一在程式正常運作下不會被呼叫到的，所以我將 `stderr` 改寫為 `libc_main_got` 的位置。

![](https://i.imgur.com/zAC0yKp.png)

接著，將 `puts` 改成 `init` 的位置，去執行 `init`，因為 leak libc 之後還有其他必須修改的地方，我將 `time` 改成 `casino` 的位置，以便之後繼續修改 GOT 。

取得 libc 的 base 之後，原本想用 one_gadget 找到的位置，寫在 `puts` 直接執行，但好像沒有辦法用。但因為 `rdi` 在 `init` 是可控的，所以在輸入 `name` 時，將 `/bin/sh` 一併蓋在後面 `0x602110` 的地方，修改 `stderr` 為 `0x602110` 再將 `setvbuf` 的 GOT 改為 `system` 就能得到 shell 了。

上面的文字解說有些繁雜，簡單來畫流程就像下面這張圖：

![](https://i.imgur.com/7spuLbS.png)

`FLAG{Y0u_pwned_me_ag4in!_Pwn1ng_n3v3r_di4_!}`
