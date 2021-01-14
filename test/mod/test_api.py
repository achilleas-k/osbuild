#
# Test for API infrastructure
#

import os
import multiprocessing as mp
import sys
import tempfile
import pytest

import osbuild
from osbuild.util import jsoncomm


class APITester(osbuild.api.BaseAPI):
    """Records the number of messages and if it got cleaned up"""
    def __init__(self, sockaddr):
        super().__init__(sockaddr)
        self.clean = False
        self.messages = 0

    endpoint = "test-api"

    def _message(self, msg, _fds, sock):
        self.messages += 1

        if msg["method"] == "echo":
            msg["method"] = "reply"
            sock.send(msg)

    def _cleanup(self):
        self.clean = True


@pytest.fixture
def tmpdir():
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir

def test_basic(tmpdir):
    # Basic API communication and cleanup checks
    socket = os.path.join(tmpdir, "socket")
    api = APITester(socket)
    with api:
        with jsoncomm.Socket.new_client(socket) as client:
            req = {'method': 'echo', 'data': 'Hello'}
            client.send(req)
            msg, _, _ = client.recv()
            assert msg["method"] == "reply"
            assert req["data"] == msg["data"]

    assert api.clean
    assert api.messages == 1

    # Assert proper cleanup
    assert api.thread is None
    assert api.event_loop is None

def test_reentrancy_guard(tmpdir):
    socket = os.path.join(tmpdir, "socket")
    api = APITester(socket)
    with api:
        with pytest.raises(AssertionError):
            with api:
                pass

def test_get_arguments(tmpdir):
    path = os.path.join(tmpdir, "osbuild-api")
    args = {"options": {"answer": 42}}
    monitor = osbuild.monitor.BaseMonitor(sys.stderr.fileno())

    with osbuild.api.API(args, monitor, socket_address=path) as _:
        data = osbuild.api.arguments(path=path)
        assert data == args

def test_exception(tmpdir):
    # Check that 'api.exception' correctly sets 'API.exception'
    path = os.path.join(tmpdir, "osbuild-api")
    args = {}
    monitor = osbuild.monitor.BaseMonitor(sys.stderr.fileno())

    def exception(path):
        with osbuild.api.exception_handler(path):
            raise ValueError("osbuild test exception")
        assert False, "api.exception should exit process"

    api = osbuild.api.API(args, monitor, socket_address=path)
    with api:
        p = mp.Process(target=exception, args=(path, ))
        p.start()
        p.join()
    assert p.exitcode == 2
    assert api.error is not None, "Error not set"
    assert "type" in api.error, "Error has no 'type' set"
    assert api.error["type"] == "exception", "Not an exception"
    e = api.error["data"]
    for field in ("type", "value", "traceback"):
        assert field in e, f"Exception needs '{field}'"
    assert e["value"] == "osbuild test exception"
    assert e["type"] == "ValueError"
    assert "exception" in e["traceback"]

def test_metadata(tmpdir):
    # Check that `api.metadata` leads to `API.metadata` being
    # set correctly
    path = os.path.join(tmpdir, "osbuild-api")
    args = {}
    monitor = osbuild.monitor.BaseMonitor(sys.stderr.fileno())

    def metadata(path):
        data = {"meta": "42"}
        osbuild.api.metadata(data, path=path)
        return 0

    api = osbuild.api.API(args, monitor, socket_address=path)
    with api:
        p = mp.Process(target=metadata, args=(path, ))
        p.start()
        p.join()
        assert p.exitcode == 0
    metadata = api.metadata  # pylint: disable=no-member
    assert metadata
    assert metadata == {"meta": "42"}
