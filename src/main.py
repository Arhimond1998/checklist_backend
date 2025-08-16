from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


from src.api import web_router, auth_router
from src.migration import init_migration

app = FastAPI(title="Check list", version="0.1.0", on_startup=[init_migration])

origins = [
    "http://localhost:3000",
    "http://localhost",
    "http://frontend",
    "http://127.0.0.1:3000",
    "http://127.0.0.1",
    "http://5.129.200.132",
    "http://5.129.200.132:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(web_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
