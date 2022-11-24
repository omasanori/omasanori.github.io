Icecreamの使い方メモ
====================

:date: 2015-01-26 19:43
:slug: how-to-use-icecream
:lang: ja
:summary: Icecream (icecc) の使い方についてメモしておいた。

とりあえずメモ程度。クロスコンパイルやってから整理する。

入れ方
------

::

    # echo 'sys-devel/icecream ~*' >> /etc/portage/package.accept_keywords
    # emerge sys-devel/icecream

使い方
------

/usr/libexec/icecc/binにPATHを通す。Portageでのみ使う場合はmake.confのPREROOTPATHに書けばいい。

ただし、PortageはCHOST込みの名前（例えばx86_64-pc-linux-gnu-gcc）でコンパイラを呼び出す。よって、先ほどの位置にそれらの名前で/usr/bin/iceccへのシンボリックリンクを置く。

クロスコンパイル
----------------

Portageでのみ使う場合はクロスコンパイラさえ配置してあれば先ほどの作業で問題なく動作するはず。今週試す。

Portage以外でも使う場合は先ほどとは逆に「単なるgccをCHOST付きの名前に置き換えてicecc越しに実行する」という細工をしないと各々のホストコンパイラでコンパイルしてリンク時にエラーを引き起こす。Gentoo Wikiのdistcc関連文書にうまいことやる方法が書かれているのでうまくやる。

問題
----

初回起動時にiceccdが死んでる問題があるがrestartするとうまくいく。これのおかげでIcecreamだけは手動で起動するようにしている。
