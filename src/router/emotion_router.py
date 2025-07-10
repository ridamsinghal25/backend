from fastapi import APIRouter, Depends, HTTPException, Request
from src.models.emotion_model import Emotion, EmotionRequest
from src.database.schema import individual_emotion, all_emotions
from typing import List
from src.database.db import emotions_collection
from bson.objectid import ObjectId
from src.ai_generator import generate_emotion
from src.utils.clerk_authentication import authenticate_and_get_user_details

emotion_router = APIRouter()

async def get_emotions():
    print("get_emotions")
    return

@emotion_router.get("/get-emotions", summary="Get all the emotions of user")
async def get_all_emotions(request: Request):
    user = authenticate_and_get_user_details(request)

    emotions = emotions_collection.find({ "user_id": user["_id"]})

    return {"success": True, "data": all_emotions(emotions), "message": "Emotions fetched successfully"}


@emotion_router.post("/create-emotion", summary="Create a new emotion")
async def create_emotion(payload: EmotionRequest, request: Request):
    try:
        user = authenticate_and_get_user_details(request)

        user_emotion = payload.user_emotion

        new_emotion = generate_emotion(user_emotion)

        new_emotion["user_id"] = str(user["_id"])

        response = emotions_collection.insert_one(dict(new_emotion))

        emotion = emotions_collection.find_one({"_id": response.inserted_id})

        return {"success": True, "data": individual_emotion(emotion), "message": "Emotion created successfully"}

    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))


@emotion_router.delete("/delete/{emotion_id}", summary="Delete an emotion")
async def delete_emotion(emotion_id: str, request: Request):
    user = authenticate_and_get_user_details(request)

    emotion = emotions_collection.find_one({"_id": ObjectId(emotion_id)})

    if not emotion:
        raise HTTPException(status_code=404, detail="Emotion not found")
    
    delete =  emotions_collection.delete_one({"_id": ObjectId(emotion_id)})
    
    return {"success": True, "message": "Emotion deleted successfully"}