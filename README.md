# sphinx-inline-svg

[≫日本語版](https://github.com/satamame/sphinx-inline-svg/blob/main/README_ja.md)

## Overview

Sphinx extension to make SVG images inline.  
It helps to make text in SVG into hyperlink.  
If the builder is not `html`, it has no effect.

## Installation

### pip

```
pip install sphinx-inline-svg
```

### rye

```
rye add --dev sphinx-inline-svg
```

## Usage

### conf.py

Add it to `extensions`.

```python
# conf.py

extensions = [
    'sphinx_inline_svg',
]
```

### Add CSS class

Add CSS class to SVG image to be inlined.

```
.. image:: img/chart.drawio.svg
    :class: inline-svg
```

As for MyST, enable `attrs_inline` in conf.py.

```python
# conf.py

myst_enable_extensions = [
    "attrs_inline",
]
```

```markdown
![](img/chart.drawio.svg){.inline-svg}
```

Define `inline-svg` class in CSS.

```css
/* _static/css/custom.css */

/* example */
.inline-svg {
  max-width: 100%;
  height: auto;
}
```

Add it in conf.py as follows if defined in _static/css.

```python
# conf.py

def setup(app):
    app.add_css_file('css/custom.css')
```

## Hyperlink

To make text in SVG a hyperlink, for example, edit it as follows in [draw.io](https://app.diagrams.net).

![drawio_edit_link.png](https://raw.githubusercontent.com/satamame/sphinx-inline-svg/main/img/drawio_edit_link.png)

![drawio_link_dialog.png](https://raw.githubusercontent.com/satamame/sphinx-inline-svg/main/img/drawio_link_dialog.png)

### Link notation

Link destination that is generated after build depends on Link notation.

|Notation|Generated destination|Example|Destination for example|
|-|-|-|-|
|Starts with "/".|Path from project root.|/index.rst|Top page.|
|Starts with "#".|Defined cross-reference target.|#target-1|Position defined as "#target-1" in the project.|
|Starts with "http://" and so on.|As is.|https:&#8203;//google&#8203;.com|The site on the Internet.|
|Other than above.|Relative path from the page.|detail.rst|detail.html file in the same directory.|

> [!NOTE]
> As for the last notation, generated destination is relative from the page where SVG is extracted to, not from the SVG itself.

## Configuration

The following settings can be configured in conf.py. If you do not write the configuration itself, the default value is applied.

```python
# conf.py

inline_svg_classes = ['inline-svg', 'selectable-svg']
```

|Name|Type|Description|Default value|
|-|-|-|-|
|inline_svg_classes|`list[str]`|List of class names. SVG image with any of these will be inlined.|`['inline-svg']`|
|inline_svg_del_attrs|`list[str]`|List of attribute names to be deleted from svg element when extracted.|`['content']`|
|inline_svg_resolve_xref|`bool`|Whether to convert destination as described in the above "Link notation" section.|`True`|

> [!NOTE]
> The svg element in SVG file saved by draw.io has "content" attribute, but this is data for editing by the draw.io app, so it is not necessary for the svg element to be inlined.
