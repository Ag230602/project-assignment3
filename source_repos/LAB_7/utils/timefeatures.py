import numpy as np
import pandas as pd

def time_features(dates, freq='h'):
    dates = pd.to_datetime(dates)
    return np.stack([
        dates.month.to_numpy() / 12.0,
        dates.day.to_numpy() / 31.0,
        dates.weekday.to_numpy() / 7.0,
        dates.hour.to_numpy() / 24.0
    ], axis=1)
