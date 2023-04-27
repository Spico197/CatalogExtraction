from doctree.utils import content_tool as C


def test_merge_pair_contents():
    contents = [
        {
            "order": "1213",
            "sentence1": "123",
            "sentence2": "456",
            "label": -1,
            "pred_tag": 1,
        },
        {
            "order": "1214",
            "sentence1": "456",
            "sentence2": "789",
            "label": -1,
            "pred_tag": 0,
        },
        {
            "order": "1215",
            "sentence1": "789",
            "sentence2": "131",
            "label": -1,
            "pred_tag": 1,
        },
        {
            "order": "1216",
            "sentence1": "131",
            "sentence2": "234",
            "label": -1,
            "pred_tag": 1,
        },
        {
            "order": "1217",
            "sentence1": "234",
            "sentence2": "345",
            "label": -1,
            "pred_tag": 0,
        },
        {
            "order": "1218",
            "sentence1": "345",
            "sentence2": "423",
            "label": -1,
            "pred_tag": 1,
        },
        {
            "order": "1219",
            "sentence1": "423",
            "sentence2": "456",
            "label": -1,
            "pred_tag": 1,
        },
        {
            "order": "1220",
            "sentence1": "456",
            "sentence2": "567",
            "label": -1,
            "pred_tag": 0,
        },
        {
            "order": "1221",
            "sentence1": "567",
            "sentence2": "756",
            "label": -1,
            "pred_tag": 1,
        },
        {
            "order": "1222",
            "sentence1": "756",
            "sentence2": "19",
            "label": -1,
            "pred_tag": 0,
        },
    ]
    results = C.merge_pair_text(contents)
    assert results == ["123456", "789131234", "345423456", "567756", "19"]
