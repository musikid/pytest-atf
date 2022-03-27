from pytest import Pytester, raises
from pytest_atf.atf_wrapper import *

DEFAULT_TEST_CASES = """
    import pytest
    from pytest_atf.markers import User

    @pytest.mark.timeout(250)
    @pytest.mark.files(["/bin/ls", "/bin/cp"])
    def test1():
        "This is a docstring"
        assert False
        pass

    @pytest.mark.user(User.ROOT)
    def test2():
        assert False
        pass

    @pytest.mark.progs("/bin/ls", "/bin/cp")
    def test3():
        assert False
        pass
    """


def test_exclusive_mutual_flag():
    actual = parse_args(["-l"])
    assert actual.list_tests
    assert actual.test_case == None

    actual = parse_args(["a_test_case"])
    assert not actual.list_tests
    assert actual.test_case == "a_test_case"

    with raises(ValueError):
        parse_args([""])

    with raises(ValueError):
        parse_args(["-l", "another_test_case"])


def test_vars_parse():
    actual = parse_args(["-v", "fake=yes", "-v", "another=yes", "stub_test_case"])
    assert actual.vars.get("fake") == "yes"
    assert actual.vars.get("another") == "yes"

    # Test spaces
    actual = parse_args(["-v", "fake=alotof yes", "stub_test_case"])
    assert actual.vars.get("fake") == "alotof yes"


def test_list_tests(pytester: Pytester):
    pypath = pytester.makepyfile(DEFAULT_TEST_CASES)

    res = pytester.runpython_c(
        """from pytest_atf.atf_wrapper import list_tests
print(list_tests())"""
    )

    items, _ = pytester.inline_genitems()

    assert str(res.stdout) == str(items)


def test_metadata(pytester: Pytester):
    pypath = pytester.makepyfile(DEFAULT_TEST_CASES)

    res = pytester.runpython_c(
        """from pytest_atf.atf_wrapper import list_tests, format_metadata, get_test_metadata
print("\\n".join(format_metadata(get_test_metadata(test)) for test in list_tests()))"""
    )

    assert (
        str(res.stdout)
        == """ident: test1
descr: This is a docstring
require.files: /bin/ls /bin/cp
timeout: 250

ident: test2
require.user: root

ident: test3
require.progs: /bin/ls /bin/cp
"""
    )
