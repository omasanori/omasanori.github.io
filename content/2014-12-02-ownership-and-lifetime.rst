なぜRustの人はlifetimeとownershipについて話すのか
=================================================

:date: 2014-12-02 00:00
:slug: ownership-and-lifetime
:lang: ja
:summary: lifetimeとownershipについて振り返ってみる。

これは `Rust Language Advent Calendar 2014`_ の2日目の記事です。前日は `@saneyuki_s`_ さんの『\ `Rustプログラミングにおけるデバッグ入門`_\ 』でした。

今日はlifetimeとownershipの話です。「なんだそれは」と思った方も、「またか」と思った方も、「Rust使ってるからよく知ってるよ」と思った方も少しの間お付き合いください。

はじめに
--------

ブラウザの会社が公開したRustというプログラミング言語があります。ブラウザの会社が公開した言語なので、\ `Rustで書かれたブラウザ`_\ もあります。このプログラミング言語の特徴の一つがlifetimeとownershipです。

例えば、\ `Rustの30分イントロダクション`_\ は少し前に書き直されるまではlifetimeとownershipを中心に解説していました。\ `関数型言語に慣れ親しんだ人のために書かれた別のRustイントロダクション`_\ でもlifetimeを題した章がありますし、その手前の章ではownershipを扱っています。以前イントロダクションとして評判の良かった\ `Rust by Example`_\ でもこれらはそれぞれの章を割り振られています。私が以前イベントでRustについて発表した際もこれらに時間を割いていましたし、東京で開催されているRustのイベントであるRust Samuraiでも直近の回でこれらの解説が行われていました。

なぜRustの人はlifetimeとownershipをよく取り上げるのでしょうか。私が思うに、これらの機能がRustコードを支える要であり、これらの機能を持たないプログラミング言語を背景に持つ人にとっては戸惑いの種になることがその理由でしょう。以下でこれらの機能を他の言語のやり方と比較しながら紹介していきます。

lifetime: リソースの寿命
------------------------

ある程度大きなプログラムは様々なリソースを扱います。例えば、メモリ、ファイル、ソケット、データベースとの接続などがあります。これらを管理する上で重要なのが寿命、つまり不要になる時期です。寿命は短く見積もりすぎても長く見積もりすぎても問題を引き起こします。短く見積もりすぎると不要だと判断されたリソースへのアクセスや頻繁なリソースの再取得が発生し、長く見積もりすぎるとリソースの再分配が滞ります。

寿命を扱う原始的な方法は、プログラマー自身がそれを扱うというものです。つまり、プログラミング言語は寿命の管理を補助しません。検証用のツールを通さない限り、コンピュータはあなたの方針に口を出しません。たとえ、明らかに間違っていたとしても。

