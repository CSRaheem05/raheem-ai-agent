from datetime import datetime


def calculator(expression: str):
    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:
        return "Invalid calculation"


def current_date():
    return datetime.now().strftime("%Y-%m-%d")