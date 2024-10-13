import pytest
from lxml import html


class TestInlineClass:
    @pytest.mark.sphinx_config(inline_svg_classes=[])
    def test_no_class(self, sphinx_app):
        '''In case no class from inline_svg_classes applied
        '''
        tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
        elements = tree.xpath('//svg')
        assert len(elements) == 0

    @pytest.mark.sphinx_config(inline_svg_classes=['inline-svg', 'custom-svg'])
    def test_additional_class(self, sphinx_app):
        '''In case additional class from inline_svg_classes applied
        '''
        tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
        elements = tree.xpath('//svg')
        assert len(elements) == 2
