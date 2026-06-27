from bson import ObjectId

from database import tour_collection


async def create_tour(tour):
    result = await tour_collection.insert_one(tour)
    return str(result.inserted_id)


async def get_all_tours():
    tours = []

    async for tour in tour_collection.find():
        tour["_id"] = str(tour["_id"])
        tours.append(tour)

    return tours


async def get_tour(tour_id):
    tour = await tour_collection.find_one({"_id": ObjectId(tour_id)})

    if tour:
        tour["_id"] = str(tour["_id"])

    return tour


async def update_tour(tour_id, tour):
    result = await tour_collection.update_one(
        {"_id": ObjectId(tour_id)},
        {"$set": tour}
    )

    return result.modified_count


async def delete_tour(tour_id):
    result = await tour_collection.delete_one(
        {"_id": ObjectId(tour_id)}
    )

    return result.deleted_count