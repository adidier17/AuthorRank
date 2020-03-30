def normalize(minimum: float, maximum: float, value: float) -> float:
    """
    Takes a minimum, maximum, and input value and converts the input
    value to a normalized value on a scale from 0 to 1.
    :param minimum: the minimum value from the set of values containing the input value
    :param maximum: the maximum value from the set of values containing the input value
    :param value: the input value to be converted to a normalized value
    :return: a normalized that lies on the scale from [0, 1]
    """

    z = (value - minimum) / (maximum - minimum)

    return z

