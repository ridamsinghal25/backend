def individual_emotion(emotion):
    return {
        "id": str(emotion["_id"]),
        "emotion": emotion["emotion"],
        "confidence": emotion["confidence"],
        "analysis": emotion["analysis"],
        "created_at":emotion["created_at"],
    }
    
 
def all_emotions(emotions):
    return [individual_emotion(emotion) for emotion in emotions ]


def create_user(user):
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "clerk_id": user["clerk_id"],
        "name": user["name"],
    }