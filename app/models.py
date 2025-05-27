from pydantic import BaseModel

class ClientInfo(BaseModel):
    name: str
    industry: str
    description: str