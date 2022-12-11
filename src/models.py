import pandera as pa


raw_plan = pa.DataFrameSchema({
    "編號": pa.Column(str, coerce=True, nullable=True),
    "需要/ 預算到達時間/ 時段": pa.Column(str, coerce=True, nullable=True),
    "CRN#": pa.Column(str, coerce=True, nullable=True),
    "聯絡人": pa.Column(str, coerce=True, nullable=True),
    "聯絡電話": pa.Column(str, coerce=True, nullable=True),
    "地址": pa.Column(str, coerce=True, nullable=True),
    "回收電器或數量": pa.Column(str, coerce=True, nullable=True),
    "truck code": pa.Column(str, coerce=True, nullable=True),
    "date": pa.Column(str, coerce=True, nullable=True),
    "truck type": pa.Column(str, coerce=True, nullable=True),
    "re-assigned by Ricky": pa.Column(str, coerce=True, nullable=True),
    "CXL order": pa.Column(str, coerce=True, nullable=True),
    "備註2 by SC": pa.Column(str, coerce=True, nullable=True),
    "備註3": pa.Column(str, coerce=True, nullable=True),
})


plan_with_geocode = pa.DataFrameSchema({
    "編號": pa.Column(str, coerce=True, nullable=True),
    "需要/ 預算到達時間/ 時段": pa.Column(str, coerce=True, nullable=True),
    "CRN#": pa.Column(str, coerce=True, nullable=True),
    "聯絡人": pa.Column(str, coerce=True, nullable=True),
    "聯絡電話": pa.Column(str, coerce=True, nullable=True),
    "address": pa.Column(str, coerce=True, nullable=True),
    "回收電器或數量": pa.Column(str, coerce=True, nullable=True),
    "truck code": pa.Column(str, coerce=True, nullable=True),
    "date": pa.Column(str, coerce=True, nullable=True),
    "truck type": pa.Column(str, coerce=True, nullable=True),
    "re-assigned by Ricky": pa.Column(str, coerce=True, nullable=True),
    "CXL order": pa.Column(str, coerce=True, nullable=True),
    "備註2 by SC": pa.Column(str, coerce=True, nullable=True),
    "備註3": pa.Column(str, coerce=True, nullable=True),
    "lat": pa.Column(float, coerce=True, nullable=True),
    "lng": pa.Column(float, coerce=True, nullable=True),
})
