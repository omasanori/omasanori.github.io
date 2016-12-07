書ける！ebuild
==============

:date: 2016-12-08 01:00
:slug: writing-ebuild-crash-course
:lang: ja
:summary: まだebuildを書いたことがない人の背中を押すためのなにか。

これは\ `Gentoo Advent Calendar 2016`_ 7日目に遅刻した文章です。

はじめに
--------

Gentoo Linuxに限らず、Linuxディストリビューションの多くにはパッケージマネージャというアプリケーションがインストールされており、システムの構成を管理することができます。一度それに慣れてしまうと、一つ一つ自分でビルドしてインストールし、不都合が起きたら調整してから再度インストールするという原始的な管理方法は次第に苦痛になり、統一的なインターフェースでシステムを組み替えられる日々を謳歌し、そして壁に突き当たります。すなわち、欲しいソフトウェアをパッケージマネージャでインストールできないという壁に。

* そのソフトウェアのパッケージそのものが用意されていない
* インストールできるバージョンが欲しいバージョンとは異なる
* コンパイルオプションなどの違いで欲しい機能が組み込まれていない

具体的な悩みは場合によって様々です。いずれにせよ、欲しいソフトウェアをどのようにしてシステムに組み込むかは悩みどころです。昔ながらのやり方はシステムの更新で静かに破綻する危険性があり、パッケージを作るのは単なるconfigure && make && make installとは異なる手順を要します。

Gentooの場合、ebuildと呼ばれるテキストファイルにビルドやインストールに必要な手順を書くことでパッケージを作ることができます。幸いなことに、後述するeclassのおかげで、一般的な手順でインストールできるソフトウェアはebuildにソースコードの入手元URLなどの数行を書くだけで済むこともあります。

この文書はまだebuildを書いたことがないGentoo者の背中を押すために書かれたものです。

ebuildを書くまで
----------------

いくらebuildを書くのが簡単な場合もあるとはいえ、書かずに済むならその方が良いこともあります。また、実際にebuildを書く前にはちょっとした準備が必要ですし、書く上でのコツもあります。まずはその辺りのポイントを押さえていきます。

Gentooリポジトリにパッケージが本当にないのか？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

欲しいソフトウェアの名前が思ったような名前でないことは珍しくありません。Gentoo Hancbookではlspciコマンドのためにpciutilsパッケージをインストールしますが、それ以外にもそのような例は沢山あります。欲しいコマンドがライブラリの付属品だったり、名前にハイフンがあったりなかったり、名前に何かが付け足されていたり、パッケージが見つからない理由は様々です。

大抵、Gentooリポジトリにあるebuildは即興で書けるものよりもうまく書かれています。まずはemerge --search(desc)などによるGentooリポジトリの探索に少し時間を割きましょう。

既存のオーバレイで解決できないか？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

様々なソフトウェアと相互に依存する巨大なパッケージを作るのはGentooであっても（場合によってはGentooであるからこそ）容易なことではありません。Gentooリポジトリにebuildがなかったとしても、なんとか書かずに済ませられないか。もしかしたら、他の人が作ったオーバレイを使えるかもしれません。

オーバレイとは、主となるGentooリポジトリを補完するために作るebuildなどの集積所です。あなたがebuildを書くときにも、システムのどこかにオーバレイを用意して、そこにebuildを置きます。

Gentoo開発者もそうでない人も含めて、様々な人々がインターネット上にオーバレイを公開しており、その一部は\ `layman <https://wiki.gentoo.org/wiki/Layman>`_\ を通して容易にシステムへ組み込むことができます。例えば、Gentooリポジトリにはまだ入っていない新しいMonoをインストールしたい場合はDotnetプロジェクトに所属しているGentoo開発者が管理しているdotnetオーバレイをlaymanで組み込むことができます。

laymanで組み込めないオーバレイも自分でrepos.confを書けばシステムに組み込めます。手前味噌ではありますが、本アドベントカレンダー2日目の\ `repos.confに関するtips <http://omasanori.github.io/blog/2016/12/02/tips-on-repos-conf/>`_\ でこの辺りの話に少し触れています。

