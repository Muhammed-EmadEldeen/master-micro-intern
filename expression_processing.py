from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
import re
import math


def evaluate_expression_sympy(expression: str, x_value: float):
    """
    Evaluate a mathematical expression given x value
    params:
        expression: str: mathematical expression
    returns:
        result: float: result of the expression
    """

    x = symbols('x')

    # Replace custom functions with sympy equivalents
    expression = replace_log10_with_log_base_10(expression)
    expression = expression.replace('^', '**')

    try:
        # Convert string expression to a sympy expression
        expr = parse_expr(expression)

        # Substitute the value of x and evaluate
        result = expr.evalf(subs={x: x_value})
        return result
    except Exception as e:
        return f"Error evaluating expression: {e}"


def replace_log10_with_log_base_10(expression: str) -> str:
    """
    Replace all instances of 'log10' in the expression with 'log(..., 10)'.
    """
    # Regular expression to find 'log10' followed by parentheses containing any character
    pattern = r'log10\(([^)]+)\)'

    # Replace 'log10(x)' with 'log(x, 10)'
    result = re.sub(pattern, r'log(\1, 10)', expression)

    return result


def get_x_values(min: float, max: float) -> np.ndarray:
    x_values = np.linspace(min, max, int(
        (500/math.log(100))*math.log(abs(max-min))))
    return x_values


operators = ['/', '^', '*', '+', '-']


def inspect_equation(expression: str) -> tuple:
    """
    Inspect the expression for validity
    """

    expression = expression.replace(" ", "")

    if expression == "":
        return False, "Empty expression"

    if expression[0] in operators or expression[-1] in operators:
        return False, "Expression cannot start or end with an operator"

    status, message = valid_characters(expression)
    if not status:
        return status, message

    status, message = wrong_format(expression)
    if not status:
        return status, message

    status, message = bracket_check(expression)
    if not status:
        return status, message

    return True, "Expression is valid"


def bracket_check(expression: str) -> tuple:
    """
    Check if brackets are balanced
    """
    open_brackets = 0
    close_brackets = 0

    for i in range(len(expression)):
        if expression[i] == '(':
            open_brackets += 1
        elif expression[i] == ')':
            close_brackets += 1
            if close_brackets > open_brackets:
                return False, "Close Bracket cannot be more than open brackets"

    if open_brackets != close_brackets:
        return False, "Number of open brackets must be equal to number of close brackets"

    return True, "Expression is valid"


def valid_characters(expression: str) -> tuple:
    """
    Check if expression contains invalid characters
    """

    pattern = r'^([0-9\s+\-*/()x\^]+|log10\(|sqrt\()*$'
    if not re.fullmatch(pattern, expression):
        return False, "Invalid characters in expression"

    return True, "Expression is valid"


def wrong_format(expression: str) -> tuple:
    """
    Check if expression is in the right format
    """

    for i in range(1, len(expression)):
        status, message = valid_preceding_char(expression, i)
        if not status:
            return False, message

    for i in range(len(expression)-1):
        status, message = valid_following_char(expression, i)
        if not status:
            return False, message

    return True, "Expression is valid"


def valid_preceding_char(expression, i):
    """
    Check if the character preceding the current character is valid
    """

    if expression[i] == 'l':
        if expression[i-1] not in operators+['(']:
            return False, "log10 must be preceded by an operator"

    elif expression[i] == 's':
        if expression[i-1] not in operators+['(']:
            return False, "sqrt must be preceded by an operator"

    elif expression[i] == 'x':
        if expression[i-1] not in operators+['(']:
            return False, "x must be preceded by an operator"

    elif expression[i] == '(':
        if expression[i-1] not in operators+['0', 't', '(']:
            return False, "Open Bracket must be preceded by an operator"

    elif expression[i] == ')':
        if expression[i-1] in operators:
            return False, "Close Bracket cannot be preceded by an operator"

    return True, "Expression is valid"


def valid_following_char(expression, i):
    """
    Check if the character following the current character is valid
    """

    if expression[i] in operators and expression[i+1] in operators:
        return False, "Two operators cannot be adjacent"

    elif expression[i] == 'x':
        if expression[i+1] not in operators+[')']:
            return False, "x must be followed by an operator"

    elif expression[i] == '(':
        if expression[i+1] in operators:
            return False, "Open Bracket Cannot be followed by an operator"

    elif expression[i] == ')':
        if expression[i+1] not in operators+[')']:
            return False, "Close Bracket must be followed by an operator"

    return True, "Expression is valid"
