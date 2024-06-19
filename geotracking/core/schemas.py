from typing import List

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
    point_data: dict


class ListPointsSchema(Schema):
    points: List[PointSchemaIn]
