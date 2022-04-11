from argparse import FileType
from io import FileIO
from os import getcwd
from sys import stdout
from typing import TextIO
from pytest import Config, TestReport, Parser
from pytest_atf.markers import atf_markers

_resfile: FileIO | TextIO = None


def pytest_addoption(parser: Parser):
    parser.addoption("--srcdir", action="store", type=str, default=getcwd())
    parser.addoption(
        "--resfile", dest="_resfile", action="store", type=FileType("w"), default=stdout
    )


def pytest_configure(config: Config):
    if not config.option.collectonly:
        global _resfile
        _resfile = config.option._resfile

    for _, description, _ in atf_markers.values():
        config.addinivalue_line("markers", description)


def pytest_runtest_logreport(report: TestReport):
    if report.when == "call":
        _resfile.write(f"{report.outcome}: {report.longreprtext}\n")
