from abra.mq.mq_handlers import RabbitMQHandler
from abra.parsers import parse, get_parser, load_snapshot, wrap_parsed_data
from abra.errors import UnknownParserError, UnknownPathError, UnsupportedMessageQueueError
import click
from abra.common import *
import json
from .parsers import PARSER_NAMES
from pathlib import Path


@click.group()
def main():
    pass


@main.command('parse')
@click.argument('parser')
@click.argument('data_path')
def parse_cli(parser: str, data_path: str):
    res = None
    try:
        res = parse(parser=parser, data_path=data_path)
    except UnknownParserError as e:
        print(e)
        exit(FAIL)
    except UnknownPathError as e:
        print(e)
        exit(FAIL)
    print(res)
    return res


# Mainly for DEBUG #
@main.command("run-all-parsers")
@click.argument('mq_url')
def run_all_parsers_cli(mq_url: str):
    for parser in PARSER_NAMES:
        run_parser_cli(parser, mq_url)


@main.command("run-parser")
@click.argument('parser')
@click.argument('mq_url')
def run_parser_cli(parser: str, mq_url: str):
    parser = parser.lower()
    if parser not in PARSER_NAMES:
        print(f"Unknown parser! please choose one of the following:\n{PARSER_NAMES!r}")
        exit(FAIL)
    parser_h = get_parser(parser)
    mq_handler = None
    try:
        mq_handler = RabbitMQHandler(mq_url)
    except UnsupportedMessageQueueError as e:
        print(e)
        exit(FAIL)

    def on_message(ch, method, props, body):
        data = json.loads(body)
        user_id, snap_id, path = data[USER_ID_KEY], data[SNAPSHOT_ID_KEY], data[USER_SNAPSHOTS_URL_KEY]
        snapshot = load_snapshot(path)  # Snapshot class
        parsed_data = parser_h.parse(msg=snapshot)
        wrapped_parsed_data = wrap_parsed_data(parsed_data, parser, user_id, snap_id)
        parsed_data_json = json.dumps(wrapped_parsed_data)
        mq_handler.publish_to_parsed_data_exchange(msg=parsed_data_json, topic=parser)

    # runs forever... stops on CTRL-C
    mq_handler.consume_queue(queue=parser, callback=on_message)


if __name__ == '__main__':
    main()
