revdep-rebuildでlibstdc++.so.*に依存したバイナリを探す方法
==========================================================

:date: 2014-11-09 18:59
:slug: revdep-rebuild-libstdcxx
:lang: ja
:summary: revdep-rebuild -L <ライブラリ名>の<ライブラリ名>は正規表現として解釈される。

Gentoo Linuxでlibstdc++.so.6に依存したバイナリを含むパッケージをまとめてリビルドしたい場合はrevdep-rebuildが利用できる。しかし、次のコマンドは意図したように動作しない。::

    revdep-rebuild -L libstdc++.so.6

なぜなら、ライブラリ名は正規表現として解釈されるからだ。正しくは次の通り。::

    revdep-rebuild -L 'libstdc\+\+.so.6'

libstdc++のABI非互換によって問題が起きたと思しき場合の応急処置として必要となったのでメモ。
