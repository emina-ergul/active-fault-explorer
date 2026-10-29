from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from backend.app.endpoints import earthquake_endpoints, fault_endpoints

app = FastAPI(title="Active Fault Explorer API")

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(earthquake_endpoints.router)
app.include_router(fault_endpoints.router)


@app.get("/")
def root():
    return RedirectResponse(url="/docs")
