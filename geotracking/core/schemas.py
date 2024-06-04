from typing import List

from ninja import Schema, ModelSchema
from pydantic import ConfigDict, field_validator
from .models import Track


class TrackSchemaIn(Schema):
    description: str

    @field_validator("description")
    def valid_description(cls, description: str) -> str:
        if description and len(description) <= 2:
            raise ValueError("It must be at least 3 characteres long.")
        return description


class TrackSchema(ModelSchema):
    class Meta:
        model = Track
        fields = ["id", "description", "done"]

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 42,
                "description": "Track One",
                "done": True,
            }
        },
    )


class ListTracksSchema(Schema):
    tracks: List[TrackSchema]
