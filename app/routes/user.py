from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from app.schemas import user
from app.models.dao_users import UserDao
from app import utils

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post('/new_user')
def register_user(user: user.NewUser):

    is_user = UserDao.get_user_by_email(user.email)

    if is_user:

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={'msg': 'User already registered'}
        )
    

    success = UserDao.register_user(
        username=user.username,
        email=user.email,
        password_hash=utils.create_hash(user.password_user)
    )


    if success:

        return JSONResponse(
            content={'msg': 'registered user'},
            status_code=status.HTTP_200_OK
        ) 

    else:

        raise HTTPException(
            detail='db error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    

