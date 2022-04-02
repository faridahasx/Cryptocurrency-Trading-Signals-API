from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import smtplib
import dns.resolver
from typing import List
from .. import models, schemas, utils, oauth2
from ..database import get_db
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

def validate_email(email):
    try:
        email_address = email
        splitAddress = email_address.split('@')
        domain = str(splitAddress[1])
        records = dns.resolver.resolve(domain, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
        server = smtplib.SMTP()
        server.set_debuglevel(0)
        server.connect(mxRecord)
        server.helo(server.local_hostname)
        server.mail(email_address)
        code, message = server.rcpt(str(email_address))
        server.quit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Please provide a valid email address: {e} ')
    else:
        if code != 250:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="The email account that you tried to reach does not exist")





@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Verify that the email is valid
    validate_email(user.email)
    user_email = db.query(models.User).filter(models.User.email == user.email).first()
    user_name = db.query(models.User).filter(models.User.username == user.username.lower()).first()

    if user_email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"This email address is already being used")
    elif user_name:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Username is already taken")

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    user.username = user.username.lower()
    user.email = user.email.lower()
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/', response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), ):
    users = db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user was found")

    return users


@router.get('/{username}', response_model=schemas.UserOut)
def get_users_by_name(username: str, db: Session = Depends(get_db), ):
    name = username.lower()
    user = db.query(models.User).filter(models.User.username == name).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No user was found")

    return user


@router.put("/", response_model=schemas.UserOut)
def update_user(update_user: schemas.UserCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    if current_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")

    validate_email(update_user.email)

    user_email = db.query(models.User).filter(models.User.email == update_user.email.lower()).first()
    user_name = db.query(models.User).filter(models.User.username == update_user.username.lower()).first()

    if user_email and user_email.email != current_user.email:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"{update_user.email} is already used by other user")

    if user_name and user_name.email != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Username is already taken")

    user = db.query(models.User).filter(models.User.email == current_user.email)
    hashed_password = utils.hash(update_user.password)
    update_user.password = hashed_password
    update_user.username = update_user.username.lower()
    update_user.email = update_user.email.lower()
    user.update(update_user.dict(), synchronize_session=False)
    db.commit()
    user_query = db.query(models.User).filter(models.User.email == update_user.email)

    return user_query.first()


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    if current_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")

    email = current_user.email
    user_query = db.query(models.User).filter(models.User.email == email)
    user = user_query.first()
    if user == None or current_user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User not found")

    user_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
