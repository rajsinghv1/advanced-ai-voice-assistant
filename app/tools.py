import ast
import math
import operator
from datetime import datetime

from langchain_core.tools import tool


_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _safe_calculate(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
            raise ValueError("Only numeric values are allowed.")
        return node.value

    if isinstance(node, ast.BinOp):
        operation = _ALLOWED_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported mathematical operator.")

        left = _safe_calculate(node.left)
        right = _safe_calculate(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Exponent is too large.")

        result = operation(left, right)

        if not math.isfinite(float(result)) or abs(result) > 1e100:
            raise ValueError("Result is outside the allowed range.")

        return result

    if isinstance(node, ast.UnaryOp):
        operation = _ALLOWED_OPERATORS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported unary operator.")
        return operation(_safe_calculate(node.operand))

    raise ValueError("Invalid mathematical expression.")


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression such as 25 * 4 or (100 + 50) / 2."""
    if not expression or len(expression) > 200:
        return "Please provide a valid expression of up to 200 characters."

    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_calculate(tree.body)
        return f"Result: {result}"
    except (ValueError, TypeError, ZeroDivisionError, OverflowError, SyntaxError) as error:
        return f"Calculation error: {error}"


@tool
def get_current_datetime() -> str:
    """Get the current local date, time, and timezone of this computer."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


TOOLS = [calculator, get_current_datetime]
