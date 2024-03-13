from BotHelperModule.service import HelperService
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from utils.logger import ModuleLogger

logger = ModuleLogger(__name__).get_logger()

router = APIRouter()

@router.get("/feedback/{user_id}/feedback_id/last", summary="Get the feedback_id of the last feedback left by the user")
async def get_feedback_id_last(
    user_id: str
    ):
    '''
    **Получить feedback_id последней заявки оставленной пользователем**

    **Foydalanuvchi tomonidan qoldirilgan oxirgi dasturning feedback_id-ni oling**
    '''
    try:
        feedback_id = await HelperService.get_feedback_id_last(user_id)
        logger.info(f"Last id for user {user_id} found")
        return JSONResponse(status_code=200, content=feedback_id)
    except IndexError:
        logger.error(f"Last id for user {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.error(f"Get last id error: {e}. User {user_id}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/feedback/{user_id}/feedback_id/list", summary="Displaying a list of feedback IDs of a given user")
async def list_feedback(
    user_id: str
    ):
    '''
    **Вывод списка id заявок заданного пользователя**

    **Berilgan Foydalanuvchining ariza identifikatori ro'yxatini ko'rsatish**
    '''
    try:
        feedback_id = await HelperService.get_feedback_id(user_id)
        logger.info(f"Id list for user {user_id} found")
        return JSONResponse(status_code=200, content=feedback_id)
    except IndexError:
        logger.error(f"Feedbacks for user {user_id} not found")
        raise HTTPException(status_code=404, detail=f"There are not feedbacks for current user")
    except Exception as e:
        logger.error(f"Get id list error: {e}. User {user_id}")
        raise HTTPException(status_code=500, detail=f"error: {e}")