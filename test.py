from datetime import date, datetime
from pathlib import Path

import matplotlib.pylab as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(data_dir: Path) -> pd.DataFrame:
    body_frames = [
        pd.read_csv(
            fname,
            converters={
                0: lambda x: datetime.strptime(x, "%Y-%m-%d").date().toordinal()
            },
            skiprows=1,
        )
        for fname in data_dir.glob("*.csv")
    ]
    body_frame = pd.concat(body_frames)
    return body_frame


def calculate_extra_data_points(data_frame: pd.DataFrame) -> pd.DataFrame:
    data_frame["Fat Mass"] = data_frame["Weight"] * (data_frame["Fat"] / 100)
    data_frame["Lean Percentage"] = 100 - data_frame["Fat"]
    data_frame["Lean Mass"] = data_frame["Weight"] - data_frame["Fat Mass"]
    return data_frame


def fix_x_axis():
    axis = plt.gca()
    tick_labels = axis.get_xticks()
    axis.set_xticklabels([date.fromordinal(int(dt)) for dt in tick_labels], rotation=30)


def generate_plot(data: pd.DataFrame, data_point: str, output_dir: Path) -> None:
    sns.set(color_codes=True)
    figsize = (len(data) / 12, len(data) / 36)
    print(f"Generating {data_point.lower()} plot...")
    # data_plot = sns.lmplot(
    #     x="Date",
    #     y=data_point,
    #     data=data,
    #     lowess=True,
    #     height=10,
    #     aspect=3,
    #     truncate=True,
    #     scatter_kws={"s": 100},
    # )
    plt.figure(figsize=figsize)
    axes = sns.regplot(
        x="Date",
        y=data_point,
        data=data,
        x_estimator=np.mean,
        logx=True,
        n_boot=10,
        y_jitter=0.01,
    )
    data_plot = axes.get_figure()
    print(f"Fixing {data_point.lower()} plot axis labels...")
    fix_x_axis()
    print(f"Saving {data_point.lower()} plot...")
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    data_plot.savefig(output_dir / f"{data_point.lower().replace(' ', '_')}.png")


if __name__ == "__main__":
    data_dir = Path(".") / "data"
    output_dir = Path(".") / "graphs"
    body_frame = calculate_extra_data_points(load_data(data_dir))
    generate_plot(body_frame, "Weight", output_dir)
    generate_plot(body_frame, "Fat", output_dir)
    generate_plot(body_frame, "Fat Mass", output_dir)
    generate_plot(body_frame, "Lean Percentage", output_dir)
    generate_plot(body_frame, "Lean Mass", output_dir)
