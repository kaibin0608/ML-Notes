from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# "Pydantic" models allow us to structure your data
class Item(BaseModel):
    text: str =None 
    is_done: bool = False

items = []

# this is an app decorator and it defineds a path for the HTTP GET method
@app.get("/") # this is how you define a route
def root():
    return {"message": "Hello, World!"}

# new endpoint to get all items
# user can access to this endpoint by sending a HTTP POST request to /items
@app.post("/items", response_model=list[Item]) # response_model is used to specify the type of data that should be returned by the endpoint
def create_item(item:Item): # need to receive an item as input
    items.append(item)
    return items

@app.get("/items")
def list_items(limit: int=10):
    return items[0:limit]


# to view a specific item in the list
@app.get("/items/{item_id}", response_model=Item) # response_model is used to specify the type of data that should be returned by the endpoint
def get_item(item_id: int) -> Item: # return an Item instead str
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")




# in FastAPI, routes are used to define the different urls(endpoints) that your app should respond to
# you can define routes to handle different interactions(HTTP methods like GET, POST, PUT, DELETE, etc.)
# directory/docs#