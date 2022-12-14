"""
# My first app
Here's our first attempt at using data to create a table:
"""
import io
import os
import sys
import typing as tp

from keplergl import KeplerGl
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


PROJECT_DIR = os.getcwd()
if PROJECT_DIR not in sys.path:
    sys.path.append(PROJECT_DIR)

from src import configs  # noqa: E402,I100
from src import clustering_models  # noqa: E402,I100
from src import models  # noqa: E402,I100

st.set_page_config(
    page_icon="🚛",
    page_title="GPS clustering",
    layout="wide",
    initial_sidebar_state="expanded",
)


class Dashboard:

    @staticmethod
    def decode_uploader_csv_content(
            file_uploader_widget: st.runtime.uploaded_file_manager.UploadedFile,
    ) -> tp.Union[pd.DataFrame, None]:
        widget_content = file_uploader_widget.getvalue()
        widget_string_content = widget_content.decode("utf-8")
        df = pd.read_csv(
            io.StringIO(widget_string_content),
            delimiter=',',
            dtype=str,
        )
        return df

    @staticmethod
    def aggregate_clusters(gps: pd.DataFrame) -> pd.DataFrame:
        clusters = gps \
            .groupby(["route_id", "cluster_id"]) \
            .agg(
                lat_centroid=("lat", "mean"),
                lon_centroid=("lon", "mean"),
                service_start_time=("datetime", "min"),
                service_end_time=("datetime", "max"),
                unix_start_time=("unixtime", "min"),
                unix_end_time=("unixtime", "max"),
            ).reset_index()
        clusters = clusters[clusters["cluster_id"] != -1.0].reset_index(drop=True)
        clusters["service_duration"] = clusters["unix_end_time"] - clusters["unix_start_time"]
        clusters.drop(columns=["unix_start_time", "unix_end_time"], inplace=True)
        return clusters

    @staticmethod
    def join_clusters_to_gps(
            gps: pd.DataFrame,
            clusters: pd.DataFrame,
    ) -> pd.DataFrame:
        return gps.merge(clusters, how="left")

    @staticmethod
    def render_map(gps: pd.DataFrame):
        kepler_map = KeplerGl(
            data={"gps": gps.fillna("")},
            height=configs.MAP_HEIGHT,
            config=configs.kepler_map_config,
        )
        html = kepler_map._repr_html_(center_map=True, read_only=True)
        components.html(html, height=configs.MAP_HEIGHT)


def render_dashboard():

    st.write(configs.heading)
    file_uploader_widget = st.file_uploader(
        label="Upload your gps file here",
        type=["csv"],
        accept_multiple_files=False,
        key=None,
        help="Helper widget",
        on_change=None,
        disabled=False,
        label_visibility="visible",
    )

    if file_uploader_widget is not None:
        gps_records = Dashboard.decode_uploader_csv_content(file_uploader_widget)
        gps_records = clustering_models.vfhdbscan.predict(gps_records)
        agg_clusters = Dashboard.aggregate_clusters(gps_records.copy())
        gps_records = Dashboard.join_clusters_to_gps(gps=gps_records, clusters=agg_clusters)
        gps_records = models.validate_visualization_schema(gps_records)
        Dashboard.render_map(gps_records)
        st.dataframe(agg_clusters.rename(columns={"service_duration": "service_duration (seconds)"}))


render_dashboard()
