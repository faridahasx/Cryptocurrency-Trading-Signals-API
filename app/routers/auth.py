import os

from fastapi import APIRouter, Depends, status, HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Email")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Wrong Password")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout_and_expire_cookie(response: Response, current_user: int = Depends(oauth2.get_current_user)):
                                                        #current_user: schemas.User = Depends(oauth2.get_current_user)):
    # response.delete_cookie("Authorization")
    response.set_cookie(
        key="Authorization",
        value=f'',
        samesite="Lax" if "dev" in os.environ.get("ENV") else "None",
        domain="localhost"
        if "dev" in os.environ.get("ENV")
        else "dericfagnan.com",
        secure="dev" not in os.environ.get("ENV"),
        httponly=True,
        max_age=1,
        expires=1,
    )

    return {}