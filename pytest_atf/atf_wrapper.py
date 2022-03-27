from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from typing import Any, Sequence
from argparse import *

import pytest
from pytest_atf.markers import atf_markers


class EnvironParserAction(Action):
    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        pair: str,
        option_string: str | None = ...,
    ) -> None:
        key, value = pair.split("=")
        env = getattr(namespace, self.dest)
        env = env if env else dict()
        env[key] = value
        setattr(namespace, self.dest, env)


def parse_args(args: Sequence[str] = None):
    parser = ArgumentParser(description="Process ATF arguments")

    list_tests_group = parser.add_argument_group()
    list_tests_group.add_argument(
        "-l",
        dest="list_tests",
        action="store_true",
        help="Lists available test cases alongside a brief description for each of them.",
    )

    test_case_group = parser.add_argument_group()
    test_case_group.add_argument(
        "-r",
        dest="resfile",
        action="store",
        type=FileType("w"),
        metavar="resfile",
        help="""Specifies the file that will receive the test case result. 
    If not specified, the test case prints its results
	to stdout. If the result of a test case needs to be
	parsed by another program,	you must use this option to
	redirect the result to a file and then read the resulting
	file from the other program.  Note: do not try to process
	the stdout of the test case because your program may
	break in the future.""",
    )
    test_case_group.add_argument(
        "-s",
        dest="srcdir",
        action="store",
        type=lambda p: Path(p).absolute(),
        metavar="srcdir",
        help="""The path to the directory where the test program is located. 
                                 This is needed in all cases, except when the test program is being executed from the current directory.
                                 The test program will use this path to locate any helper data files or utilities.""",
    )
    test_case_group.add_argument(
        "-v",
        dest="vars",
        action=EnvironParserAction,
        help="Sets the configuration variable var to the value value.",
        metavar="var=value",
    )
    test_case_group.add_argument(
        "test_case",
        action="store",
        type=lambda s: s if s else None,
        nargs="?",
        help="Test case to run",
    )

    args: Namespace = parser.parse_args(args)

    if not args.list_tests and args.test_case == None:
        raise ValueError("One of -l or test_case should be specified")

    if args.list_tests and args.test_case != None:
        raise ValueError("One of -l or test_case should be specified")

    return args


class PytestError(Exception):
    err: str

    def __init__(self, err: str, *args: object) -> None:
        super().__init__(*args)
        self.err = err

    def __str__(self) -> str:
        return self.err


def list_tests():
    class CollectPlugin:
        items: list[pytest.Item] = []

        def pytest_report_collectionfinish(items):
            CollectPlugin.items = items

    flags = ["-qqq", "--no-header", "--no-summary", "--collect-only"]

    with redirect_stdout(StringIO()) as stdout:
        with redirect_stderr(StringIO()) as stderr:
            code = pytest.main(flags, [CollectPlugin])
            if code != pytest.ExitCode.OK:
                raise PytestError(stdout.getvalue())

    return CollectPlugin.items


def get_test_metadata(test: pytest.Item) -> dict[str, Any]:
    """Returns the ATF metadata associated to a test."""
    metadata = {}
    metadata["ident"] = test.name

    if hasattr(test, "obj") and hasattr(test.obj, "__doc__") and test.obj.__doc__:
        metadata["descr"] = test.obj.__doc__

    for mark in test.iter_markers():
        if mark.name in atf_markers:
            entry = atf_markers[mark.name]

            if entry.type is list:
                metadata[entry.metadata_key] = (
                    mark.args[0] if isinstance(mark.args[0], list) else mark.args
                )
            elif isinstance(mark.args[0], entry.type):
                metadata[entry.metadata_key] = mark.args[0]

    return metadata


def format_metadata(metadata: dict[str, Any]) -> str:
    s = []
    for prop, value in metadata.items():
        value = (
            " ".join(str(val) for val in value)
            if isinstance(value, (list, tuple))
            else str(value)
        )
        value = value.replace("\n", "\t")
        s.append(f"{prop}: {value}")
    return "\n".join(s) + "\n"


METADATA_HEADER = 'Content-Type: application/X-atf-tp; version="1"\n\n'


def atf_main_wrapper(args: Sequence[str] = None):
    parsed_args = parse_args(args)
    if parsed_args.list_tests:
        tests = list_tests()
        metadatas = "\n".join(
            format_metadata(get_test_metadata(test)) for test in tests
        )
        print(METADATA_HEADER)
        print(metadatas)