他の人が書いたオーバレイを使う際には、それらがGentooリポジトリとは異なることに注意してください。Gentooリポジトリとは管理方針が異なるでしょうし、そのオーバレイのebuildがよからぬことをしていないかどうかを十分多くの目が見張っていないかもしれません。

ローカルオーバレイを作る
~~~~~~~~~~~~~~~~~~~~~~~~

どうやらebuildを書くことになりそうだと思ったら、自分のebuildを置くローカルオーバレイを作りましょう。

今回は/usr/local/portageにomasanori-localという名前のオーバレイを作ることにします。

::

        # mkdir -p /usr/local/portage/{profiles,metadata}
        # echo 'omasanori-local' > /usr/local/portage/profiles/repo_name
        # echo << EOF > /usr/local/portage/metadata/layout.conf
        masters = gentoo
        thin-manifests = true
        EOF
        # echo << EOF > /etc/portage/repos.conf/local.conf
        [omasanori-local]
        location = /usr/local/portage
        masters = gentoo
        auto-sync = no
        EOF

skel.ebuildから始める
~~~~~~~~~~~~~~~~~~~~~

/usr/portageにはskel.ebuildという名前でebuildの骨組みが置かれています。このファイルを読むことでebuildにどのような事柄を記載すればよいかがわかります。実際にebuildを作る際もskel.ebuildをコピーしてから必要に応じて書き換えるとよいでしょう。

例えば、foobarのバージョン1.0.0をインストールするためのnet-misc/foobar-1.0.0というパッケージを作りたい場合はこのようにして始めます。

::

        # mkdir -p /usr/local/portage/net-misc/foobar
        # cp /usr/portage/skel.ebuild /usr/local/portage/net-misc/foobar/foobar-1.0.0.ebuild

eclassを知る
~~~~~~~~~~~~

/usr/portage/eclassにはebuildを書く上で有用な「ライブラリ」であるeclassが置かれています。特定のパッケージ群（例えばQt）のために書かれたeclassや言語特有のeclass、ビルドツールに応じたeclassなど、Gentooリポジトリを支える多くのコードが詰まっています。

skel.ebuildを読んで愚直にビルド手順を書いてみると数十行にわたるコマンド列ができる場合でも、eclassを上手く使えば何分の一にもなることがあります。もっと楽に書けないかと思ったときは\ `eclassのリファレンス <https://devmanual.gentoo.org/eclass-reference/>`_\ を眺めてみましょう。

ebuildを書き上げたら
~~~~~~~~~~~~~~~~~~~~

さて、それらしいebuildが書けたら早速インストール……の前に、ソースコードの入ったtarballなどのチェックサムを保存しているManifestというファイルを生成します。

::

        # ebuild /usr/local/portage/net-misc/foobar/foobar-1.0.0.ebuild manifest

上手くいったらemerge net-misc/foobarしてみましょう。記述に問題がなければworldにあなたのパッケージが刻まれます。

いくつかの実例
--------------

ここまでは一般的な話をしてきましたが、ここからは私がこれまでに自分で書いたebuildからいくつか選んで話していきます。

ケース1: フォントを追加したい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

私が初めてebuildを書いたのは、使いたいフォントがあるからでした。

もちろん自分でtarballをダウンロードして適当なディレクトリに置いてもよかったのですが、/usr/share以下にパッケージマネージャを使わずに手を加えるのはシステムの更新時に上書きされる可能性を考えると避けたいですし、ホームディレクトリに置くと他のユーザからは使えなくなります。そういうわけで、私はebuildに初挑戦しました。以下がそのebuildの全文です。

::

        # Copyright 1999-2015 Gentoo Foundation
        # Distributed under the terms of the GNU General Public License v2
        # $Header: $
        
        EAPI=5
        inherit font
        
        MY_P="Koruri-${PV}"
        DESCRIPTION="Japanese TrueType font based on M+ outline fonts and Open Sans"
        HOMEPAGE="http://sourceforge.jp/projects/koruri/"
        SRC_URI="mirror://sourceforge.jp/${PN}/63497/${MY_P}.tar.xz"
        
        LICENSE="mplus-fonts Apache-2.0"
        SLOT="0"
        KEYWORDS="~amd64 ~arm ~arm64 ~x86"
        
        # Only installs fonts
        RESTRICT="binchecks strip"
        
        S="${WORKDIR}/${MY_P}"
        FONT_S="${S}"
        FONT_SUFFIX="ttf"
        DOCS="README*"

