import pandas as pd
import matplotlib.pyplot as plt


class TimeSeriesHelper:
    def __init__(self):
        self.ts = None

    def to_timeseries(
        self, df, datetime_col, count_col, freq="D", agg_method="sum", date_format=None
    ):
        """
        Convert DataFrame to time series.
        :param df: Pandas DataFrame containing the data.
        :param datetime_col: Name of the column with datetime data.
        :param count_col: Name of the column with count data.
        :param freq: Frequency for resampling ('D' for day, 'M' for month, 'Y' for year).
        :param agg_method: Method for aggregation (sum, mean, etc.).
        :param date_format: The format of the dates in the datetime_col.
        """
        # Convert the datetime column based on the specified format
        if date_format:
            df[datetime_col] = pd.to_datetime(df[datetime_col], format=date_format)
        else:
            df[datetime_col] = pd.to_datetime(df[datetime_col])

        # Set the datetime column as the index
        df.set_index(datetime_col, inplace=True)

        # Resample and aggregate
        if agg_method == "sum":
            self.ts = df[count_col].resample(freq).sum()
        elif agg_method == "mean":
            self.ts = df[count_col].resample(freq).mean()
        # More aggregation methods can be added here

        return self.ts

    def plot_timeseries(self, figsize=(10, 6), title="Time Series Plot", color="blue"):
        """
        Plot the time series with custom color.
        :param figsize: Size of the figure.
        :param title: Title of the plot.
        :param color: Color of the line plot.
        """
        if self.ts is not None:
            ax = self.ts.plot(kind="line", figsize=figsize, color=color)
            ax.set_xlabel("Date")
            ax.set_ylabel("Count")
            ax.set_title(title)

            # Rotate x-axis labels
            plt.xticks(rotation=45)

            # Remove the top, left, and right spines
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)

            # Set gridlines
            ax.yaxis.grid(True)  # Horizontal grid
            ax.xaxis.grid(False)  # No vertical grid

            plt.show()
        else:
            print("No time series data available. Please run to_timeseries first.")

    def fill_missing(self, method="ffill"):
        """
        Fill missing values in time series.
        """
        if self.ts is not None:
            self.ts.fillna(method=method, inplace=True)
        else:
            print("No time series data available. Please run to_timeseries first.")

    # Example usage:
    # ts_helper = TimeSeriesHelper()
    # ts_helper.to_timeseries(df, 'datetime_col', 'count_col', 'M', 'mean')
    # ts_helper.fill_missing('bfill')
    # ts_helper.plot_timeseries(figsize=(12, 8), title='Monthly Mean Count')
    # ts_helper.decompose_timeseries(model='multiplicative', freq=12)
