import json
from unittest import mock

import pytest
from test_setup import *

import lagring as lg


def test_file_exist(monkeypatch):
    """Test parsing"""
    m = mock.mock_open(read_data=json.dumps(working_server_data))
    monkeypatch.setattr("builtins.open", m)

    result = lg.parse_servers_json()
    assert result == working_server_data


def test_environment_variable_read(monkeypatch, tmp_path):
    """Testing the environment variable"""
    file = tmp_path / "test_server.json"
    file.write_text(json.dumps(working_server_data), "utf-8")
    monkeypatch.setenv("INVENTORY_DATAFIL", str(file))

    result = lg.parse_servers_json()
    assert result == working_server_data


test_server_for_add = {
    "namn": "dev01",
    "adress": "localhost",
    "miljo": "dev",
    "roll": "utvecklingsserver",
    "status": "Unknown",
    "senast_kontrollerad": "",
}


def test_add_server(monkeypatch, tmp_path):
    """Test if the server is added correctly"""
    # I do not need to mock_open because
    # we create a temp file
    file = tmp_path / "test_server.json"
    monkeypatch.setenv("INVENTORY_DATAFIL", str(file))

    lg.add_server("dev01", "localhost", "dev", "utvecklingsserver")
    result = lg.parse_servers_json()
    assert result == test_server_for_add


@pytest.fixture
def up_down():
    return ["UP", "DOWN"]


def test_update_server_status(up_down, monkeypatch, tmp_path):
    file = tmp_path / "test_server.json"
    monkeypatch.setenv("INVENTORY_DATAFIL", str(file))
    file.write_text(json.dumps(working_server_data), "utf-8")

    monkeypatch.setattr(lg, "get_current_time", lambda: test_time)
    lg.update_server_status("web01", up_down)

    target_server = lg.get_server("web01")

    assert target_server["status"] == up_down
    assert target_server["senast_kontrollerad"] == lg.get_current_time()
