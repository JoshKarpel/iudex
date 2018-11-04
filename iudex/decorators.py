import textwrap
import inspect

from . import exceptions


def pre(test):
    def wrapper(func):
        if not isinstance(func, Judge):
            func = Judge(func)

        func._add_pre(test)

        return func

    return wrapper


def post(test):
    def wrapper(func):
        if not isinstance(func, Judge):
            func = Judge(func)

        func._add_post(test)

        return func

    return wrapper


def invariant(test):
    def wrapper(func):
        if not isinstance(func, Judge):
            func = Judge(func)

        func._add_invariant(test)

        return func

    return wrapper


class Judge:
    def __init__(self, func):
        self.func = func

        self.signature = inspect.signature(func)
        self.positional_arg_indices_by_name = {
            name: idx
            for idx, (name, param)
            in enumerate(self.signature.parameters.items())
        }

        self.pre_tests = []
        self.post_tests = []
        self.invariants = []

    def __call__(self, *args, **kwargs):
        self._run_pre_tests(args, kwargs)

        invariants_before = {}
        for inv in self.invariants:
            sig = inspect.signature(inv)
            vals = tuple(
                kwargs.get(param, self.signature.parameters[param].default)
                if param in kwargs
                else args[self.positional_arg_indices_by_name[param]]
                for param in sig.parameters
            )
            invariants_before[inv] = inv(*vals)

        rv = self.func(*args, **kwargs)

        self._run_post_tests(args, kwargs, rv)

        for inv in self.invariants:
            sig = inspect.signature(inv)
            vals = []
            for param in sig.parameters:
                if param == 'rv':
                    vals.append(rv)
                elif param in kwargs:
                    vals.append(kwargs.get(param, self.signature.parameters[param].default))
                else:
                    vals.append(args[self.positional_arg_indices_by_name[param]])
            invariant_after = inv(*vals)
            if invariants_before[inv] != invariant_after:
                info = build_test_failed_msg(inv, self.signature, vals)
                raise exceptions.InvariantViolated(
                    '\n'.join((
                        f'Invariant violated for function {self.func}!\n',
                        info,
                        '\nInvariant value before execution:',
                        f'    {invariants_before[inv]}',
                        '\nInvariant value after execution:',
                        f'    {invariant_after}',
                    ))
                )

        return rv

    def _run_pre_tests(self, args, kwargs):
        for pre_test in self.pre_tests:
            sig = inspect.signature(pre_test)
            vals = tuple(
                kwargs.get(param, self.signature.parameters[param].default)
                if param in kwargs
                else args[self.positional_arg_indices_by_name[param]]
                for param in sig.parameters
            )
            test_passed = pre_test(*vals)
            if not test_passed:
                info = build_test_failed_msg(pre_test, self.signature, vals)
                raise exceptions.TestFailed(f'Pre-execution test for function {self.func} failed!\n\n{info}')

    def _run_post_tests(self, args, kwargs, return_value):
        for post_test in self.post_tests:
            sig = inspect.signature(post_test)

            vals = []
            for param in sig.parameters:
                if param == 'rv':
                    vals.append(return_value)
                elif param in kwargs:
                    vals.append(kwargs.get(param, self.signature.parameters[param].default))
                else:
                    vals.append(args[self.positional_arg_indices_by_name[param]])
            test_passed = post_test(*vals)
            if not test_passed:
                info = build_test_failed_msg(post_test, self.signature, vals)
                raise exceptions.TestFailed(f'Post-execution test for function {self.func} failed!]\n\n{info}')

    def _add_pre(self, test):
        self.pre_tests.append(test)

    def _add_post(self, test):
        self.post_tests.append(test)

    def _add_invariant(self, test):
        self.invariants.append(test)


def build_test_failed_msg(test, signature, values):
    file = inspect.getsourcefile(test)
    source, lineno = get_source_of_test(test)

    msg_lines = [
        f'Test: line {lineno} in {file}',
        textwrap.indent(source, prefix = ' ' * 4).rstrip(),
        f'\nParameters:',
        textwrap.indent(
            '\n'.join(f'{param} = {val}' for param, val in zip(signature.parameters, values)),
            prefix = ' ' * 4,
        ),
    ]

    return '\n'.join(msg_lines)


def get_source_of_test(test):
    raw, lineno = inspect.getsourcelines(test)
    if 'def' in raw[0]:
        return ''.join(raw), lineno
    return take_until_paren_balanced(''.join(raw)), lineno


def take_until_paren_balanced(string):
    open_count = 0
    has_opened = False
    output = []
    for char in string:
        output.append(char)
        if char == '(':
            open_count += 1
            has_opened = True
        elif char == ')':
            open_count -= 1

        if has_opened and open_count == 0:
            break

    return ''.join(output)
