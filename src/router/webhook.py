from fastapi import APIRouter, Request, HTTPException, Response, status
from svix.webhooks import Webhook
import os
import json
from src.database.db import users_collection

router = APIRouter()


@router.post("/clerk")
async def handle_user_created(request: Request, response: Response):
    webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")

    if not webhook_secret:
        raise HTTPException(status_code=500, detail="CLERK_WEBHOOK_SECRET not set")

    body = await request.body()
    headers = dict(request.headers)

    payload = body.decode("utf-8")

    try:
        wh = Webhook(webhook_secret)
        event = wh.verify(payload, headers)

    except WebhookVerificationError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return


    eventType = event["type"]

    if (eventType == "user.created"):
        try:

            email_addresses = event["data"]["email_addresses"]
            primary_email_address_id = event["data"]["primary_email_address_id"]
            primary_email = next(
                (email for email in email_addresses if email["id"] == primary_email_address_id),
                None
            )

            if not primary_email:
                raise HTTPException(status_code=400, detail="Error occurred - No primary email")

            new_user = users_collection.insert_one({
                "email": primary_email["email_address"],
                "clerk_id": event["data"]["id"],
                "name": event["data"]["first_name"],
            })                

            if (not str(new_user.inserted_id)):
                raise HTTPException(status_code=400, detail="Error occurred - User not created")

        except Exception as e:
            print("Webhook error:", e)
            raise HTTPException(status_code=401, detail=str(e))

    
    return {"status": 200, "message": "success"}