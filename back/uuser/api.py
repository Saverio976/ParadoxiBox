from typing import Literal, Optional
from django.conf import settings

from ninja import Router, Schema
from ninja.security import HttpBearer

from uuser.models import UUser

router = Router(tags=["auth"])


class LoginSchema(Schema):
    bearer: Optional[str] = None


class CreateUserSchema(Schema):
    status: Literal["created", "error"]


class DeleteUserSchema(Schema):
    deleted: bool


class AuthBearer(HttpBearer):
    def __init__(self, django_secret: bool = False) -> None:
        super().__init__()
        self._django_secret = django_secret

    def authenticate(self, request, token):
        if self._django_secret:
            if token == settings.SECRET_KEY:
                return token
            return None
        if UUser.is_connected(token):
            return token
        return None


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


@router.get("/delete", auth=AuthBearer())
def delete(request):
    deleted = UUser.delete_with_bearer(request.auth)
    return {"deleted": deleted}
