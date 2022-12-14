import pandas as pd
import pandera as pa


columns_schema = {
    "datetime": pa.Column(
        dtype=str,
        nullable=False,
        required=True,
        coerce=True,
        unique=False,
    ),
    "plate_no": pa.Column(
        dtype=str,
        nullable=False,
        required=True,
        coerce=True,
        unique=False,
    ),
    "lat": pa.Column(
        dtype=float,
        nullable=False,
        required=True,
        coerce=True,
        unique=False,
    ),
    "lon": pa.Column(
        dtype=float,
        nullable=False,
        required=True,
        coerce=True,
        unique=False,
    ),
    "computed_velocity": pa.Column(
        dtype=float,
        nullable=False,
        required=True,
        coerce=True,
        unique=False,
    ),
    "cluster_id": pa.Column(
        dtype=int,
        nullable=False,
        required=True,
        coerce=True,
        unique=False,
    ),
    "lat_centroid": pa.Column(
        dtype=float,
        nullable=True,
        required=True,
        coerce=True,
        unique=False,
    ),
    "lon_centroid": pa.Column(
        dtype=float,
        nullable=True,
        required=True,
        coerce=True,
        unique=False,
    ),
    "service_start_time": pa.Column(
        dtype=str,
        nullable=True,
        required=True,
        coerce=True,
        unique=False,
    ),
    "service_end_time": pa.Column(
        dtype=str,
        nullable=True,
        required=True,
        coerce=True,
        unique=False,
    ),
    "service_duration": pa.Column(
        dtype=float,
        nullable=True,
        required=True,
        coerce=True,
        unique=False,
    ),
}

gps_visualization_schema = pa.DataFrameSchema(
    columns=columns_schema,
    coerce=True,
    description="Data provided from customer excel file",
)


def validate_visualization_schema(gps: pd.DataFrame) -> pd.DataFrame:
    gps[["service_start_time", "service_end_time"]] = \
        gps[["service_start_time", "service_end_time"]].fillna("")
    gps = gps_visualization_schema.validate(gps)
    gps = gps.loc[:, list(gps_visualization_schema.columns.keys())]
    return gps
