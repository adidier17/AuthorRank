from python_utils.terminal import get_terminal_size
import sys


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


def emit_progress_bar(progress: str, index: int, total: int) -> str:
    """
    A progress bar that is continuously updated in Python's standard
    out.
    :param progress: a string printed to stdout that is updated and later
    returned.
    :param index: the current index of the iteration within the tracked
    process.
    :param total: the total length of the tracked process.
    :return: progress string.
    """

    w, h = get_terminal_size()
    sys.stdout.write("\r")
    if total < w:
        block_size = int(w / total)
    else:
        block_size = int(total / w)

    if index % block_size == 0:
        progress += "="
    percent = index / total
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()
    return progress
