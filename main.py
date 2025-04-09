from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
import os
from dotenv import load_dotenv
from bson import ObjectId
import gridfs

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

class PlayerScore(BaseModel):
    player_name: str
    score: int

def getDB():
    # Connect to Mongo Atlas
    CONNECTION_STRING = os.getenv('CONNECTION_STRING')
    client = AsyncIOMotorClient(CONNECTION_STRING)
    return client.DB_PlayerData  

#Create gridfs buckets REF: https://motor.readthedocs.io/en/stable/api-asyncio/asyncio_gridfs.html
def getSpriteBucket(db):
    return AsyncIOMotorGridFSBucket(db,bucket_name="sprites")

def getAudioBucket(db):
    return AsyncIOMotorGridFSBucket(db,bucket_name="audio")


#This endpoint is here to test vercel's connection
@app.get("/")
def read_root():
    return {"message": "Vercel Online"}    

#This uploads a sprite to the mongo dB it only allows sprites of type PNG 
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    """
    Retrieves DB and Bucket from MongoDB
    Verifies file type is PNG
    Reads file content and uploads it to GridFS bucket
    IF successful returns the uploaded item ID, else an HTTP Exception 500 
    """

    db = getDB()
    fsSprites = getSpriteBucket(db) 

    try:
        if file.content_type != "image/png":
            raise HTTPException(status_code=400, detail="Uploaded file is not an image")

        contents = await file.read()
        #Upload to GridFS
        fileID = await fsSprites.upload_from_stream(
            filename=file.filename,
            source=contents
        )

        if(not fileID):
            raise HTTPException(status_code=500, detail=str("Unable to Upload File"))
           
        return {
            "message": "Sprite uploaded",
            "audio_id": str(fileID)
        }
    except HTTPException as httpE: #if an http exception is caught outpout it
        raise httpE

    except Exception as e:
        raise HTTPException(status_code=500, detail=str("Unable to Upload File"))


#Get Sprite
@app.get("/spritefile/{sprite_id}")
async def get_sprite_file(_id: str):
    """
    Retrieves DB and Bucket from MongoDB
    Converts _id paramater to ObjectId 
    Searches through files DB to find a file with the matching ID
    If the file exists it gets it from the GridFS bucket 
    A StreamingResponse is returned containing the file
    """

    db = getDB()
    fsSprites = getSpriteBucket(db) 

    try:
        fileID = ObjectId(_id) #Convert the audio_id to ObjectId
        fileData = await db.sprites.files.find_one({"_id": fileID}) #Verify it exists in files
        if not fileData:
            raise HTTPException(status_code=404, detail="Sprite file not found")
        gridfsResult = await fsSprites.open_download_stream(fileID) #Ref: https://www.mongodb.com/docs/drivers/node/v3.6/fundamentals/gridfs/
        if not gridfsResult:
            raise HTTPException(status_code=404, detail="Unable to open Sprite file")  
        return StreamingResponse(gridfsResult, media_type="image/png") #Ref: https://fastapi.tiangolo.com/advanced/custom-response/#additional-documentation
    
    except HTTPException as httpE: #if an http exception is caught outpout it
        raise httpE
    except Exception:
        raise HTTPException(status_code=404, detail="Sprite file not found")

@app.get("/spritedata/{sprite_id}")
async def get_sprite_data(_id: str):   
    """
    Retrieves DB from MongoDB
    Converts _id paramater to ObjectId 
    Searches through files DB to find a file with the matching ID
    If the file exists it returns the file data
    """
    db = getDB()

    fileID = ObjectId(_id) #Convert the sprite_id to ObjectId
    fileData = await db.sprites.files.find_one({"_id": fileID})
    if not fileData:
        raise HTTPException(status_code=404, detail="Sprite file not found")

    return {
        "_id": str(fileData["_id"]), 
        "filename": fileData["filename"],
        "chunkSize": fileData["chunkSize"],
        "length": fileData["length"],
        "uploadDate": fileData["uploadDate"]
    }   
    

#Get All Sprites
@app.get("/all_sprites")
async def get_all_sprites():
    """
    Retrieves DB and Bucket from MongoDB
    Searches the bucket and returns first 100 records found
    """

    db = getDB()
    fsSprites = getSpriteBucket(db) 

    savedSprites = await fsSprites.find().to_list(length=100) #Get first 100 records
    allSprites = []

    for sprite in savedSprites: #For each record add the following data
        allSprites.append({
            "_id": str(sprite["_id"]),  #Convert ObjectId to string
            "filename": sprite["filename"],
            "length": sprite["length"],
            "uploadDate": sprite["uploadDate"]
        })

    return {"all_sprites": allSprites}

