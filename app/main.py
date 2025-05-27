from fastapi import FastAPI
from .models import ClientInfo
from .risk_logic import score_client

app = FastAPI()

@app.post("/check_risk")
def check_risk(client: ClientInfo):
    return score_client(client)