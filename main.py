from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
import os
from dotenv import load_dotenv
from bson import ObjectId
import gridfs
import re

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

#SQL Injection Prevention
def checkWhitelist(input_str: str): #White Listing REF: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html#primary-defenses
    forbiddenCharacters = ['$', '{', '}', ';', '<', '>', '!', '`', "'", '"']
    #Loop through forbidden characters and search for them
    for char in forbiddenCharacters: 
        if char in input_str:
            return False
    return True #Return true if nothing found

def escapeInput(input_str: str): #This is an Option, but it is Discouraged to use so it not being used
    pattern = r"([\"'`;$.\\{}\[\]\(\)])"
    return re.sub(pattern, r"\\\1", input_str)


#This endpoint is here to test vercel's connection
@app.get("/")
def read_root():
    return {"message": "Vercel Online"}    

#This deletes a sprite
@app.delete("/delete_sprite/{sprite_id}")
async def delete_sprite(sprite_id: str):
    """
    Deletes a sprite from the database by its ID.
    """
    if not checkWhitelist(sprite_id):
        raise HTTPException(status_code=400, detail="Invalid character in input")

    db = getDB()
    fsSprites = getSpriteBucket(db)

    try:
        fileID = ObjectId(sprite_id)  #Convert the sprite_id to ObjectId
        fileData = await db.sprites.files.find_one({"_id": fileID})  #Verify it exists in files
        if not fileData:
            raise HTTPException(status_code=404, detail="Sprite file not found")

        # Delete the file from the GridFS bucket
        await fsSprites.delete(fileID)
        return {"message": f"Sprite with ID {sprite_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting sprite: {str(e)}")


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
        if file.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(status_code=400, detail="Only .png and .jpeg are supported")

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
    if not checkWhitelist(_id):
        raise HTTPException(status_code=400, detail="Invalid character in input")   

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
    if not checkWhitelist(_id):
        raise HTTPException(status_code=400, detail="Invalid character in input")  

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

#Delete Audio
@app.delete("/delete_audio/{audio_id}")
async def delete_audio(audio_id: str):
    """
    Deletes an audio file from the database by its ID.
    """
    if not checkWhitelist(audio_id):
        raise HTTPException(status_code=400, detail="Invalid character in input")

    db = getDB()
    fsAudio = getAudioBucket(db)

    try:
        fileID = ObjectId(audio_id)  #Convert the audio_id to ObjectId
        fileData = await db.audio.files.find_one({"_id": fileID})  #Verify it exists in files
        if not fileData:
            raise HTTPException(status_code=404, detail="Audio file not found")

        # Delete the file from the GridFS bucket
        await fsAudio.delete(fileID)
        return {"message": f"Audio with ID {audio_id} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting audio: {str(e)}")


#Upload audio
@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Retrieves DB and Bucket from MongoDB
    Verifies file type is audio
    Reads file content and uploads it to GridFS bucket
    IF successful returns the uploaded item ID, else an HTTP Exception 500 
    """
    if not checkWhitelist(file.filename):
        raise HTTPException(status_code=400, detail="Invalid character in input")  

    db = getDB()
    fsAudio = getAudioBucket(db)  

    try:
        if file.content_type not in ["audio/mpeg", "audio/wav"]:
            raise HTTPException(status_code=400, detail="Only mp3 and wav are supported")

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
    if not checkWhitelist(_id):
        raise HTTPException(status_code=400, detail="Invalid character in input")  

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
    if not checkWhitelist(_id):
        raise HTTPException(status_code=400, detail="Invalid character in input")  

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

#Delete Player Score
@app.delete("/delete_player_score/{player_name}")
async def delete_player_score(player_name: str):
    """
    Deletes a player score from the database by player name.
    """
    if not checkWhitelist(player_name):
        raise HTTPException(status_code=400, detail="Invalid character in input")

    db = getDB()

    try:
        result = await db.scores.delete_one({"player_name": player_name})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Player score not found")
        return {"message": f"Player score for {player_name} deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting player score: {str(e)}")


#Add Player Score
@app.post("/player_score")
async def add_score(score: PlayerScore):
    """
    Retrieves DB from MongoDB
    Creates a score dictionary 
    Adds the score to the score DB (player_name: str,score: int)
    """
    if not checkWhitelist(score.player_name):
        raise HTTPException(status_code=400, detail="Invalid character in input")  


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
    if not checkWhitelist(player_name):
        raise HTTPException(status_code=400, detail="Invalid character in input")  

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

#Update player score
@app.put("/update_player_score/{player_name}")
async def update_player_score(player_name: str, new_score: int):
    """
    Updates the score of a player by their name.
    """
    if not checkWhitelist(player_name):
        raise HTTPException(status_code=400, detail="Invalid character in input")

    db = getDB()

    try:
        result = await db.scores.update_one(
            {"player_name": player_name},  # Find the player by name
            {"$set": {"score": new_score}}  # Update the score
        )

        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Player not found")
        
        return {"message": f"Score for {player_name} updated successfully", "new_score": new_score}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating player score: {str(e)}")
