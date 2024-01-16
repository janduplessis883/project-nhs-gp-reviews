import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


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
        :param agg_method: Method for aggregation (sum, mean, count,etc.).
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
        elif agg_method == "count":
            self.ts = df[count_col].resample(freq).count()
        # More aggregation methods can be added here

        return self.ts

    def plot_timeseries(
        self,
        package="seaborn",
        figsize=(10, 6),
        title="Time Series Plot",
        color="blue",
        line_thickness=4,
    ):
        """
        Plot the time series with custom color.
        :param package: The plotting package to use ('seaborn' or 'plotly').
        :param figsize: Size of the figure.
        :param title: Title of the plot.
        :param color: Color of the line plot.
        """
        if self.ts is not None:
            if package == "seaborn":
                # Create a figure and axis with Matplotlib
                fig, ax = plt.subplots(figsize=figsize)

                # Use Seaborn to create the line plot on the created axis
                sns.lineplot(ax=ax, data=self.ts, color=color, linewidth=line_thickness)

                ax.set_xlabel("Date")
                ax.set_ylabel("Count")
                ax.set_title(title)

                # Customize spines and gridlines
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["left"].set_visible(False)
                ax.yaxis.grid(
                    True, linestyle="--", linewidth=0.5, color="#888888", alpha=0.8
                )
                ax.xaxis.grid(
                    True, linestyle="--", linewidth=0.5, color="#888888", alpha=0.8
                )

                plt.show()

            elif package == "plotly":
                # Use Plotly to create the line plot
                fig = px.line(
                    self.ts, y=self.ts.name, title=title, template="plotly_white"
                )

                # Customize the plotly figure
                fig.update_traces(line=dict(color=color, width=line_thickness))
                fig.update_layout(
                    xaxis_title="Date", yaxis_title="Count", plot_bgcolor="white"
                )

                fig.show()
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