GC (garbage collection) はプログラミング言語が寿命の管理を補助する機構として広く利用されています。GCの手法はトレース (tracing) と参照カウント (reference counting) の2つに大きく分けられますが、どちらも実行時にあるリソースが不要になったことを検知して後始末します。Objective-CのARC (automatic reference counting) もretainとreleaseをコンパイラがプログラマの代わりに挿入する仕組みであって、実行時のコストはretainとreleaseを書く場合と変わりません。\ [#]_

広く利用されている別の方法として、変数の有効な範囲（スコープ）を寿命と結びつけるものがあります。いわゆるスタック変数はその身近な例です。スコープをコンパイル時に解析できるならば、スコープと結び付けられたリソースが不要になるタイミングもまたコンパイル時に解析できるので、実行時に不要になったかどうかを調べずに済みます。C++などでよく使われているRAII (resource acquisition is initialization) パターンもこの方法に分類できます。

lifetimeはスコープを使った方法と似ていますが、重要な違いを含んでいます。それは、有効な範囲に名前を付けて明示的に扱うことができるという点です。この違いによって、「この関数の引数として渡されるリソースの有効範囲は返り値として生成されるリソースの有効範囲を含まなければならない」といった制約を表現することができるようになります。Rustでプログラムを書いていて "does not live long enough" というフレーズを含むメッセージが表示されたときは、コードの中にそうした制約を守っていない部分があることを示しています。

.. [#] ただし、理屈の上ではコンパイラが最適化しやすくなり、Clangのドキュメントでもそのような最適化の可能性を示唆している。とはいえ、大雑把に言うと「ここで参照数を上げてすぐ下げるのは明らかに無駄」というような箇所でそれを省くというもので、真に参照カウントが必要な箇所において実行時のコストがなくなるというわけではない。

ownership: リソースの所有権
---------------------------

リソースを管理する際に気を遣うのは寿命だけではありません。ある時点で特定のリソースに何らかの操作をして良いかどうかを管理することも重要です。リソースを「読む」「書き換える」、あるいは「不要になったので後始末する」というのも操作に含まれます。これを適切に管理できなかった場合、リソースやプログラム全体が整合性を損なうことになります。

こうした「操作を行う権利」はプログラムが並行に動作する複数の処理単位（プロセス、スレッド、タスクなどの様々な名前があります）によって構成されている場合によく問題となるので、それを管理する方法は並行性と共に論じられがちです。しかし、並行性を含まないプログラムであっても、例えばC言語の関数について書かれたmanページで見かける「関数を呼び出した後のbufの状態は未規定である」という類の文面はまさに操作を行う権利について述べています。

Rustのownershipとは、どの有効なリソースもプログラムのある部分に所有されており、あるリソースをある時点で所有している部分はただひとつという制約（所有権）を指しています。例えば、あるタスクが所有権を持っているリソースを同時に別のタスクが所有することはできません。また、ある関数がリソースの所有権を要求しなければ、その関数は所有権が必要な操作を内部で行うことができません。

リソースをプログラムの複数の部分で共有するにはどうしたらよいでしょうか。もし本当に共有する必要がないのであれば、リソースを複製するのも可能な場面では有効です。また、所有権は移動する (move) こともできますし、所有権を持つ部分からリソースを借りる (borrow) こともできます。リソースを借りている場合は所有権を持っている場合に比べて制限を受け、またリソースをどこかが借りている場合は所有権を持つ部分も制限を受けます。

このようなモデルでは扱えないプログラムを書く場合のために、Rustは抜け道を用意しています。しかし、普段はownershipに従ってコードを書くことでコンパイラに安全性を検証させることができます。

起源
----

Rustはlifetimeを導入した初めてのプログラミング言語ではなく、ownershipを導入した初めてのプログラミング言語でもありません。例えば、lifetime（一般的にはregionと呼ばれ、Rustでもかつてはそう呼んでいました）は1960年代にその萌芽が現れたそうです（Wikipediaの\ `Region-based memory management`_\ によくまとまっている）。私はownershipの起源を知りません（ご存じの方がいらっしゃったらぜひご一報ください）が、RAIIパターンはある種のownershipを表現していますし、Rustの発表以前にも型システムにそのような概念を導入する試みがあった（\ `OOPSLA '02のBoyapatiらによる論文`_\ など）ようです。

おわりに
--------

この記事は、かつてRustについて発表する機会を頂いた際にlifetimeとownershipについてうまく発表できなかったことがきっかけで書かれました。あなたがRustに興味を持つきっかけ、あるいは何か新しいアイデアを得る助けになれば幸いです。

.. _`Rust Language Advent Calendar 2014`: http://www.adventar.org/calendars/462
.. _`@saneyuki_s`: https://twitter.com/saneyuki_s
.. _`Rustプログラミングにおけるデバッグ入門`: http://saneyukis.hatenablog.com/entry/2014/12/01/034929
.. _`Rustで書かれたブラウザ`: https://github.com/servo/servo
.. _`Rustの30分イントロダクション`: http://doc.rust-lang.org/intro.html
.. _`関数型言語に慣れ親しんだ人のために書かれた別のRustイントロダクション`: http://science.raphael.poss.name/rust-for-functional-programmers.html
.. _`Rust by Example`: http://rustbyexample.com/
.. _`Region-based memory management`: http://en.wikipedia.org/wiki/Region-based_memory_management
.. _`OOPSLA '02のBoyapatiらによる論文`: http://dl.acm.org/citation.cfm?id=582440
