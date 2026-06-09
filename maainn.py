from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from bson.objectid import ObjectId

app = FastAPI()
templates = Jinja2Templates(directory="templates")

cluster_link = "ТВІЙ_РЯДОК_ПІДКЛЮЧЕННЯ_З_MONGODB_ATLAS"
client = MongoClient(cluster_link)
db = client["travel_agency_db"]
tours_collection = db["tours"]



@app.get("/")
def index_page(request: Request, search: str = None):
    if search:
        query = {
            "$or": [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}}
            ]
        }
        tours = list(tours_collection.find(query).limit(20))
    else:
        tours = list(tours_collection.find().limit(20))

    return templates.TemplateResponse("index.html", {"request": request, "tours": tours, "search": search})


@app.get("/web/tour/{tour_id}")
def tour_detail_page(request: Request, tour_id: str):
    tour = tours_collection.find_one({"_id": ObjectId(tour_id)})
    return templates.TemplateResponse("tour_detail.html", {"request": request, "tour": tour})



@app.post("/web/tour/add")
def web_add_tour(title: str = Form(...), description: str = Form(...), price: int = Form(...)):
    new_tour = {"title": title, "description": description, "price": price}
    tours_collection.insert_one(new_tour)
    return RedirectResponse(url="/", status_code=303)



@app.get("/web/tour/delete/{tour_id}")
def web_delete_tour(tour_id: str):
    tours_collection.delete_one({"_id": ObjectId(tour_id)})
    return RedirectResponse(url="/", status_code=303)



@app.get("/api/tours")
def get_all_tours():
    tours = []
    for t in tours_collection.find():
        t["_id"] = str(t["_id"])
        tours.append(t)
    return tours


@app.post("/api/tours")
def create_tour(title: str, description: str, price: int):
    tour = {"title": title, "description": description, "price": price}
    result = tours_collection.insert_one(tour)
    return {"status": "Тур створено", "id": str(result.inserted_id)}


@app.get("/api/tours/{tour_id}")
def get_tour(tour_id: str):
    tour = tours_collection.find_one({"_id": ObjectId(tour_id)})
    if tour:
        tour["_id"] = str(tour["_id"])
        return tour
    return {"error": "Тур не знайдено"}


@app.put("/api/tours/{tour_id}")
def update_tour(tour_id: str, title: str, description: str, price: int):
    updated = {"title": title, "description": description, "price": price}
    tours_collection.update_one({"_id": ObjectId(tour_id)}, {"$set": updated})
    return {"status": "Тур оновлено"}


@app.delete("/api/tours/{tour_id}")
def delete_tour(tour_id: str):
    tours_collection.delete_one({"_id": ObjectId(tour_id)})
    return {"status": "Тур видалено"}