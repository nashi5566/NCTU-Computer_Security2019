# HW0x02 Writeup

這次作業雖然說沒辦法用 ida ，但我還是用 ida 做ㄌ....抱歉。

![](https://img.moegirl.org/common/0/06/在违法的边缘试探.jpg)


可以看到 ida 裡的 main function 裡分別會有兩個 function 分別對傳入的 `seed` 及 `flag` 做操作：

![](https://i.imgur.com/bND85ls.png)
（這裡有對一些名稱跟 type 做修改以方便閱讀） 

首先看到 `shellcode_decoder` 中，一開始先給了 `header` `IMAGE_DOS_HEADER` 所在的位置，第一關檢查 signature 是否正確，接著移動 `0x3c` 個 offset 來到 PE header 的位置，再來往下不斷的以 `0x28` 為單位移動到 `.data` 段的起點。
![](https://i.imgur.com/mda7R4i.png)

進入 `.data` 段之後，繼續往下找到放有第一個 element 是 `0xF` 的 array 的地方，這邊做的運算是將目前所在的 element 加上與自己相隔 `0x20` 個 offset 的 element 之後存起來，並繼續往下移動，直到這個 array 正中央的 element 與最後一個 element 相加之後才會離開迴圈，進行下個步驟。這裡可以發現，經過運算後產生的 element 總共有 32 個，正好與 `flag_checker` 一開始對長度檢查要求一致，所以推測這部分處理的事之後檢查 `flag` 所需要的東西，我們姑且稱為 `flag_cmp`。

![](https://i.imgur.com/893hUCu.png)

繼續往下，會持續移動到在 `.data` 段中，第一個 element 為 `0x45` 的 array 所在的位置。而看到 `flag_checker` 的最後呼叫的 function pointer 正是這段內容，而傳入的參數分別是先前我們得知的 array 的內容以及我們傳入的 flag ，因此這應該是一個處理過後可以變成能執行的 shellcode 的東西。

![](https://i.imgur.com/mCmVE6Z.png)

這裡可以看到找到起點 `0x45` 之後會對這段的所有 element 加上我們傳進去的 `seed` ，最後他就會變成之後 `flag_checker` 所呼叫的 shellcode 。

一個 function 的開始會是存當前 `frame` 的最頂端，因此開頭必須為 `\x55` 才會是 `push ebp`，因此這邊推測 `seed` 應為 16 。加上 `seed` 之後，後續的 `\x8b\xec\x51` 也的確是 `mov ebp, esp` 跟 `push ecx` 。整段完成計算之後，將 shellcode disassenble ，可以得到這個 shellcode 的 assembly 如下：

```=
push   ebp
mov    ebp,esp
push   ecx
mov    DWORD PTR [ebp-0x4],0x0
jmp    0x16
mov    eax,DWORD PTR [ebp-0x4]
add    eax,0x1
mov    DWORD PTR [ebp-0x4],eax
mov    ecx,DWORD PTR [ebp+0xc]
add    ecx,DWORD PTR [ebp-0x4]
movsx  edx,BYTE PTR [ecx]
test   edx,edx
je     0x48
mov    eax,DWORD PTR [ebp+0x8]
add    eax,DWORD PTR [ebp-0x4]
movsx  ecx,BYTE PTR [eax]
add    ecx,0x23
xor    ecx,0x66
cmpxchg ecx,edx
mov    eax,DWORD PTR [ebp+0xc]
add    eax,DWORD PTR [ebp-0x4]
movsx  ecx,BYTE PTR [eax]
cmp    edx,ecx
je     0x46
xor    eax,eax
jmp    0x4d
jmp    0xd
mov    eax,0x1
mov    esp,ebp
pop    ebp
ret
```

可以看到第 17 、 18 行，他會對 ecx 中的內容先做 `add 0x23` 再做 `xor 0x66` ，接著與 edx 的內容作比較。這邊可以從前面的 assembly 得知 ecx 是 我們傳進去的 `flag` （第一個參數）而 edx 則是先前 得到的 `flag_cmp` 。所以只要逆著將 `flag_cmp` 的內容先 `xor 0x66` 再 `sub 0x23` 就能得到真正的 flag 的 ascii code 。

`FLAG{y3s!!y3s!!y3s!!0h_my_g0d!!}`