#Upload audio
@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Retrieves DB and Bucket from MongoDB
    Verifies file type is audio
    Reads file content and uploads it to GridFS bucket
    IF successful returns the uploaded item ID, else an HTTP Exception 500 
    """
    db = getDB()
    fsAudio = getAudioBucket(db)  

    try:
        if file.content_type != "audio/mpeg":
            raise HTTPException(status_code=400, detail="Uploaded file is not an audio file")

        contents = await file.read() #Read File Contents
        #Upload to GridFS
        fileID = await fsAudio.upload_from_stream(
            filename=file.filename,
            source=contents
        )

        if(not fileID): #If upload failed return error message
            raise HTTPException(status_code=500, detail=str("Unable to Upload File"))
        
        return {
            "message": "Audio uploaded",
            "audio_id": str(fileID)
        }

    except HTTPException as httpE: #if an http exception is caught outpout it
        raise httpE
    except Exception as e:
        raise HTTPException(status_code=500, detail=str("Unable to Upload File"))


#Get Audio
@app.get("/audiofile/{audio_id}")
async def get_audio_file(_id: str): 
    """
    Retrieves DB and Bucket from MongoDB
    Converts _id paramater to ObjectId 
    Searches through files DB to find a file with the matching ID
    If the file exists it gets it from the GridFS bucket 
    A StreamingResponse is returned containing the file
    """

    db = getDB()
    fsAudio = getAudioBucket(db)     
    try:
        fileID = ObjectId(_id) #Convert the audio_id to ObjectId
        fileData = await db.audio.files.find_one({"_id": fileID}) #Verify it exists in files
        if not fileData:
            raise HTTPException(status_code=404, detail="Audio file not found")
        gridfsResult = await fsAudio.open_download_stream(fileID) #Ref: https://www.mongodb.com/docs/drivers/node/v3.6/fundamentals/gridfs/
        if not gridfsResult:
            raise HTTPException(status_code=404, detail="Unable to open Audio file")  
        return StreamingResponse(gridfsResult, media_type="audio/mpeg") #Ref: https://fastapi.tiangolo.com/advanced/custom-response/#additional-documentation

    except HTTPException as httpE: #if an http exception is caught output it
        raise httpE
    except Exception:
        raise HTTPException(status_code=404, detail="Audio file not found")

@app.get("/audiodata/{audio_id}")
async def get_audio_data(_id: str): 
    """
    Retrieves DB from MongoDB
    Converts _id paramater to ObjectId 
    Searches through files DB to find a file with the matching ID
    If the file exists it returns the file data
    """
    db = getDB()     
    fileID = ObjectId(_id) #Convert the audio_id to ObjectId
    fileData = await db.audio.files.find_one({"_id": fileID})
    if not fileData:
        raise HTTPException(status_code=404, detail="Audio file not found")

    return {
        "_id": str(fileData["_id"]), 
        "filename": fileData["filename"],
        "chunkSize": fileData["chunkSize"],
        "length": fileData["length"],
        "uploadDate": fileData["uploadDate"]
    }   
    

#Get All Audio
@app.get("/all_audio")
async def get_all_audio():
    """
    Retrieves DB and Bucket from MongoDB
    Searches the bucket and returns first 100 records found
    """

    db = getDB()
    fsAudio = getAudioBucket(db)

    savedAudio = await fsAudio.find().to_list(length=100)
    allAudio = []

    for audio in savedAudio:
        allAudio.append({
            "_id": str(audio["_id"]),  #Convert ObjectId to string
            "filename": audio["filename"],
            "length": audio["length"],
            "uploadDate": audio["uploadDate"]
        })

    return {"all_audio": allAudio}


#Add Player Score
@app.post("/player_score")
async def add_score(score: PlayerScore):
    """
    Retrieves DB from MongoDB
    Creates a score dictionary 
    Adds the score to the score DB (player_name: str,score: int)
    """

    db = getDB()
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
    """
    Retrieves DB from MongoDB
    Searches the DB for a matching player_name and returns it
    """

    db = getDB()
    result = await db.scores.find_one({"player_name": player_name})

    if result:
        result["_id"] = str(result["_id"]) #Convert ObjectId to string
        return result 
    else:
        raise HTTPException(status_code=404, detail="Player not found")
    

@app.get("/all_scores")
async def get_all_scores():
    """
    Retrieves DB from MongoDB
    Searches the DB and returns the first 100 records
    """

    db = getDB()
    savedScores = await db.scores.find().to_list(length=100)
    allScores = []

    for score in savedScores:
        score["_id"] = str(score["_id"]) #Convert ObjectId to string
        allScores.append(score)

    return {"all_scores": allScores}