from abra.abra_pb2 import Snapshot
from abra.common import *
from abra.errors import *
import json
from .parsers import PARSER_NAMES, PoseParser, CImageParser, DImageParser, FeelingsParser
from pathlib import Path


def parse(parser, data_path):
    parser = parser.lower()
    if parser not in PARSER_NAMES:
        raise UnknownParserError(f"Unknown parser! please choose one of the following:\n{PARSER_NAMES!r}")

    path = Path(data_path)
    with open(path, "rb") as f:
        raw_data = json.load(f)

    data = json.loads(raw_data)
    parser_h = get_parser(parser)

    user_id, snapshot_id, path = data[USER_ID_KEY], data[SNAPSHOT_ID_KEY], data[USER_SNAPSHOTS_URL_KEY]
    snapshot = load_snapshot(path)
    parsed_data = parser_h.parse(msg=snapshot)
    wrapped_parsed_data = wrap_parsed_data(parsed_data, parser, user_id, snapshot_id)
    parsed_data_json = json.dumps(wrapped_parsed_data)
    return parsed_data_json


def wrap_parsed_data(parsed_data, parser, user_id, snapshot_id):
    wrapped_parsed_data = {
        TOPIC_KEY: parser,
        USER_ID_KEY: user_id,
        SNAPSHOT_ID_KEY: snapshot_id,
        PARSED_DATA_KEY: parsed_data
    }
    return wrapped_parsed_data


def get_parser(parser_name: str):
    if parser_name == "pose":
        return PoseParser()
    elif parser_name == "color-image":
        return CImageParser()
    elif parser_name == "depth-image":
        return DImageParser()
    elif parser_name == "feelings":
        return FeelingsParser()
    else:
        return None


def load_snapshot(path):
    f = Path(path)
    if not f.is_file():
        raise UnknownPathError(f"ERROR: no file detected on '{f}'")
    snapshot = Snapshot()
    r_data = f.read_bytes()
    snapshot.ParseFromString(r_data)
    return snapshot


def wrap_data_for_saver(user, data):
    data[USER_ID_KEY] = user.user_id
