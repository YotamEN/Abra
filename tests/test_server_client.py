from abra.server import run_server
from abra.client import upload_sample

TEST_PORT = 8060
TEST_HOST = '127.0.0.1'


def conn_assertion(client_path):
    import multiprocessing
    import time

    loc_server = multiprocessing.Process(target=run_server,
                                         args=(TEST_HOST, TEST_PORT, print))
    loc_server.start()
    time.sleep(3)
    upload_sample(host=TEST_HOST, port=TEST_PORT, path=client_path)
    loc_server.terminate()

    return True


def test_client_server_short():
    assert conn_assertion(client_path="./tests/mock_data/short.mind.gz"), "Failed short server test"

#
# def test_client_server_long():
#     assert conn_assertion(client_path="./tests/mock_data/long.mind.gz"), "Failed long server test"
