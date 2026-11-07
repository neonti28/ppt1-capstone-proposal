import pandas as pd
import numpy as np

# Repro hipotesis: DataFrame.insert dengan Series ber-index DatetimeIndex
# ke DataFrame ber-index integer -> NaN (alignment), vs numpy array -> aman.
df = pd.DataFrame({"a": [10, 11, 12]}, index=[0, 1, 2])  # index integer
ser = pd.Series([100.0, 110.0, 120.0],
                index=pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-03"]))
df.insert(0, "from_series", ser)
df.insert(1, "from_numpy", np.array([1, 2, 3]))
print(df)
print("series_nan:", df["from_series"].isna().sum(), "/ 3")
