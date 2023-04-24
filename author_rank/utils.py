from collections import Counter
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

    try:
        z = (value - minimum) / (maximum - minimum)

    # this error occurs when the minimum and maximum of a set of scores are identical to one another
    # this situation may arise when all of the authors are evenly scored as a result of AuthorRank
    # in this situation, set all of their scores to 1.0
    except ZeroDivisionError:
        z = 1.

    return z


def emit_progress_bar(progress: str, index: int, total: int, percent_offset: float = 1e-9) -> str:
    """
    A progress bar that is continuously updated in Python's standard
    out.
    :param progress: a string printed to stdout that is updated and later
    returned.
    :param index: the current index of the iteration within the tracked
    process.
    :param total: the total length of the tracked process.
    :param percent_offset: an offset in which to start the progress bar. 0.5 starts the
    progress bar at 50%.
    :return: progress string.
    """

    w, h = get_terminal_size()
    if percent_offset > 1e-9:
        w = w * 0.5
    sys.stdout.write("\r")

    if total < w:
        block_size = int(w / total)
    else:
        block_size = int(total / w)

    if index % block_size == 0:
        progress += "="

    percent = index / total
    if percent_offset > 1e-9:
        percent_inverse = percent_offset ** -1
        percent = percent_offset + (index / (total * percent_inverse))

    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()

    return progress


def check_author_count(counter: Counter) -> bool:
    """
    Takes a set of documents and counts the number of authors. If less than
    2, returns False otherwise True.
    :param counter: a Counter object for author counts.
    :return: a boolean indicating whether or not the document set can be
    analyzed (True for yes, no for False).
    """

    if len(counter) == 1:
        return False
    return True
