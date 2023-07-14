import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def add_timeseries(ax, ts, color="green", name="time series", showlegend=False):
    timestamps = ts.index
    ax.plot(timestamps, ts[ts.columns[0]], color=color, label=(name if showlegend else '_nolegend_'))

def plot_timeseries(ts, color="green", ax=None, name="time series"):
    showlegend = True
    if type(ts) == dict:
        data = ts
        if type(color) == str:
            color = {k: color for k in data}
    elif type(ts) == list:
        data = {}
        for k, ts_data in enumerate(ts):
            data[k] = ts_data
        if type(color) == str:
            color = {k: color for k in data}
    else:
        data = {}
        data["default"] = ts
        color = {"default": color}

    if ax is None:
        fig, ax = plt.subplots()

    first = True
    for key, ts in data.items():
        if not first:
            showlegend = False

        add_timeseries(ax, ts, color=color[key], showlegend=showlegend, name=name)
        first = False

    return ax

def plot_tsice_explanation(explanation, forecast_horizon):
    original_ts = pd.DataFrame(explanation["data_x"])
    perturbations = explanation["perturbations"]
    forecasts_on_perturbations = explanation["forecasts_on_perturbations"]

    new_perturbations = []
    new_timestamps = []
    pred_ts = []

    original_ts.index.freq = pd.infer_freq(original_ts.index)
    for i in range(1, forecast_horizon + 1):
        new_timestamps.append(original_ts.index[-1] + (i * original_ts.index.freq))

    for perturbation in perturbations:
        new_perturbations.append(pd.DataFrame(perturbation))

    for forecast in forecasts_on_perturbations:
        pred_ts.append(pd.DataFrame(forecast, index=new_timestamps))

    pred_original_ts = pd.DataFrame(
        explanation["current_forecast"], index=new_timestamps
    )

    fig, ax = plt.subplots()

    # Plot perturbed time series
    ax = plot_timeseries(new_perturbations, color="lightgreen", ax=ax, name="perturbed timeseries samples")

    # Plot original time series
    ax = plot_timeseries(original_ts, color="green", ax=ax, name="input/original timeseries")

    # Plot varying forecast range
    ax = plot_timeseries(pred_ts, color="lightblue", ax=ax, name="forecast on perturbed samples")

    # Plot original forecast
    ax = plot_timeseries(pred_original_ts, color="blue", ax=ax, name="original forecast")

    # Set labels and title
    ax.set_xlabel("Month/Year")
    ax.set_ylabel("sunspots")
    ax.set_title("Time Series Individual Conditional Expectation (TSICE) Plot")

    ax.legend()

    # Display the plot
    plt.show()

    # Return the figure
    return fig


def plot_tsice_with_observed_features(explanation, feature_per_row=2):
    df = pd.DataFrame(explanation["data_x"])
    n_row = int(np.ceil(len(explanation["feature_names"]) / feature_per_row))
    feat_values = np.array(explanation["feature_values"])

    fig, axs = plt.subplots(n_row, feature_per_row, figsize=(15, 15))
    axs = axs.ravel()  # Flatten the axs to iterate over it

    for i, feat in enumerate(explanation["feature_names"]):
        x_feat = feat_values[i, :, 0]
        trend_fit = LinearRegression()
        trend_line = trend_fit.fit(x_feat.reshape(-1, 1), explanation["signed_impact"])
        x_trend = np.linspace(min(x_feat), max(x_feat), 101)
        y_trend = trend_line.predict(x_trend[..., np.newaxis])

        # Scatter plot
        axs[i].scatter(x=x_feat, y=explanation["signed_impact"], color='blue')
        # Line plot
        axs[i].plot(x_trend, y_trend, color="green", label="correlation between forecast and observed feature")
        # Reference line
        current_value = explanation["current_feature_values"][i][0]
        axs[i].axvline(x=current_value, color='firebrick', linestyle='--', label="current value")

        axs[i].set_xlabel(feat)
        axs[i].set_ylabel('Δ forecast')

    # Display the legend on the first subplot
    axs[0].legend()

    fig.suptitle("Impact of Derived Variable On The Forecast", fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    return fig

def plot_ts(df, df_timestamps, df_timestamp_name, df_targets, df_description):
    n_targets = len(df_targets)

    fig, axs = plt.subplots(n_targets, 1, figsize=(10, 5 * n_targets))

    # In case there's only one target, make sure axs is a list
    if n_targets == 1:
        axs = [axs]

    for ax, target in zip(axs, df_targets):
        ax.plot(df_timestamps, df[target], color="black", label=target)
        ax.set_xlabel(df_timestamp_name)
        ax.set_ylabel(target)
        ax.set_title(f"[target] {target}")
        ax.legend()

    fig.suptitle(df_description)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    return fig