はい、これだけです。skel.ebuildを読むとわかるように、ebuildにはインストールまでの各工程に対応する手続きを書くのですが、eclassから引き継いだ手続きで十分であれば書くべき内容は「どこから持ってくる」「どんなものなのか」の説明がほとんどです。

なんだか簡単に書けそうな気がしてきませんか？

ケース2: tarballの配布場所変更に対応したい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

単にバージョンが上がっただけなら、ebuildをコピーしてファイル名のバージョン部分だけを変更するとうまくいくこともよくあります。

しかし、プロジェクトの本拠地がSourceForgeからGitHubに変わったり、独自ドメインを取得してそこに引っ越したり、.tgzになっていた拡張子がいつの間にかtar.gzに変わったりして、tarballを取得できないこともあります。そんなときはSRC_URIを書き換えましょう。

例えば、Single Unix Specificationという文書をインストールするapp-doc/single-unix-specificationパッケージで最新の2016年版をインストールするために必要な作業はSRC_URIを\ http://pubs.opengroup.org/onlinepubs/9699919799/download/susv4tc2.tar.bz2\ にすることと、それに伴ってS="${WORKDIR}/susv4tc1"という行のtc1をtc2に置き換えるだけでした。

ケース3: Rubygemsにあるパッケージを入れたい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

言語ごとのパッケージマネージャは広く使われるようになりましたが、Cライブラリとリンクする類のライブラリを扱うときには若干の注意が必要です。できることなら、Cライブラリの更新に伴って、必要なパッケージだけ再ビルドしてほしいところです。ebuildならそれができます。まあ、そうでなくともケース1と同様の理由でebuildを書きたいこともあるでしょう。

以下は昔書いた\ `adlint <http://adlint.sourceforge.net/>`_\ のebuildです。

::

        # Copyright 1999-2013 Gentoo Foundation
        # Distributed under the terms of the GNU General Public License v2
        # $Header: $
        
        EAPI=5
        
        USE_RUBY="ruby19 ruby20 ruby21"
        RUBY_FAKEGEM_EXTRAINSTALL="etc"
        
        inherit ruby-fakegem
        
        DESCRIPTION="A static source code analyzer for C"
        HOMEPAGE="http://adlint.sourceforge.net/"
        
        LICENSE="GPL-3"
        SLOT="0"
        KEYWORDS="~amd64 ~x86"
        IUSE=""

ケース1よりも短くなっていますが、掲載ミスではありません。ruby-fakegemというeclassのおかげで、Rubygemsからインストールできる場合はもはやSRC_URIすら書かなくてもよくなり、ほぼメタデータしか書かれていません。Rubygemsからインストールできない場合でも、ruby-ngというeclassがシステムにある複数バージョンのRubyにインストールする面倒を見てくれます。

Rubyだけでなく、Java、Python、Perlなど様々な言語に向けたeclassが用意されています。

ケース4: configureしてmakeしてmake install系のソフトウェアを入れたい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

様々なメタビルドツールであふれている今でも、Autotoolsを使ってビルドするソフトウェアは数多く存在しています。そうしたソフトウェアをインストールするためのebuildの一例をお見せします。

::

	# Copyright 1999-2014 Gentoo Foundation
	# Distributed under the terms of the GNU General Public License v2
	# $Header: $
	
	EAPI=5
	
	inherit autotools-multilib
	
	DESCRIPTION="A library to retrieve the information in the NamesList.txt
	published by the Unicode Consortium."
	HOMEPAGE="https://bitbucket.org/sortsmill/libunicodenames/"
	SRC_URI="mirror://bitbucket/sortsmill/${PN}-new-repo/downloads/${P}.tar.xz"
	
	LICENSE="LGPL-3+"
	SLOT="0"
	KEYWORDS="~amd64 ~x86"
	IUSE="cxx nls static-libs"
	
	DEPEND="virtual/pkgconfig
		nls? ( >=sys-devel/gettext-0.18.1 )"
	RDEPEND=""
	
	src_configure() {
		local myeconfargs=(
			$(use_enable cxx c++)
			$(use_enable nls)
		)
		autotools-multilib_src_configure
	}
	
	src_install() {
		autotools-multilib_src_install
	
		# Use pkgconfig instead of libtool's .la file.
		prune_libtool_files --modules
	}

