from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from bson import ObjectId
import gridfs

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Connect to Mongo Atlas
CONNECTION_STRING = os.getenv('CONNECTION_STRING')

client = AsyncIOMotorClient(CONNECTION_STRING)
db = client.DB_PlayerData  
#fs = gridfs.GridFSBucket(db)  # Create GridFS instance for this database

class PlayerScore(BaseModel):
    player_name: str
    score: int

    


@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):

 # In a real application, the file should be saved to a storage service 
 content = await file.read()
 sprite_doc = {"filename": file.filename, "content": content}
 result = await db.sprites.insert_one(sprite_doc)
 return {"message": "Sprite uploaded", "id": str(result.inserted_id)}


#Get Audio
@app.get("/sprite/{sprite_id}")
async def get_sprite(_id: str):
    result = await db.sprites.find_one({"_id": ObjectId(_id)})

    if result:
        result["_id"] = str(result["_id"]) #Convert ObjectId to string
        return result 
    else:
        raise HTTPException(status_code=404, detail="Sprite not found")
    

#Get All Sprites
@app.get("/all_sprites")
async def get_all_sprites():
    savedSprites = await db.sprites.find().to_list(length=100)
    allSprites = []

    for sprite in savedSprites:
        sprite["_id"] = str(sprite["_id"]) #Convert ObjectId to string
        allSprites.append(audio)

    return {"all_audio": allSprites}


#TODO: THIS
@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    content = await file.read()
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

#Get Audio
@app.get("/audio/{audio_id}")
async def get_audio(_id: str):
    result = await db.audio.find_one({"_id": ObjectId(_id)})

    if result:
        result["_id"] = str(result["_id"]) #Convert ObjectId to string
        return result 
    else:
        raise HTTPException(status_code=404, detail="Audio not found")
    

#Get All Audio
@app.get("/all_audio")
async def get_all_audio():
    savedAudio = await db.audio.find().to_list(length=100)
    allAudio = []

    for audio in savedAudio:
        audio["_id"] = str(audio["_id"]) #Convert ObjectId to string
        allAudio.append(audio)

    return {"all_audio": allAudio}


#Add Player Score
@app.post("/player_score")
async def add_score(score: PlayerScore):
    score_doc = score.dict()

    try:
        result = await db.scores.insert_one(score_doc)
        return{
            "message": "Player Score Uploaded",
            "id":str(result.inserted_id)
        }

    except Exception:
        raise HTTPException(status_code=500, detail="Unable to add player score")
  
#Get Player Score
@app.get("/player_score/{player_name}")
async def get_score(player_name: str):
    result = await db.scores.find_one({"player_name": player_name})

    if result:
        result["_id"] = str(result["_id"]) #Convert ObjectId to string
        return result 
    else:
        raise HTTPException(status_code=404, detail="Player not found")
    

@app.get("/all_scores")
async def get_all_scores():
    savedScores = await db.scores.find().to_list(length=100)
    allScores = []

    for score in savedScores:
        score["_id"] = str(score["_id"]) #Convert ObjectId to string
        allScores.append(score)

    return {"all_scores": allScores}