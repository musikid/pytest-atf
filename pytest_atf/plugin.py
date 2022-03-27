from pathlib import Path
from pytest import Session, hookimpl, Parser
from pytest_atf.markers import atf_markers


def pytest_configure(config):
    for _, description, _ in atf_markers.values():
        config.addinivalue_line("markers", description)


def _format_tests(items):
    pass
