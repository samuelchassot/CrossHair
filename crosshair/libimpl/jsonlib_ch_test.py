import json
from typing import Dict, List, Tuple, Union
import sys

import pytest  # type: ignore

from crosshair.core_and_libs import analyze_function
from crosshair.core_and_libs import run_checkables
from crosshair.core_and_libs import MessageType
from crosshair.options import AnalysisOptionSet
from crosshair.test_util import compare_results


def check_decode(s: str):
    """ post: _ """
    return compare_results(json.loads, s)


def check_encode_atomics(obj: bool, float, str, int):
    """ post: _ """
    return compare_results(json.dumps, obj)


def check_encode_containers(obj: Union[Dict[float, bool], Tuple[int, bool], List[str]]):
    """ post: _ """
    return compare_results(json.dumps, obj)


def check_encode_decode_roundtrip(obj: Union[bool, int, str]):
    """ post: _ """
    return compare_results(lambda o: json.loads(json.dumps(o)), obj)


# TODO: Test customized encoding stuff


# This is the only real test definition.
# It runs crosshair on each of the "check" functions defined above.
@pytest.mark.parametrize("fn_name", [fn for fn in dir() if fn.startswith("check_")])
def test_builtin(fn_name: str) -> None:
    opts = AnalysisOptionSet(
        max_iterations=40, per_condition_timeout=60, per_path_timeout=5
    )
    fn = getattr(sys.modules[__name__], fn_name)
    messages = run_checkables(analyze_function(fn, opts))
    errors = [m for m in messages if m.state > MessageType.PRE_UNSAT]
    assert errors == []
