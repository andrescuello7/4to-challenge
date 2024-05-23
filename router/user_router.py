from fastapi import APIRouter, HTTPException, Header, status
from fastapi.params import Depends
from starlette.responses import RedirectResponse
from enums.user_enum import user_role
from schemas.user_schema import user_schema
from db_config import session, get_db
from utils.auth import auth_token
from services import user_service as controller

router = APIRouter()

@router.get("/")
def main():
    return RedirectResponse(url="/docs/")

@router.get('/api/users/getAll')
def get_users(db: session = Depends(get_db)):
    '''
    Get all Users
    '''
    try:
        response = controller.get_all(db)
        return response
    except Exception as e:
        return {'error': f"get all users, detail: {e}"}

@router.post('/api/create/user')
def create_user(
    req: user_schema,
    authorization: str = Header(...),
    db: session = Depends(get_db)):
    '''
    Create new User
    '''
    try:
        if auth_token(authorization)['role'] != user_role().ADMIN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not authorized'
            )

        response = controller.create_new_user(db, req)
        return response
    except Exception as e:
        return {'error': f"create user, detail: {e}"}

@router.put('/api/update/user/{user_id}')
def update_task(
    req: user_schema,
    user_id: int,
    authorization: str = Header(...),
    db: session = Depends(get_db)):
    '''
    Update a task of admin
    '''
    try:
        if auth_token(authorization)['role'] != user_role().ADMIN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not authorized'
            )

        response = controller.update_user(db, user_id, req)
        return response
    except Exception as e:
        return {'error': f"update user, {str(e)}"}

@router.delete('/api/delete/user/{user_id}')
def delete_character(
    user_id: int,
    authorization: str = Header(...),
    db: session = Depends(get_db)):
    '''
    Delete a user
    '''
    try:
        if auth_token(authorization)['role'] != user_role().ADMIN:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Not authorized'
            )

        user = controller.delete_user(db, user_id)
        return {"message": "User deleted successfully", "user": user}
    except Exception as e:
        return {'error': f"delete user, {str(e)}"}
