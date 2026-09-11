from fastapi import FastAPI

from .routers import players, fixtures, teams

app = FastAPI(title="FPL Scout API")


@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(teams.router)
app.include_router(players.router)
app.include_router(fixtures.router)