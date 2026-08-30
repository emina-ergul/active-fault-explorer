from fastapi import FastAPI

from backend.app.services.earthquake_service import get_all_earthquakes

app = FastAPI()


@app.get("/")
def root():
    return {"running fault explorer"}


@app.get("/all-earthquakes")
def all_earthquakes():
    try:
        earthquakes = get_all_earthquakes()
        return {"earthquakes": earthquakes}
    except ValueError as e:
        return {"error": str(e)}
