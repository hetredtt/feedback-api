from fastapi import APIRouter
from fastapi.responses import JSONResponse
from AdministrationModule.service import AdministrationService
from fastapi.exceptions import HTTPException
from utils.logger import ModuleLogger

logger = ModuleLogger(__name__).get_logger()

router = APIRouter()

@router.get("/user/", summary="To find user")
async def find_user(
    user_id: str
    ):
    '''
    **Найти пользователя**

    **Foydalanuvchini toping**
    '''
    try:
        user = await AdministrationService.find_user(user_id)
        logger.info(f"User {user_id} found")
        return JSONResponse(status_code=200, content=user)
    except IndexError:
        logger.error(f"User {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Find user error: {e}. User {user_id}")
        raise HTTPException(status_code=500, detail=f"error: {e}")

@router.post("/user/", summary="To create user")
async def create_user(
    name: str,
    mobile: str,
    user_id: str
    ):
    '''
    **Создать пользователя**

    **Foydalanuvchi yarating**
    '''
    try:
        await AdministrationService.create_user(name, mobile, user_id)
        logger.info(f"User {user_id} created")
        raise HTTPException(status_code=201, detail=f"User {name} was successfully added!")
    except Exception as e:
        logger.error(f"Create user error: {e}. User {user_id}")
        raise HTTPException(status_code=500, detail=str(e))