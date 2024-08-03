from typing import List, Optional

from ninja import Schema, ModelSchema
from pydantic import ConfigDict, field_validator

from .models import Track, Circuit


class TrackSchemaIn(Schema):
    description: str
    circuit_id: int

    @field_validator("description")
    def valid_description(cls, description: str) -> str:
        if description and len(description) <= 2:
            raise ValueError("It must be at least 3 characteres long.")
        return description


class TrackSchema(ModelSchema):
    class Meta:
        model = Track
        fields = ["id", "description", "circuit", "started", "finished"]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 42,
                "description": "Track One",
                "circuit": 1,
                "started": "2024-05-11 14:00:00",
                "finished": None,
            }
        },
    )


class ListTracksSchema(Schema):
    tracks: List[TrackSchema]


class CircuitSchema(ModelSchema):
    class Meta:
        model = Circuit
        fields = ["id", "name", "start_line"]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 42,
                "description": "Circuit One",
                "start_line": None,
            }
        },
    )


class ListCircuitsSchema(Schema):
    circuits: List[CircuitSchema]


class PointSchemaIn(Schema):
    latitude: float
    longitude: float
    latLongAccuracy: Optional[float] = None
    heading: Optional[float] = None
    speed: Optional[float] = None
    altitude: Optional[float] = None
    altitudeAccuracy: Optional[float] = None
    dateTime: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "latitude": -28.5048628,
                "longitude": -49.0152924,
                "latLongAccuracy": 2.375,
                "heading": 214.7494354248047,
                "speed": 1.702397193909,
                "altitude": 7.099999904632568,
                "altitudeAccuracy": None,
                "dateTime": "2024-05-11 14:00:00",
            }
        },
    )


class ListPointsSchema(Schema):
    points: List[PointSchemaIn]


class ListPointsSchemaOut(Schema):
    points: List[dict]
