from fastapi import FastAPI
from uvicorn import run
from os import getenv
from firebase_admin import initialize_app
from firebase_admin.firestore import client
firebase = initialize_app()
db = client()
app = FastAPI()

@app.get("/group/{group_id}")
async def get_group(group_id: int):
    pass

if __name__ == '__main__':
    run(app, host='0.0.0.0', port=int(getenv('PORT', '8000')))