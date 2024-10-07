import pytest


@pytest.mark.sphinx('proj_rest')
def test_build(sphinx_app):
    assert (sphinx_app.outdir / "index.html").exists()
