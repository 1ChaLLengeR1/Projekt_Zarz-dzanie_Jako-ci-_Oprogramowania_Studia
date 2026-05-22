from fastapi import APIRouter

from api.user.login.login import router as user_login_router
from api.user.register.register import router as user_register_router
from api.user.collection.collection import router as user_collection_router
from api.user.one.one import router as user_one_router
from api.user.update.update import router as user_update_router
from api.user.delete.delete import router as user_delete_router

api_router = APIRouter()

api_router.include_router(user_login_router)
api_router.include_router(user_register_router)
api_router.include_router(user_collection_router)
api_router.include_router(user_one_router)
api_router.include_router(user_update_router)
api_router.include_router(user_delete_router)
