repos.confに関するtips
======================

:date: 2016-12-02 00:00
:slug: tips-on-repos-conf
:lang: ja
:summary: repos.confについての簡単なまとめ

これは\ `Gentoo Advent Calendar 2016`_ 2日目に寄稿した文章です。

`Gentooは市民の義務`_\ 、皆さんご存知ですね？

はじめに
--------

最近のPortageでoverlayを追加するときにはrepos.confという設定ファイルを書くことになっています。このrepos.confについての情報はGentoo Wikiのいくつかのページに分散しています。主な文書は次の3つです。

* `Project:Portage/Sync <https://wiki.gentoo.org/wiki/Project:Portage/Sync>`_
* `/etc/portage/repos.conf <https://wiki.gentoo.org/wiki//etc/portage/repos.conf>`_
* `Overlay/Local overlay <https://wiki.gentoo.org/wiki/Overlay/Local_overlay>`_

この文章はこれらに書かれているrepos.confの機能からよく使うものを抜粋した覚書です。

repos.confをはじめる
--------------------

最新のGentoo Handbookにはrepos.confを前提とした説明が掲載されているので、指示通りにやれば問題ありません。

まだrepos.confに移行していない古い環境がある場合は、Portageを更新してから/etc/portage/repos.confディレクトリを作り、その中に/usr/share/portage/config/repos.confを適当な名前でコピーすればとりあえず動きます。

更にlaymanを使っている場合は、バージョン2.3以降のlayman（現時点ではunstable）に新しい機構に対応するためのsync-plugin-portageというUSEフラグがあるので、これを有効にしてから/etc/layman/layman.cfgのconf_typeをrepos.confにし、layman-updater -Rした後でlaymanのmake.confを削除します。

Gentoo treeの同期方法をrsyncからwebrsyncに切り替える
----------------------------------------------------

gentooリポジトリの設定部分でsync-typeをrsyncからwebrsyncに切り替えてsync-uriを削除すればemerge-webrsync相当の方法でGentoo treeを同期します。

webrsyncでダウンロードしてきたebuildツリーのアーカイブはOpenPGP鍵で署名されており、それを検証できるのがwebrsync方式の大きな利点ですが、検証のためには追加の手順が必要です。\ `Gentoo HandbookのFeatures <https://wiki.gentoo.org/wiki/Handbook:Parts/Working/Features>`_\ を参照してください。

Gentoo treeの同期方法をrsyncからgitに切り替える
-----------------------------------------------

gentooリポジトリの設定部分でsync-typeをrsyncからgitに切り替えてsync-uriを適当なリポジトリに変更すればGitでGentoo treeを同期します。

が、これはむしろ他のoverlayを使うときによく使っている気もします。

新しいoverlayを追加する
-----------------------

たとえばRust overlayを使いたくなったとき、laymanをインストールしていればいつも通りlayman -a rustすれば使えるようになりますが、laymanを使っていない場合は/etc/portage/repos.conf/rust.confで次のように書きます。

::

    [rust]
    location = /usr/local/overlay/rust
    sync-type = git
    sync-uri = https://github.com/gentoo/gentoo-rust.git

その後でsyncすれば使えるようになります。他のoverlayでも、どこにあってどの方法で同期するかによってsync-typeとsync-uriを調整すれば同じ手順で使えます。

crossdevを使う
--------------

Gentooにはクロスツールチェーンをインストールするのに便利なcrossdevというツールがあります。crossdevはtripletごとにカテゴリを作ってebuildをそこにコピーするので、専用のoverlayが必要になります。それは次のような手順で作ります。

::

    # mkdir -p /usr/local/overlay/crossdev/{profiles,metadata}
    # echo 'crossdev' > /usr/local/overlay/crossdev/profiles/repo_name
    # echo << EOF > /usr/local/overlay/crossdev/metadata/layout.conf
    masters = gentoo
    thin-manifests = true
    EOF
    # echo << EOF > /etc/portage/repos.conf/crossdev.conf
    [crossdev]
    location = /usr/local/overlay/crossdev
    masters = gentoo
    priority = 10
    auto-sync = no
    EOF
    # chown -R portage:portage /usr/local/overlay/crossdev

おわりに
--------

overlayごとに/etc/portage/repos.conf以下にファイルを置けばうまくやってくれる今の仕組みは私好みでいいなぁと思っています。

Happy emerging!

.. _Gentoo Advent Calendar 2016: http://www.adventar.org/calendars/1493
.. _Gentooは市民の義務: https://twitter.com/naota344/status/801896700470169600
