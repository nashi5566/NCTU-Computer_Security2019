# HW0x03 Writeup

## Unexploitable

![](https://i.imgur.com/3jWdu4t.png)

在網頁底下按 `F12` 看 `Request Header` ，可以看到回傳 Request 的 server 是 GitHub.com ，由此可知這個網頁是一個 git page ，而他的 `CNAME` 是指向 `unexploitable.kaibro.tw` 。

![](https://i.imgur.com/PnW8pY8.png)


所以 ping 這個 URL ，可以知道這個 git page 的帳號是 `Bucharesti` 。找到裡面有這個網頁的 github repo ，看一下他的 commit ，可以看到其中一條 commit 是刪掉某個檔案，裡面放的就是 flag。

![](https://i.imgur.com/FhVkM1I.png)

`FLAG{baby_recon_dont_forget_to_look_github_page}`

## Safe R/W

source code:
```php=
<?php

    if(isset($_GET['src']))
        highlight_file(__FILE__);

    function waf($s, $type) {
        if($type == 0) {
            if(stripos($s, ".") !== FALSE) die(bye());
            if(stripos($s, "/") !== FALSE) die(bye());
            if(stripos($s, "-") !== FALSE) die(bye());
        } else if($type == 1) {
            if(strlen($s) > 20) die(bye());
        } else {
            if(stripos($s, "ph") !== FALSE) die(bye());
        }
    }

    function bye() {
        header("Location: https://youtu.be/dQw4w9WgXcQ");
    }

    $sandbox = '/var/www/html/sandbox/' . @md5("kaibro" . $_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT']);
    @mkdir($sandbox);
    @chdir($sandbox);

    $f = $_GET{'f'};
    $c = $_GET{'c'};
    $i = $_GET{'i'};

    waf($f, 0, 1, 2, 3);
    waf($c, 1, 2, 3, 0);
    waf($i, 2, 3, 0 ,1);

    @system("mkdir " . escapeshellarg($sandbox . "/" . $f));
    @chdir($sandbox . "/" . $f);

    @file_put_contents("meow", $c);

    @chdir($sandbox);
    if(isset($i) && stripos(file_get_contents($i), '<') === FALSE) {
        echo "<div class='container'>";
        echo "<h2>Here is your file content:</h2>";
        @include($i);
        echo "</div>";
    }


    @chdir(__DIR__);
    $md5dir = @md5("kaibro" . $_SERVER['REMOTE_ADDR'] . $_SERVER['HTTP_USER_AGENT']);
    @system('rm -rf sandbox/' . $md5dir );

    echo "<hr>";
?>
```

可以看到 `40` 行的地方有對檔案內容做檢查，然而因為在 `@include` 之前的 critical section 並沒有做 lock 的機制保護寫與讀的動作，導致有 race condition 的可能，若在寫入一個預期的輸入後馬上寫入非法的內容，後者就可以藉此繞過檢查。

![](https://i.imgur.com/r0SonmX.png)

`FLAG{w3lc0me_t0_th3_PHP_W0r1d}`