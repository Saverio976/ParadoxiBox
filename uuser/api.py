from typing import Literal, Optional
from ninja import Router, Schema
from uuser.models import UUser
from ninja.security import HttpBearer

router = Router(tags=["auth"])

class LoginSchema(Schema):
    bearer: Optional[str] = None

class CreateUserSchema(Schema):
    status: Literal["created", "error"]

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        if UUser.is_connected(token):
            return token

@router.get("/create", response=CreateUserSchema)
def create_user(_, username: str, email: str, password: str):
    try:
        user = UUser.create(email=email, password=password, username=username)
    except Exception:
        return {"status": "error"}
    if user is None:
        return {"status": "error"}
    return {"status": "created"}

@router.get("/login", response=LoginSchema)
def login(_, email: str, password: str):
    user = UUser.connect(email=email, password=password)
    print("ici3")
    if user is None:
        print("ici2")
        return {"bearer": None}
    print("ici")
    return {"bearer": user.bearer}

@router.get("/logout", auth=AuthBearer())
def logout(request):
    UUser.disconnect(request.auth)