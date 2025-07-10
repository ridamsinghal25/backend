from pydantic import Field, BaseModel
from datetime import datetime

class Emotion(BaseModel):
    user_id: str
    emotion: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    analysis: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EmotionRequest(BaseModel):
    user_emotion: str
