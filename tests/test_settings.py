import pytest
from lxml import html


class TestInlineClass:
    '''Tests for `inline_svg_classes` setting
    '''
    @pytest.mark.sphinx_config(inline_svg_classes=[])
    def test_no_class(self, sphinx_app):
        '''In case no class from `inline_svg_classes` applied
        '''
        tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
        elements = tree.xpath('//svg')
        assert len(elements) == 0

    @pytest.mark.sphinx_config(inline_svg_classes=['inline-svg', 'custom-svg'])
    def test_additional_class(self, sphinx_app):
        '''In case additional class from `inline_svg_classes` applied
        '''
        tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
        elements = tree.xpath('//svg')
        assert len(elements) == 2


class TestDelAttrs:
    '''Tests for `inline_svg_del_attrs` setting
    '''
    @pytest.mark.sphinx_config(inline_svg_del_attrs=[])
    def test_del_no_attrs(self, sphinx_app):
        '''Test if `inline_svg_del_attrs` setting is applied
        '''
        tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")
        svg_elem = tree.xpath('//svg')[0]

        # `inline_svg_del_attrs` setting has 'content' by default.
        # In this test, `inline_svg_del_attrs` is set as empty,
        # so the svg element should have 'content' attribute.
        assert svg_elem.get('content')


class TestResolveXRef:
    '''Tests for `inline_svg_resolve_xref` setting
    '''
    @pytest.mark.sphinx_config(inline_svg_resolve_xref=False)
    def test_no_resolve_xref(self, sphinx_app):
        '''Test if `inline_svg_del_attrs` setting is applied
        '''
        tree = html.parse(sphinx_app.outdir / "svg_inline/index.html")

        # Test project name for this test - 'proj_rest' or 'proj_myst'
        proj_name = sphinx_app.srcdir.parent.name
        # Hyperlink's `href` attribute depends on test project.
        href = '/index.rst' if proj_name == 'proj_rest' else '/index.md'

        text = 'To Document root'
        xpath = f'//svg//a[@href="{href}" and text()="{text}"]'
        elements = tree.xpath(xpath)
        assert len(elements) == 1
