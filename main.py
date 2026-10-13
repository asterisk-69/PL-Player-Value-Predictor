from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from typing import List
app=FastAPI()

class Player(BaseModel):
    id:int
    name:str
    position: str
    club: str
    age: int

class PlayerUpdate(BaseModel):
    name: str | None=None
    position: str | None=None
    club: str | None=None
    age: int | None=None

@app.get("/health_check")
async def ping():
    return ("result: healthy")
players = [
    {
        "id": 1,
        "name": "Bukayo Saka",
        "position": "RW",
        "club": "Arsenal",
        "age": 24
    },
    {
        "id": 2,
        "name": "Erling Haaland",
        "position": "ST",
        "club": "Manchester City",
        "age": 26
    },
    {
        "id": 3,
        "name": "Cole Palmer",
        "position": "AM",
        "club": "Chelsea",
        "age": 24
    }
]
@app.get("/players")
def return_players() -> List[Player]:
    return players
@app.post("/players")
def add_players(player:Player):
    for i in players:
        if i["id"] == player.id:
            raise HTTPException(status_code=409,detail="Already exists")
    players.append(player.model_dump())
    return player

@app.get("/players/{player_id}")
def get_player(player_id: int)-> Player:
    for i in players:
        if player_id==i["id"]:
            return i
    raise HTTPException(status_code=404,detail="Not Found") 
@app.patch("/players/{player_id}")
def update_player(player_id:int,player:PlayerUpdate) -> Player:
    for i in players:
        if i["id"] == player_id:

            updates = player.model_dump(exclude_unset=True)

            for field, value in updates.items():
                i[field] = value

            return i

    raise HTTPException(status_code=404, detail="Player not found")
            