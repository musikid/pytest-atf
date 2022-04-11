from enum import Enum
from typing import NamedTuple, Sequence, Type, TypeVar


class User(Enum):
    ROOT = "root"
    PRIVILEGED = "root"
    UNPRIVILEGED = "unprivileged"

    def __str__(self) -> str:
        return self.value


class ATFMarker(NamedTuple):
    metadata_key: str
    description: str
    type: Type | Sequence[Type]


atf_markers = {
    "timeout": ATFMarker(
        "timeout",
        """timeout(time): Specifies the maximum amount of time the test case can
        run.  This is particularly useful because some tests
        can stall either because they are incorrectly coded or
        because	they trigger an	anomalous behavior of the pro-
        gram.  It is not acceptable for these tests to stall
        the whole execution of the test	program.

        Can optionally be set to zero, in which	case the test
        case has no run-time limit.  This is discouraged.""",
        int,
    ),
    "arch": ATFMarker(
        "require.arch",
        """arch(archs): A list of architectures that the test case can be run under without causing errors due to an architecture mismatch.""",
        list,
    ),
    "config_variables": ATFMarker(
        "require.config",
        """config_variables(vars): A list of configuration variables that must be defined to execute the test case.
               If any of the required variables is not defined, the test case is skipped.""",
        list,
    ),
    "diskspace": ATFMarker(
        "require.diskspace",
        """diskspace(size): Specifies the minimum
               amount of available disk space needed by the test.
               The value can have a size suffix such as `K', `M', `G'
               or `T' to make the amount of bytes easier to type and
               read.""",
        (str, int),
    ),
    "files": ATFMarker(
        "require.files",
        """files(files): A list of files that must be present to execute the test case. The names of these files must be absolute paths.
               If any of the required files is not found, the test case is skipped.""",
        list,
    ),
    "machine": ATFMarker(
        "require.machine",
        """machine(machines):A list of machine types that the
			test case can be run under without causing errors due
			to a machine type mismatch.""",
        list,
    ),
    "memory": ATFMarker(
        "memory",
        """memory(minsize):  Specifies the minimum
			amount of physical memory needed by the	test.  The
			value can have a size suffix such as `K', `M', `G' or
			`T' to make the	amount of bytes	easier to type and
			read.""",
        (str, int),
    ),
    "progs": ATFMarker(
        "require.progs",
        """progs(programs): A list of programs that must be
        present	to execute the test case.  These can be	given
        as plain names, in which case they are looked in the
        user's PATH, or as absolute paths.  If any of the re-
        quired programs is not found, the test case is
        skipped.""",
        list,
    ),
    "user": ATFMarker(
        "require.user",
        """user(privileged): The required privileges to execute the test case.  Can
               be one of `root' or `unprivileged'.
                If the test case is running as a regular user and this
                property is `root', the	test case is skipped.
                If the test case is running as root and this property
                is `unprivileged', the runtime engine will automati-
                cally drop the privileges if the `unprivileged-user'
                configuration property is set
                otherwise the test case
                is skipped.""",
        (User, str),
    ),
}
