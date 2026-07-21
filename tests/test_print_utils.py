from print_utils import get_print_styles


def test_get_print_styles_includes_print_specific_rules():
    styles = get_print_styles()

    assert "@media print" in styles
    assert "stSidebar" in styles
    assert "display:none !important" in styles
