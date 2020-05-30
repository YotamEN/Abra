from abra.common import DATABASE_DEFAULT_URL, FAIL
from abra.errors import UnsupportedTopic
import click
import json
from .saver import Saver


@click.group()
def main():
    pass


@main.command("save")
@click.option("--database", "-d", default=DATABASE_DEFAULT_URL)
@click.argument('topic')
@click.argument('data_path')
def save_cli(database, topic, data_path):
    saver = Saver(database)
    with open(data_path) as f:
        data = f.read()
    saver.save(topic=topic, data=data)


@main.command("run-saver")
@click.argument("db_url")
@click.argument('mq_url')
def run_saver(db_url, mq_url):
    saver = Saver(db_url)
    try:
        saver.register_to_all_topics(mq_url)
    except UnsupportedTopic as e:
        print(e)
        exit(FAIL)


if __name__ == '__main__':
    main()