今までに比べると長くなりましたが、それでも全体で40行に満たない短いファイルです。myeconfargsという部分（configureに渡す--enable-xyzといった引数をUSEフラグを元に構築している）以外はskel.ebuildから得られる知識で読める部分も多いと思います。

ここでのポイントはautotools-multilibというeclassで、例によって実際の仕事の大部分はこのeclassに書かれています。

Autotoolsだけでなく、CMakeやSConsといった他のビルドツール向けのeclassもあるので、リファレンスのページでビルドツールの名前を検索してみるのも良いと思います。

ケース5: USEフラグを追加したい
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ケース4でも触れたように、USEフラグの設定をebuild内で扱う場面のひとつにconfigureへの引数があります。こうした引数はバージョンが上がる際にしばしば追加されますが、USEフラグが追加されていないがためにその機能を有効にしてビルドする方法がないこともあります。

例として、xtermに注目します。最近のxtermはSixelやReGISといった比較的後期のDEC VTが有していたグラフィックス機能を実装しています。これらのグラフィックス機能はconfigureで--enable-sixel-graphicsといった引数を与えることで有効になりますが、Gentooリポジトリのx11-terms/xtermにはそのようなことをする機能がありません。

それではSixelを使えるxtermのebuildを作ってみましょう。まずはローカルオーバレイにバージョンに-r1などと付け加えた名前でxtermのebuildをコピーします（例えばxterm-327-r1.ebuild）。

そしてIUSEにsixelを含めます。例えば以下のように。

::

        IUSE="+openpty sixel toolbar truetype unicode Xaw3d xinerama"

今度はeconfの後に並ぶconfigureの引数の列にsixelのものを付け加えます。例えば以下のように。

::

		...
		$(use_enable openpty) \
		$(use_enable sixel sixel-graphics) \
		$(use_enable toolbar) \
		...

今回のように外部のソフトウェアへの依存関係が増えない類であれば、必要な仕事はこれで大体終わりです。新たなライブラリとリンクしなければならない場合などはRDEPENDやDEPENDなどに必要なパッケージを追加しましょう。（USEフラグを条件にして依存するように書くのを忘れずに！）

おわりに
--------

いくつかの事例を紹介しましたが、慎重な方であれば「でも、これは簡単そうな例だけを取り上げてるだけじゃないか？」と思うことでしょう。その通りです。

ebuildを書いていく中で、今回紹介したものを含むeclassが役に立つ場合は多いですが、そうでもない場合もあります。また、この文書にはebuildの詳細な仕様も記載されておらず、ebuildで使う様々な「コマンド」、今回登場したものでいうとeconfなどについても説明していません。また、metadata.xmlやfilesディレクトリなども知っておくことが重要です。良いebuildを書くために必要な更なる知識は以下の文書で得られることでしょう。

* `Basic guide to write Gentoo Ebuilds <https://wiki.gentoo.org/wiki/Basic_guide_to_write_Gentoo_Ebuilds>`_\ ではebuildの基礎が説明されています。
* `Package Manager Specification <https://wiki.gentoo.org/wiki/Package_Manager_Specification>`_\ にはebuildの仕様書があります。
* `Gentoo Development Guide <https://devmanual.gentoo.org/index.html>`_\ はGentoo開発者のためのガイドです。

もし便利なebuildが書けたら、GitHubなどで自分のローカルオーバレイを公開するのも良いでしょう。また、Gentooリポジトリにあるebuildを修正した場合は、Gentooリポジトリに取り込んでもらうべく\ `GentooのBugzilla <https://bugs.gentoo.org/>`_\ への報告や\ `GitHubミラー <https://github.com/gentoo/gentoo>`_\ へのプルリクエストをぜひ検討してみてください。

この文書を読む前よりもebuildを身近に感じられますように。

.. _Gentoo Advent Calendar 2016: http://www.adventar.org/calendars/1493
