import json
import unittest
from unittest import mock

import pytest
from _pytest.tmpdir import tmp_path

import lagring as lg

working_server_data = [
    {
        "namn": "web01",
        "adress": "example.com",
        "miljo": "prod",
        "roll": "webbserver",
        "status": "unknown",
        "senast_kontrollerad": "",
    },
    {
        "namn": "db01",
        "adress": "127.0.0.1",
        "miljo": "prod",
        "roll": "databas",
        "status": "unknown",
        "senast_kontrollerad": "",
    },
    {
        "namn": "test01",
        "adress": "192.0.2.10",
        "miljo": "test",
        "roll": "testserver",
        "status": "unknown",
        "senast_kontrollerad": "",
    },
    {
        "namn": "dev01",
        "adress": "localhost",
        "miljo": "dev",
        "roll": "utvecklingsserver",
        "status": "unknown",
        "senast_kontrollerad": "",
    },
]


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
