import json
from unittest import mock

import pytest
from test_setup import *

import kontroller as kt
import lagring as lg


# These have been tested in shell
@pytest.mark.parametrize(
    ["namn", "status"],
    [["web01", "UP"], ["db01", "UP"], ["test01", "DOWN"], ["dev01", "UP"]],
)
def test_check_server_status(namn, status, monkeypatch, tmp_path):
    file = tmp_path / "test_server.json"
    monkeypatch.setenv("INVENTORY_DATAFIL", str(file))
    file.write_text(json.dumps(working_server_data), "utf-8")

    kt.check_server_status(namn)

    assert lg.get_server(namn)["status"] == status
