from pydantic import BaseModel, Field


class Tour(BaseModel):
    title: str = Field(...)
    country: str = Field(...)
    city: str = Field(...)
    description: str = Field(...)
    price: int = Field(...)
    days: int = Field(...)
    start_date: str = Field(...)
    available_places: int = Field(...)