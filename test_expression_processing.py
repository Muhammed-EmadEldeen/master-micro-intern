import pytest
import math
from expression_processing import evaluate_expression_sympy, get_x_values, inspect_equation, bracket_check, valid_characters, wrong_format


def test_evaluate_expression_sympy():
    assert int(evaluate_expression_sympy("x+2", 3)) == 5
    assert int(evaluate_expression_sympy("x^2", 4)) == 16
    assert int(evaluate_expression_sympy("log10(x)", 1)) == 0
    assert math.isclose(evaluate_expression_sympy(
        "sqrt((x^2)*log10(x))", 4), 3.1, rel_tol=0.2)
    assert "Error evaluating expression" in evaluate_expression_sympy("x +", 3)


def test_get_x_values():
    x_values = get_x_values(0, 10)
    assert len(x_values) > 0
    assert x_values[0] == 0
    assert x_values[-1] == 10


def test_inspect_equation():

    assert inspect_equation("x + 2") == (True, "Expression is valid")
    assert inspect_equation("") == (False, "Empty expression")
    assert inspect_equation(
        "+ 2") == (False, "Expression cannot start or end with an operator")
    assert inspect_equation("x ++ 2") == (False,
                                          "Two operators cannot be adjacent")
    assert inspect_equation("x ( 2") == (
        False, "Open Bracket must be preceded by an operator")


def test_bracket_check():
    assert bracket_check("(x + 2)") == (True, "Expression is valid")
    assert bracket_check(
        "((x + 2)") == (False, "Number of open brackets must be equal to number of close brackets")
    assert bracket_check("(x + 2))") == (False,
                                         "Close Bracket cannot be more than open brackets")


def test_valid_characters():
    assert valid_characters("x + 2") == (True, "Expression is valid")
    assert valid_characters("x + 2 @") == (False,
                                           "Invalid characters in expression")
    assert valid_characters("log10x + 2") == (False,
                                              "Invalid characters in expression")


def test_wrong_format():
    assert wrong_format("x+2") == (True, "Expression is valid")
    assert wrong_format("x++2") == (False,
                                    "Two operators cannot be adjacent")
    assert wrong_format("x sqrt2") == (
        False, "sqrt must be preceded by an operator")


if __name__ == "__main__":
    pytest.main()
