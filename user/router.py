from fastapi import APIRouter, Depends
from auth.deps_auth import get_current_user
from auth.schemas import UserSchema


router = APIRouter()


@router.get("/me")
def my_details(current_user: UserSchema = Depends(get_current_user)):
    """My details
    
    Get details of the current logged in users.
    """
    return current_user