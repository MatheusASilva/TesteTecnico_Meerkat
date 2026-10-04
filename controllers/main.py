from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from controllers import pecas_controller, vendas_controller, dashboard


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "null",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Accept", "Content-Type"],
)

app.include_router(pecas_controller.router)
app.include_router(vendas_controller.router)
app.include_router(dashboard.router)

VIEW_DIR = Path(__file__).resolve().parent.parent / "view"
app.mount("/", StaticFiles(directory=VIEW_DIR, html=True), name="view")