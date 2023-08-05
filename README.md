# 説明

Orbital Coreの代替を目指すプロジェクト

## 必要ライブラリ

```sh
pip install pyautogui
pip install pyserial
pip install keyboard
```

## プロトコル

※本家ソフトウェアの利用規約にてプロトコルの解析が禁止されているため、
以下の参考リンクの情報をもとに作成した。
[参考リンク](https://qiita.com/kame404/items/deaf7c066b6a3e82b1d4)

### ジョイスティック

`JSX@Y@;`
の形式
`@`には0から255までの値が1バイトで出力される。

### ジョイスティックのスイッチ

右に1クリック回転の場合、`RE-R;`、
左に1クリック回転の場合、`RE-L;`、
ボタン押下の場合、`RC4=@;`
`@`は押下した際に`1`、離上した場合に`0`となる。
ただし、離上は複数回出力されることもあるので注意

### リングスイッチ

`SW*=@;`

`*`はスイッチの位置を指し、USB接続箇所を北として、西から時計回りに`1,2,3,4,5,6,7,8`が入る
`@`は押下した際に`1`、離上した場合に`0`となる。
ただし、離上は複数回出力されることもあるので注意
