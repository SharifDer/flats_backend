# main.py

from fastapi import FastAPI, Depends, Form, File, UploadFile
from typing import Optional, List
from app.auth import JWTBearer
from services.apartment_services import *
from app.data_fetcher import create_firebase_user, login_user
from app_dtypes.request_dtypes import *
# from app_dtypes.request_dtypes import (
#                         ReqCreatUser, 
#                         Reqlogin,
#                         ReqcreateApartment, 
#                         ReqApartments, 
#                         Reqapartment_details)
from app_dtypes.response_dtypes import Resapartments, Resapartment_details
from services.user_services import create_user_record
from config import routes
from services.storage_cloudinary import upload_images


app = FastAPI()

@app.post(routes.create_user)
async def create_user(req: ReqCreatUser):
    user = await create_firebase_user(req=req)
    _ = await create_user_record(firebase_id=user['user_id'], user_type=req.user_type)
    return user

@app.post(routes.login)
async def login(req: Reqlogin):
    return await login_user(req)




@app.post(routes.post_apartment, dependencies=[Depends(JWTBearer())])
async def create_apartment(
    title: str = Form(...),
    type: str = Form(...),
    address: str = Form(...),
    price: float = Form(...),
    number_of_rooms: Optional[int] = Form(None),
    number_of_bathrooms: Optional[int] = Form(None),
    description: Optional[str] = Form(None),
    images: Optional[List[UploadFile]] = File(None),
    token_data=Depends(JWTBearer()),
):
    req = ReqcreateApartment(
        title=title,
        type=type,
        address=address,
        price=price,
        number_of_rooms=number_of_rooms,
        number_of_bathrooms=number_of_bathrooms,
        description=description,
        image=None
    )
    
    images_url = await upload_images(images)  # make sure this is async and returns URLs
    apartment_id = await create_apartment_record(req, token_data["uid"], images=images_url or [])

    return {"message": "Apartment created", "apartment_id": apartment_id}


@app.get(routes.Apartments , response_model=List[Resapartments])
async def get_apartments(req: ReqApartments = Depends()):
    data = await fetch_apartments_data(req)
    return data


@app.get(routes.apartment_details, response_model=Resapartment_details)
async def apartment_details(req : Reqapartment_details = Depends()) :
    return await fetch_apartment_details(req=req)


@app.patch(routes.update_apartment_status)
async def update_apartment_status(req : Requpdate_apartment_status , token_data=Depends(JWTBearer())):
    user_id = token_data['uid']
    await update_status(req , user_id)
    return {"message" : "status updated"}

