from fastapi import APIRouter, HTTPException

from models import Tour
from crud import (
    create_tour,
    get_all_tours,
    get_tour,
    update_tour,
    delete_tour
)

router = APIRouter()


@router.post("/tours")
async def add_tour(tour: Tour):
    tour_id = await create_tour(tour.model_dump())
    return {"id": tour_id}


@router.get("/tours")
async def read_tours():
    return await get_all_tours()


@router.get("/tours/{tour_id}")
async def read_tour(tour_id: str):
    tour = await get_tour(tour_id)

    if not tour:
        raise HTTPException(status_code=404, detail="Tour not found")

    return tour


@router.put("/tours/{tour_id}")
async def edit_tour(tour_id: str, tour: Tour):
    updated = await update_tour(tour_id, tour.model_dump())

    if updated == 0:
        raise HTTPException(status_code=404, detail="Tour not found")

    return {"message": "Tour updated"}


@router.delete("/tours/{tour_id}")
async def remove_tour(tour_id: str):
    deleted = await delete_tour(tour_id)

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Tour not found")

    return {"message": "Tour deleted"}