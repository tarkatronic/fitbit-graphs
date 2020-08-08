# fitbit-graphs
Generating useful graphs from Fitbit's body data

## Development

### Prerequisites

This project uses Poetry for its dependency and project management. If you have not already, you will need to [install Poetry](https://python-poetry.org/docs/#installation). You will also need at least Python 3.6 in order to work on this project.

### Setup

Once you have your basics set up, getting going is as easy as one command:

```sh
poetry install
```

From here, you should be ready to get working!

### Running things

Everything is still very much in the testing and pre-alpha stage, so files are not in their final places. No tests are in place. No fancy entry points exist yet. To run the code and generates graphs, you will want to do a couple of things.

1. Create a `data/` folder inside the `fitbit-graphs/` folder.
2. Go to https://www.fitbit.com/settings/data/export and export all of your historical data, month by month, from Fitbit.
  a. You will want to be sure to select only the "Body" option under "Include Data", or things will break.
  b. You should use a consistent naming pattern for the files, to keep them separated and organized. I personally name them with the format `body-YYYY-MM.csv`. For example, `body-2020-08.csv`.
  c. You must save the files with a `.csv` file extension, or the scripts will not find them.

Now that your data is all set up and ready, all you need to do to run one of the scripts is:

```sh
poetry run python <script name>
```

For example:

```sh
poetry run python test2.py
```

And voila, you're off to the races!
