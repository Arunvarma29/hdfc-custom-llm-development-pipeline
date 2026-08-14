from fastapi import FastAPI

from services.run_orchestrator.app.routes.runs import (
    router,
)

app = FastAPI(
    title="HDFC LLM Run Orchestrator",
    version="1.0.0",
)

app.include_router(
    router,
    prefix="/api/v1",
)