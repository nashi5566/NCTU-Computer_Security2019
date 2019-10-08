# HW0x01 Writeup

![](https://i.imgur.com/i7kOkzf.png)

當程式開始執行時，會看到題目會提醒使用者如果年份不是 1985 的話，之後可能會有些問題。

![](https://i.imgur.com/svFaV9r.png)

可以看到第一個 for loop 中，會對輸入的字串跟後方一串運算後的數字做 XOR ，隨後檢查是否與`byte408008` 的內容符合，如果檢查通過，就會進入下個 for loop ，將輸入的字串跟`byte_40801c` 做 XOR 後，出來的便會是我們要的 Flag 。而這個 `dword_40c040` 其實就是 `time()` 回傳的 local time 的年份。

而觀察這個運算式，可以知道如果年份是 1985 ，那麼這個運算的結果就會是 `2*(1985+63) + 127 + (debugger attached flag)` ，Hex 值會是 `0x17F + ()` ，ASCII 編碼表中的 printable character 範圍是從 `32` 到 `7E` 。而去 `.data` 段找有沒有 `byte_408008` 的內容，可以看到裡面有 19 個 element ：

![](https://i.imgur.com/IcRqEkr.png)

這些 element 都是 32-bit 的值，然後我猜測前面得到的值最後加上 `()` 之後應該會小於 `0x7F` ，因為如果是 `0x100` 的話，做 XOR 會超過 ASCII 的 printable 的範圍。於是我嘗試性的先用 0x7F 跟 `byte_408008` 做 XOR ，發現結果是 `blog.30cm.tw/./././` ，剛好是講師的網站的網址。ONLY YOU~ (　◜◡‾)

![](https://i.imgur.com/PpqppAI.png)


認知到年份一定要是 1985 的原因之後，查閱了`localtime()`，因為 `time.h` 中時間的計算是從 1900/01/01 以後開始，所以可以看到 0x00401649 將 `0x76C` ，就是 1900 加到 `EAX` 回傳年份，於是將 `ADD` 這個步驟 patch 成 `ADD EAX, 74A`，年份就會是 1985 而不是 2019 了。

![](https://i.imgur.com/0bsqbEV.png)
![](https://i.imgur.com/qKbGghO.png)

隨後改完年份以後，可以看到 `0x00401702` 的部份跟 `0x7C1` 做比較，也就是 1985 ，年份不對的話會出現警告的句子。這邊 patch 掉之後，就不會看到這句話了。

![](https://i.imgur.com/ENuUkLo.png)
![](https://i.imgur.com/3at2Uck.png)

接著繼續往下，可以看到判斷 Time Machine Guarder 的狀態的是看在 `EBP-20` 裡的值。

![](https://i.imgur.com/vgz1hPo.png)
![](https://i.imgur.com/EvhJe7P.png)

比較 DS:[EAX+2] 裡是否為 0 ，如果是 0 就跳到 `0x00401727` ([SAFE])，這邊可以看到在 `AL` 裡的是 `0xF0` 。因為還沒進行到後面運算的部份，為了保險起見，我還是將這裡 patch 掉，直接 `JMP` 到 [SAFE] 去。

![](https://i.imgur.com/LUQzYAP.png)

接著輸入剛剛推測出來的 `blog.30cm.tw/./././` 的 password 之後往下走，可以看到這裡又再次使用了 DS:[EAX+2] 的值，將他移到 EAX 中跟 `0x7F` 相加，可以知道前面的 `()` 的值就是 `0xF0` 。

![](https://i.imgur.com/e4RKjwP.png)
![](https://i.imgur.com/Rdk4GHa.png)

但前面已經測出來必須跟 `0x7F` 做 XOR 出來的結果才能夠通過第一關的檢查，所以這裡我直接將 `EAX` 清空成 0 。

![](https://i.imgur.com/9g7WmcK.png)

就能看到接下來的檢查 ，`AL` 跟 `DL` 都會是一樣的。

![](https://i.imgur.com/XSjNItX.png)

接著就能看到 Flag 了：

![](https://i.imgur.com/zO6SHyt.png)






