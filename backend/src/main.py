from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.domains import router as domains_router
from api.v1.scenarios import router as scenarios_router
from api.v1.admin import router as admin_router

app = FastAPI(title="Cyber Risk & Awareness Hub")

# ✅ Allow the Vite frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://dvteiiw99nz3y2svrguosici.178.104.40.223.sslip.io",
        "https://cyber.licursi.dev"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(domains_router)
app.include_router(scenarios_router)
app.include_router(admin_router)

@app.get("/")
def root():
    return {"status": "ok", "message": "Cyber Risk & Awareness Hub API running"}
