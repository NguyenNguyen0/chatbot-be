from fastapi import APIRouter, Depends


router = APIRouter()


@router.post("/")
def login():
    return {"message": "Login"}


@router.post("/register")
def register():
    return {"message": "Register"}