import pytest
import sys
import random

from pathlib import Path
from contextlib import contextmanager
from typing import Callable

EXTREMES = {
        type(None): [None],
        int: [0, 1, -1, sys.maxsize, -sys.maxsize],
        float: [0.0, 1.0, 3.141592653, float('inf'), float('-inf'), float('nan')],
        str: ['', 'a', '\0', '\xff', 'A'*1000],
        bytes: [b'', b'a', b'\0', b'\xff', b'A'*1000],
        list: [[], [[]], [[], []], [0], [[0]], [[] * 100]],
        tuple: [(), ((),), ((), ()), ((), (0,)), ((0),)]
}

@contextmanager
def not_raises(ex):
    """ Check that it doesn't raise the given exception """
    try:
        yield
    except ex as e:
        raise AssertionError()
    except Exception:
        pass

def test_type_combs(func: Callable,
                    num_required: int,
                    num_default: int,
                    types: list,
                    max_tries: int = 50,
                    no_correct: bool = True):
    """
    Test a function with extreme combinations of types

    Args:
        func (Callable): function to test
        num_required (int): number of required parameters
        num_default (int): number of default parameters
        types (list): list of types of parameters
        max_tries (int): maximum number of tries (default: 50)
        no_correct (bool): if True test for all incorrect only combinations

    Raises:
        TypeError: if any argument is of the wrong type
        ValueError: if `num_required` or `num_default` are negative
        ValueError: if the sum of `num_required` and `num_default` doesn't equal the length of `types`
        Warning: if a type from `types` is missing from the predefined ones
    """

    if not isinstance(func, Callable) or not isinstance(types, list) \
            or not all(isinstance(x, int) for x in (num_required, num_default, max_tries)):
        raise TypeError("Wrong types for arguments")

    if num_required < 0 or num_default < 0:
        raise ValueError("Invalid values for `num_required` or `num_default`")

    if len(types) != num_required + num_default:
        raise ValueError("Wrong length for `types`")

    if no_correct:
        # all incorrect
        with pytest.raises(TypeError):
            func(*([object()] * len(types)))
        return

    if not all(k in EXTREMES.keys() for k in types):
        raise Warning("Check `types` or add to EXTREMES variable")

    max_tries = max(max_tries, 5)

    allowed = {k: EXTREMES[k] for k in types}

    # all incorrect
    with pytest.raises(TypeError):
        func(*([object()] * len(types)))

    # all correct
    with not_raises(TypeError):
        for _ in range(max_tries):
            args = [random.choice(allowed[t]) for t in types]
            print(args)
            func(*args)

    # one required incorrect
    with pytest.raises(TypeError):
        if num_required > 0:
            for _ in range(max_tries):
                args = [random.choice(allowed[t]) for t in types]
                idx = random.randrange(num_required)
                args[idx] = object()
                func(*args)
        else:
            func(object(), *[random.choice(allowed[t]) for t in types])

    # one default incorrect
    with pytest.raises(TypeError):
        if num_default > 0:
            for _ in range(max_tries):
                args = [random.choice(allowed[t]) for t in types]
                idx = num_required + random.randrange(num_default)
                args[idx] = object()
                func(*args)
        else:
            func(*[random.choice(allowed[t]) for t in types], object())

