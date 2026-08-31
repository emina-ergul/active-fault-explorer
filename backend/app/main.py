from fastapi import FastAPI
from backend.app.endpoints import earthquake_endpoints, fault_endpoints

app = FastAPI()

app.include_router(earthquake_endpoints.router)
app.include_router(fault_endpoints.router)


@app.get("/")
def root():
    return {"running fault explorer"}
