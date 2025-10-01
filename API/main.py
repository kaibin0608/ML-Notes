from fastapi import FastAPI

app = FastAPI()

# this is an app decorator and it defineds a path for the HTTP GET method
@app.get("/") # this is how you define a route
def root():
    return {"message": "Hello, World!"}

