from doctree.utils import guid


def test_parse_guid():
    guid_str = "0.2.3"
    assert guid.parse_guid(guid_str) == [0, 2, 3]


def test_generate_guid():
    guid_list = [0, 2, 3]
    assert guid.generate_guid(guid_list) == "0.2.3"
