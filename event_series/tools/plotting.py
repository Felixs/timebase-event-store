import io
from typing import List, Tuple

from matplotlib import pyplot as plt
from matplotlib.figure import Figure


def image_bytes_from_event_value(name: str, data: List[Tuple[int, str]]):
    if not data:
        raise ValueError("No data to plot")
    figure, axis = plt.subplots()
    figure.suptitle(name)
    for entry in data:
        axis.plot(entry[0], entry[1])
    return save_figure_to_bytes(figure)


def save_figure_to_bytes(figure: Figure):
    buffer = io.BytesIO()
    figure.savefig(buffer)
    return buffer.getvalue()
