from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    name: str
    email: str
    password: str
    is_active: bool = True
    last_login: str = None
    created_at: str = None
