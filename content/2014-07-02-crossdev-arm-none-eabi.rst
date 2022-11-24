Crossdevを使ってarm-none-eabiのツールチェインを用意する
=======================================================

:date: 2014-07-02 17:50
:slug: crossdev-arm-none-eabi
:lang: ja
:summary: ARM用のツールチェインが欲しくなったのでcrossdevで用意した。

::

    $ crossdev -s4 --without-headers -t arm-none-eabi

これだけでC・C++・Fortranのフロントエンドが用意される。楽。

このくらいの覚書でも書くようにしないと私はブログを日常的に書くことなどできないだろうということに今更気づいた。
