def safe_cast(value, to, default=None):
    """
    Attempts casting `value` into the type `to`.

    Returns `default` if this fails.
    """

    try:
        return to(value)
    except (ValueError, TypeError):
        return default