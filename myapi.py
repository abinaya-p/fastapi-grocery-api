from fastapi import FastAPI, Path, Query
from pydantic import BaseModel

app = FastAPI()

grocery = {
    1: {"item": "milk",
         "rate": 30, 
         "brand": "kavin"
         },
    2: {"item": "cake",
         "rate": 50, 
         "brand": "wonderla"
         },
    3: {"item": "bread",
         "rate": 40, 
         "brand": "britannia"
         },
}

class GroceryItem(BaseModel):
    item: str
    rate: int
    brand: str

#get method--path and query parameters

@app.get("/get-grocery/{grocery_id}")
def get_grocery(
    grocery_id: int = Path(..., description="ID of the grocery item", gt=0),
    brand: str = Query(None, description="Filter by brand (optional)"),
):
    if grocery_id not in grocery:
        return {"error": "Item not found"}

    item = grocery[grocery_id]
    if brand and item["brand"].lower() != brand.lower():
        return {"error": "Item found, but brand does not match"}

    return {grocery_id: item}

#post method

@app.post("/add-grocery/{grocery_id}")
def add_grocery(
    grocery_id: int = Path(..., description="ID for the new grocery item", gt=0),
    item: GroceryItem = None
):
    if grocery_id in grocery:
        return {"error": "Item with this ID already exists"}

    grocery[grocery_id] = item.dict()
    return {"message": "Grocery item added successfully", grocery_id: item.dict()}

#put method

@app.put("/update-grocery/{grocery_id}")
def update_grocery(
    grocery_id: int = Path(..., description="ID of the grocery item to update", gt=0),
    item: GroceryItem = None
):
    if grocery_id not in grocery:
        return {"error": "Item not found"}

    grocery[grocery_id] = item.dict()
    return {"message": "Grocery item updated successfully", grocery_id: item.dict()}

#delete method

@app.delete("/delete-grocery/{grocery_id}")
def delete_grocery(
    grocery_id: int = Path(..., description="ID of the grocery item to delete", gt=0)
):
    if grocery_id not in grocery:
        return {"error": "Item not found"}

    del grocery[grocery_id]
    return {"message": "Grocery item deleted successfully"}
