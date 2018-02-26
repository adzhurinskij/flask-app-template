# -*- coding: utf-8 -*-


def to_boolean(var):
    """Check boolean and return value."""
    if var in ("True", "true", "1", True, 1):
        return True
    elif var in ("False", "false", "0", False, 0):
        return False
    else:
        raise ValueError("Expected boolean value.")


def split_args(var):
    return [ item.strip() for item in var.split(',') ]
