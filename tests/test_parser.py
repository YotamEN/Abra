from abra.parsers import *

ERROR_ON_FIELD = "Error: wrong value found in field: {0}"


def get_res(parser):
    parser_h = get_parser(parser)
    msg = load_snapshot("./tests/mock_data/snap.json")
    parsed = parser_h.parse(msg=msg)
    print(parsed)
    return parsed


def test_pose():
    parser_name = "pose"
    parsed_data = get_res(parser_name)

    # check snapshot general data
    assert parsed_data[PARSER_NAME_KEY] == parser_name, "Error: wrong parser name!"
    assert parsed_data[DATETIME_KEY] == 1575446887339, "Error: wrong timestamp!"

    # check parsed data
    rot_res = [-0.10888676356214629, -0.26755994585035286, -0.021271118915446748, 0.9571326384559261]
    tran_res = [0.4873843491077423, 0.007090016733855009, -1.1306129693984985]

    assert parsed_data[ROT_X_KEY] == rot_res[0], ERROR_ON_FIELD.format(f"{ROT_X_KEY}")
    assert parsed_data[ROT_Y_KEY] == rot_res[1], ERROR_ON_FIELD.format(f"{ROT_Y_KEY}")
    assert parsed_data[ROT_Z_KEY] == rot_res[2], ERROR_ON_FIELD.format(f"{ROT_Z_KEY}")
    assert parsed_data[ROT_W_KEY] == rot_res[3], ERROR_ON_FIELD.format(f"{ROT_W_KEY}")

    assert parsed_data[TRANS_X_KEY] == tran_res[0], ERROR_ON_FIELD.format(f"{TRANS_X_KEY}")
    assert parsed_data[TRANS_Y_KEY] == tran_res[1], ERROR_ON_FIELD.format(f"{TRANS_Y_KEY}")
    assert parsed_data[TRANS_Z_KEY] == tran_res[2], ERROR_ON_FIELD.format(f"{TRANS_Z_KEY}")


def test_color_image():
    parser_name = "color-image"
    parsed_data = get_res(parser_name)

    # check snapshot general data
    assert parsed_data[PARSER_NAME_KEY] == parser_name, "Error: wrong parser name!"
    assert parsed_data[DATETIME_KEY] == 1575446887339, "Error: wrong timestamp!"

    # check parsed data
    assert parsed_data[HEIGHT_KEY] == 172, ERROR_ON_FIELD.format(HEIGHT_KEY)
    assert parsed_data[WIDTH_KEY] == 224, ERROR_ON_FIELD.format(WIDTH_KEY)


def test_depth_image():
    parser_name = "depth-image"
    parsed_data = get_res(parser_name)

    # check snapshot general data
    assert parsed_data[PARSER_NAME_KEY] == parser_name, "Error: wrong parser name!"
    assert parsed_data[DATETIME_KEY] == 1575446887339, "Error: wrong timestamp!"

    # check parsed data
    assert parsed_data[HEIGHT_KEY] == 172, ERROR_ON_FIELD.format(HEIGHT_KEY)
    assert parsed_data[WIDTH_KEY] == 224, ERROR_ON_FIELD.format(WIDTH_KEY)


def test_feelings():
    parser_name = "feelings"
    parsed_data = get_res(parser_name)

    # check snapshot general data
    assert parsed_data[PARSER_NAME_KEY] == parser_name, "Error: wrong parser name!"
    assert parsed_data[DATETIME_KEY] == 1575446887339, "Error: wrong timestamp!"

    # check parsed data
    res = [0.0 for _ in range(4)]

    assert parsed_data[HUNGER_KEY] == res[0], ERROR_ON_FIELD.format(HUNGER_KEY)
    assert parsed_data[THIRST_KEY] == res[1], ERROR_ON_FIELD.format(THIRST_KEY)
    assert parsed_data[EXHAUSTION_KEY] == res[2], ERROR_ON_FIELD.format(EXHAUSTION_KEY)
    assert parsed_data[HAPPINESS_KEY] == res[3], ERROR_ON_FIELD.format(HAPPINESS_KEY)
