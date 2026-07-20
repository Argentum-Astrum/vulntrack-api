from fastapi import FastAPI

app = FastAPI(
    title="VulnTrack API",
    version="0.1.0",
)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    """Return the application health status."""
    return {"status": "ok"}
