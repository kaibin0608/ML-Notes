# content of test_sysexit.py
import pytest


def f():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()

#### run this 
# $pytest -q test_sysexit.py
#The -q/--quiet flag keeps the output brief in this and following examples.