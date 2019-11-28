# HW0x05 Writeup

![](https://i.imgur.com/6xrk6Og.png)



## Casino

首先發現輸入 `name` 的部分，`seed` 正好在 .data 段接續在 `name` 後方， read() 可以 overflow。
![](https://i.imgur.com/aWAP81E.png)

可以注意到 `seed` 後方 .data 段都不會用到，所以可以先蓋滿 `name` 、 `age` 、 `seed` 之後把 payload 放在後面，之後再找地方可以跳回來就可以。
payload 的前半目前是： `b"A"*16+p64(0)+b"A"*16`

`seed` 已知之後，寫一個 C code 來產 rand ：
```c=
int main(){
	srand(0);
	int r;

	for(int i = 0; i < 6; ++i){
		r = rand()%100;
		printf("%d\n", r);
	}
	return 0;
}
```
已知等等的 `lottery` 依序為：`83, 86, 77, 15, 93, 35`

接著進到 `casino` 後可以發現有兩次機會，以及 `Change number` 可以任意寫，可以往前蓋到 `GOT` 。

![](https://i.imgur.com/olhiO9N.png)

第一次隨意蓋，選擇蓋 `atoi` 結果第二輪就會炸掉，才意識到要選一個最後才會用到的，因為一次只能寫 4 bytes ，要將 address 分成兩次寫才行。

後來發現在 `0x602020` 有 `puts` ，可以發現其實沒有印 `You win!` 其實也不會怎樣，所以第一輪先故意輸入錯誤的 `guess` 不去觸發 `puts` ，並在 `Change number` 時改後半， offset 為 `-43`，因為 `read_init` 會經過 `atoi` ，所以輸入我們要跳的位置 0x602110 的十進位 `6299920` ；第二輪則輸入正確數字，並在 offset `-42` 輸入 `0` 將 address 前面的數字清掉，因為是正確的輸入會觸發 `call puts@plt`，接著就會跳到我們放 payload 的地方執行 shellcode 了。

Flag：`FLAG{0verf1ow_1n_ev3rywhere!}`