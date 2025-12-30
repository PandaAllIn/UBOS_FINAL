from __future__ import annotations

import pytest
from pathlib import Path
from trinity.master_librarian_adapter import MasterLibrarianAdapter


@pytest.fixture
def adapter() -> MasterLibrarianAdapter:
    return MasterLibrarianAdapter()


def test_write_and_read_file(adapter: MasterLibrarianAdapter):
    file_path = "skills/test_file.txt"
    content = "Hello, world!"
    adapter.write_file(file_path, content)
    read_content = adapter.read_file(file_path)
    assert read_content == content


def test_execute_shell(adapter: MasterLibrarianAdapter):
    result = adapter.execute_shell("echo 'Hello, shell!'")
    assert result["ok"]
    assert result["stdout"].strip() == "Hello, shell!"