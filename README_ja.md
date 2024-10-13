# sphinx-inline-svg

## 概要

SVG 画像をインライン化する Sphinx 拡張機能です。  
SVG 内のテキストをハイパーリンクにしたい場合に便利です。  
ビルダーが `html` の場合のみ効果があります。

## インストール

### pip

```
> pip install sphinx-inline-svg
```

### rye

```
> rye add --dev sphinx-inline-svg
```

## 使い方

### conf.py

`extensions` に追加します。

```python
# conf.py

extensions = [
    'sphinx_inline_svg',
]
```

### クラスの追加

インライン化したい SVG 画像にクラスを追加します。

```
.. image:: img/chart.drawio.svg
    :class: inline-svg
```

MyST の場合、conf.py で `attrs_inline` を有効にします。

```python
# conf.py

myst_enable_extensions = [
    "attrs_inline",
]
```

```markdown
![](img/chart.drawio.svg){.inline-svg}
```

実際にスタイルを変えたければ、`inline-svg` クラスを CSS で定義します。

```css
/* _static/css/custom.css */

/* 例 */
.inline-svg {
  max-width: 100%;
  height: auto;
}
```

そして、そのファイルを conf.py で追加します。

```python
# conf.py

def setup(app):
    app.add_css_file('css/custom.css')
```

> [!NOTE]
> クラスのスタイルを定義しなくても、クラスを追加した SVG 画像はインライン化されます。

## ハイパーリンク

SVG 内のテキストをハイパーリンクにするには、たとえば [draw.io](https://app.diagrams.net) で以下のように編集します。

![drawio_edit_link.png](https://raw.githubusercontent.com/satamame/sphinx-inline-svg/main/img/drawio_edit_link.png)

![drawio_link_dialog.png](https://raw.githubusercontent.com/satamame/sphinx-inline-svg/main/img/drawio_link_dialog.png)

### リンクの書き方

リンクの書き方によって、ビルド後のリンク先の生成方法が決まります。

|書き方|ビルド後のリンク先|例|左の例のビルド後のリンク先|
|-|-|-|-|
|"/" で始まる。|プロジェクトルートからのパス。|/index.rst|トップページ。|
|"#" で始まる。|定義されたクロスリファレンス・ターゲット。|#target-1|プロジェクト内の "#target-1" で定義された箇所。|
|"http://" 等で始まる。|そのまま。|https:&#8203;//google&#8203;.com|インターネット上のそのサイト。|
|その他。|そのページからの相対パス。|detail.rst|同じディレクトリの detail.html ファイル。|

> [!NOTE]
> 相対パスは SVG 画像ファイルからでなく SVG がインライン展開されたページからの相対パスになります。

## 設定

conf.py で以下の設定ができます。設定自体を書かなければデフォルト値が適用されます。

```python
# conf.py

inline_svg_classes = ['inline-svg', 'selectable-svg']
```

|設定名|型|説明|デフォルト値|
|-|-|-|-|
|inline_svg_classes|`list[str]`|クラス名のリスト。これらのいずれかを持つ SVG 画像はインライン化される。|`['inline-svg']`|
|inline_svg_del_attrs|`list[str]`|インライン展開する時に svg 要素から削除する属性名のリスト。|`['content']`|
|inline_svg_resolve_xref|`bool`|リンク先を、上記の「リンクの書き方」で説明したように変換するかどうか。|`True`|

> [!NOTE]
> draw.io で保存した SVG ファイルの svg 要素には content 属性がありますが、これは draw.io アプリで編集時に使うデータなので、インライン化して表示する svg 要素には不要です。
