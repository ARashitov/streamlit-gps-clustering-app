import logging
from typing import Dict, Optional

import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline


class JunkRecordFilter(BaseEstimator, TransformerMixin):
    """
    Drops junk records which exceeding # max_missing_tolerance
    """

    def __init__(self, n_max_missing_tolerance: int = 5):
        self.n_max_missing_tolerance = n_max_missing_tolerance

    def fit(self, X, y=None):
        return self

    def __drop_head_junk_records(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[~(df.isna().T.sum() > self.n_max_missing_tolerance)]
        df.reset_index(drop=True, inplace=True)
        return df

    def transform(self, X):
        X = self.__drop_head_junk_records(X)
        return X


class GPSDateTimeFormatter(BaseEstimator, TransformerMixin):
    """
    Drops junk records which exceeding # max_missing_tolerance
    """

    def __init__(
        self,
        colname: str = "datetime",
        input_datetime_format: str = "%Y/%m/%d (%H:%M:%S)",
    ):
        self.input_datetime_format = input_datetime_format
        self.colname = colname

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        try:
            X[self.colname] = pd.to_datetime(X[self.colname], format=self.input_datetime_format)
        except KeyError:
            logging.error(f"{self.colname} is missing")
        return X


class VehicleIdPreprocessor(BaseEstimator, TransformerMixin):
    """
    Drops junk records which exceeding # max_missing_tolerance
    """

    def __init__(self, plate_no_col: str = "plate_no"):
        self.plate_no_col = plate_no_col

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        # pylint: disable-next=W1401
        X[self.plate_no_col] = X[self.plate_no_col].str.replace("\./--|/--", "", regex=True)
        return X


class RoutePrimaryKeyGenerator(BaseEstimator, TransformerMixin):
    """
    Drops junk records which exceeding # max_missing_tolerance
    """

    def __init__(
        self,
        datetime_col: str = "datetime",
        plate_no_col: str = "plate_no",
        route_id_col: str = "route_id",
    ):
        self.datetime_col = datetime_col
        self.plate_no_col = plate_no_col
        self.route_id_col = route_id_col

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        date = X[self.datetime_col].dt.date.astype("str")
        vehicle_id = X[self.plate_no_col]
        X[self.route_id_col] = date + " :: " + vehicle_id
        return X


class EmptyColumnFilter(BaseEstimator, TransformerMixin):
    """
    Drops junk records which exceeding # max_missing_tolerance
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        empty_columns = X.columns[X.isna().all()]
        X = X.drop(columns=empty_columns, errors="ignore")
        return X


class ColumnRenamer(BaseEstimator, TransformerMixin):
    """
    Drops junk records which exceeding # max_missing_tolerance
    """
    # flake8: noqa: B006

    def __init__(
        self,
        rename_params: Dict[str, str] = {
            "日期(時間)": "datetime",
            "Date(time)": "datetime",
            "車牌號碼\n(香港/國內) ": "plate_no",
            "Plate no.\n(HK/PRC)": "plate_no",
            "車隊名稱": "Fleet name",
            "拖架號碼": "BRACKET no",
            "Driver\n(Department)": "driver(department)",
            "司機(部門)": "driver(department)",
            "緯度": "lat",
            "經度": "lon",
            "Latitude": "lat",
            "Longitude": "lon",
            "區域": "Region",
            "地區": "District",
            "分區": "Sub-district",
            "街道": "Street",
            "建築物": "Poi",
            "方向": "Direction",
            "速度\n(公里/小時)": "speed_km_per_hour",
            "Speed\n(km/hr.)": "speed_km_per_hour",
            "狀況": "Status",
            "Reception time\n": "receiving_time_delta_sec",
            "接收時\n間差(秒)": "receiving_time_delta_sec",
            "Mileage\n(km)": "distance_km",
            "里數(公里)": "distance_km",
            "溫度(℃)": "temperature",
            "重量": "Weight",
            "備註": "Remark",
        },
    ):
        self.rename_params = rename_params

    def fit(self, X, y=None):
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        X = X.rename(columns=self.rename_params)
        return X


def factory_raw_gps_formatter_pipeline() -> Pipeline:
    return Pipeline([
        ('junk_record_filter', JunkRecordFilter()),
        ('column_renamer', ColumnRenamer()),
        ('datetime_formatter', GPSDateTimeFormatter(colname="datetime")),
        ('vehicle_id_preprocessor', VehicleIdPreprocessor()),
        ('route_p_key_generator', RoutePrimaryKeyGenerator()),
        ('empty_columns_filter', EmptyColumnFilter()),
    ])
