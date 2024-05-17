import os
import bcrypt
from jwt import encode
from fastapi import HTTPException
from fastapi.params import Depends, Depends
from fastapi import APIRouter, Depends, Header, HTTPException
from schemas.auth_schema import AuthSchema
from models.user_model import UserModel
from db_config import Session, get_db
from utils.auth import auth_token

router = APIRouter()

@router.get('/api/auth/user')
def get_auth(authorization: str = Header(...), db: Session = Depends(get_db)): # type: ignore
    try: 
        response = auth_token(authorization)
        return response
    except Exception as e:
        return {'error': f'user not authenticated, details: {str(e)}'}

@router.post('/api/auth/user')
def create_auth(req: AuthSchema, db: Session = Depends(get_db)): # type: ignore
    try:
        user = db.query(UserModel).filter_by(user_name=req.user_name).first()
        if user:
            if not bcrypt.checkpw(req.password.encode('utf-8'), user.password.encode('utf-8')):
                raise HTTPException(401, detail="passwords do not match")

            token = encode({
                'user': {
                    'id': user.id,
                    'role': user.role,
                    'full_name': user.full_name,
                    'user_name': user.user_name,
                    'photo': user.photo
                }
            }, os.getenv('JWT_SECRET'), algorithm='HS256')
        return {'x-auth-token': token}
    except Exception as e:
        raise HTTPException(401, detail=f"user not authenticated, details: {str(e)}")