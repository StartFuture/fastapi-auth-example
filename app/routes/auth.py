from datetime import datetime, timedelta
import logging

from fastapi import APIRouter, Depends, HTTPException, status, Path
from pydantic import EmailStr
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app import parameters, emails, utils
from app.models.dao_users import UserDao
from app.schemas import auth

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

oauth = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_token(token: str = Depends(oauth)):
    
    try:

        payload = jwt.decode(token, parameters.SECRET_KEY, algorithms=parameters.ALGORITHM)
        user_id = payload['sub']
        is_user_valid = UserDao.get_user_by_id(user_id)

        if not is_user_valid:

            raise HTTPException(
                detail={'msg': 'invalid token'}, 
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        
        if payload['type'] == 'reset_password':

            raise HTTPException(
                detail={'msg': 'invalid token'}, 
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        return {**payload, 'token': token}

    except JWTError as error:

        logging.error(f'Jwt error: {error}')

        raise HTTPException(
            detail={'msg': 'missing token'}, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    

def verify_token_recovery(token: str): # transformar em decorator

    print(token)

    # try:

    payload = jwt.decode(token, parameters.SECRET_KEY, algorithms=parameters.ALGORITHM)
    print(payload)
    user_id = payload['sub']
    is_user_valid = UserDao.get_user_by_id(user_id)

    if not is_user_valid:

        raise HTTPException(
            detail={'msg': 'invalid token'}, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    if payload['type'] == 'login':

        raise HTTPException(
            detail={'msg': 'invalid token'}, 
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    return {**payload, 'token': token}

    # except JWTError:

    #     raise HTTPException(
    #         detail={'msg': 'missing token'}, 
    #         status_code=status.HTTP_401_UNAUTHORIZED
    #     )


@router.post('/login')
def login(request_form: OAuth2PasswordRequestForm = Depends()):

    email = request_form.username

    user = UserDao.get_user_by_email(email)

    if user:

        if utils.check_pwd_hash(password_hash=user['password_user'], password=request_form.password):

            expire = datetime.utcnow() + timedelta(days=int(parameters.ACCESS_TOKEN_EXPIRE))

            payload = {
                'sub': str(user['id_user']),
                'exp': expire,
                'type': 'login'
            }

            token = jwt.encode(payload, parameters.SECRET_KEY, algorithm=parameters.ALGORITHM)

            return JSONResponse(
                    content={'access_token': token, "type": 'login'},
                    status_code=status.HTTP_200_OK
            )

        else:

            raise HTTPException(
                detail={'msg': 'invalid data'},
                status_code=status.HTTP_401_UNAUTHORIZED
                )

    else:

        raise HTTPException(
            detail={'msg': 'invalid data'},
            status_code=status.HTTP_401_UNAUTHORIZED
            )
    

@router.post('/')
def token_health_check(token: str = Depends(verify_token)):

    if token['type'] == 'login':

        return JSONResponse(
            content={'msg': 'token is valid', "type": 'login'},
            status_code=status.HTTP_200_OK
        )

    if token['type'] == 'reset_password':

        raise HTTPException(
            detail={'msg': 'this token is unique to recover password'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    

@router.post('/send_email_recovery')
def send_email_recovery(reset_password: auth.ResetPassword):

    user = UserDao.get_user_recover(reset_password.email)

    if user:
        expire = datetime.utcnow() + timedelta(minutes=30)

        payload = {
            'sub': str(user['id_user']),
            'exp': expire,
            'type': 'reset_password'
        }
        
        token = jwt.encode(payload, parameters.SECRET_KEY, algorithm=parameters.ALGORITHM)
        
        url_reset_password = f'{parameters.HOST_FRONT}/auth/recovery_password/{token}'

        success = utils.send_email(
            client_email=user['email'],
            layout_email=emails.CONTENT_EMAIL_RECOVER_PASSWORD.format(
                name=user['username'],
                action_url=url_reset_password,
                operating_system='Windows',
                browser_name='Chrome',
                support_url=parameters.SUPPORT_URL
            ),
            context='Recuperação de senha'
        )

        if success:

            return JSONResponse(
                    content={'msg': 'email send'},
                    status_code=status.HTTP_200_OK
            )
        
        raise HTTPException(
            detail={'msg': 'email error'},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    else:

        raise HTTPException(
            detail={'msg': 'invalid data'},
            status_code=status.HTTP_401_UNAUTHORIZED
            )


@router.post('/recovery_password/{token}')
def recovery_password(new_password: str, token: str = Depends(verify_token_recovery)):

    success = UserDao.update_password(id_user=token['sub'], new_password=utils.create_hash(new_password))

    if success:

        return JSONResponse(
            content={'msg': 'success'},
            status_code=status.HTTP_200_OK
        )
    
    else:

        raise HTTPException(
            detail='db error',
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
