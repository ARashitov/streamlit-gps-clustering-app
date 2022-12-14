from gps_activity import ActivityExtractionSession
from gps_activity.extraction.factory.clustering import FDBSCANFactory
from gps_activity.extraction.factory.clustering import STCMFactory
from gps_activity.extraction.factory.fragmentation import VelocityFragmentationFactory
from gps_activity.extraction.factory.preprocessing import PreprocessingFactory


preprocessing = PreprocessingFactory.factory_pipeline(
    source_lat_column="lat",
    source_lon_column="lon",
    source_datetime="datetime",
    source_vehicle_id="plate_no",
    source_crs="EPSG:4326",
    target_crs="EPSG:2326",
)

fragmentation = VelocityFragmentationFactory.factory_pipeline(max_velocity_hard_limit=4)
clustering_fdbscan = FDBSCANFactory.factory_pipeline(
    source_vehicle_id_column="plate_no",
    eps=30,
    min_samples=3,
)

vfhdbscan = ActivityExtractionSession(
    preprocessing=preprocessing,
    fragmentation=fragmentation,
    clustering=clustering_fdbscan,
)

clustering_stcm = STCMFactory.factory_pipeline(
    source_vehicle_id_column="plate_no",
    eps=30,
    min_duration_sec=60,
)

stcm = ActivityExtractionSession(
    preprocessing=preprocessing,
    fragmentation=fragmentation,
    clustering=clustering_stcm,
)
