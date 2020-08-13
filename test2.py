from datetime import date, datetime
from pathlib import Path
from matplotlib.cbook import ls_mapper

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import MultipleLocator
import matplotlib.dates as mdates

WINDOW_SIZE = 14


def load_data(data_dir: Path) -> pd.DataFrame:
    # Get data from CSV and make it data frames(type)...but called body frame(variable name here)
    body_frames = [pd.read_csv(fname, skiprows=1) for fname in data_dir.glob("*.csv")]
    body_frame = pd.concat(body_frames)
    body_frame["Date"] = pd.to_datetime(body_frame["Date"], format="%Y-%m-%d")
    body_frame = body_frame.sort_values(by="Date")
    #body_frame.set_index("Date")
    return body_frame


def calculate_extra_data_points(data_frame: pd.DataFrame) -> pd.DataFrame:
    # Calculate additional data points for plots
    data_frame["Fat Mass"] = data_frame["Weight"] * (data_frame["Fat"] / 100)
    data_frame["Lean Percentage"] = 100 - data_frame["Fat"]
    data_frame["Lean Mass"] = data_frame["Weight"] - data_frame["Fat Mass"]
    aspects = ["Weight", "Fat", "Fat Mass", "Lean Percentage", "Lean Mass"]
    for aspect in aspects:
        data_frame[f"Average {aspect}"] = data_frame.rolling(window=WINDOW_SIZE).mean()[aspect]
    print(data_frame)
    return data_frame


def fix_x_axis():
    axis = plt.gca()
    tick_labels = axis.get_xticks()
    axis.set_xticklabels([date.fromordinal(int(dt)) for dt in tick_labels], rotation=30)


def generate_plot(data_frame: pd.DataFrame, data_point: str, output_dir: Path) -> None:
    # Generate for each data point passed the following figure format
    figsize = (len(data_frame) / 12, len(data_frame) / 36)
    print(f"Generating {data_point.lower()} plot...")
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot()
    fig.autofmt_xdate()
    myFmt = mdates.DateFormatter('%m-%d')
    ax.xaxis.set_major_locator(MultipleLocator(7))
    ax.xaxis.set_major_formatter(myFmt)
    # how do we add data labels? ax.set_title('fig.autofmt_xdate fixes the labels')
    ax.plot_date(data_frame["Date"], data_frame[data_point], "co")
    ax.plot_date(
        data_frame["Date"], data_frame["Average " + data_point], fmt="g-", linewidth=3)

    print(f"Fixing {data_point.lower()} plot axis labels...")
    # fix_x_axis()
    print(f"Saving {data_point.lower()} plot...")
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    plt.savefig(output_dir / f"{data_point.lower().replace(' ', '_')}.png")
    plt.close()


if __name__ == "__main__":
    data_dir = Path(".") / "data"
    output_dir = Path(".") / "graphs"
    body_frame = calculate_extra_data_points(load_data(data_dir))
    generate_plot(body_frame, "Weight", output_dir)
    generate_plot(body_frame, "Fat", output_dir)
    generate_plot(body_frame, "Fat Mass", output_dir)
    generate_plot(body_frame, "Lean Percentage", output_dir)
    generate_plot(body_frame, "Lean Mass", output_dir)
