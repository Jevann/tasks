import uvicorn
from fastapi import FastAPI, HTTPException, status
import requests

app = FastAPI()

BORED_API_URL = "https://www.boredapi.com/api/activity"


@app.get("/health", status_code=status.HTTP_200_OK)
async def service_alive():
    return {"message": "Service alive"}


@app.get("/activity")
async def get_activity():
    response = requests.get(BORED_API_URL)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching activity")
    return response.json()


@app.get("/activity_by_type/{activity_type}")
async def get_activity_by_type(activity_type: str):
    response = requests.get(f"{BORED_API_URL}?type={activity_type}")
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching activity")
    return response.json()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
