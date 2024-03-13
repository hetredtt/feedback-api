from typing import Optional
from FeedbackModule.servise import FeedbackService
from fastapi import APIRouter, UploadFile, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
import FeedbackModule.model as model
from utils.logger import ModuleLogger

logger = ModuleLogger(__name__).get_logger()

router = APIRouter()

@router.post("/feedback/", summary="Add feedback", responses={
    201: {"model": model.FeedbackUpdate, "description": " Feedback was successfully inserted"},
    404: {"description": "Feedback type doesn't exist"},
    }, response_model_exclude_unset=False)
async def add_feedback(
    type: model.FeedbackType, 
    user_id: Optional[str] = None, 
    client_form: Optional[str] = None, 
    category: Optional[str] = None, 
    device_uid: Optional[str] = None, 
    date: Optional[str] = None, 
    pan: Optional[str] = None, 
    amount: Optional[str] = None, 
    terminal_id: Optional[str] = None, 
    merchant_id: Optional[str] = None,
    cardholder_name: Optional[str] = None, 
    branch_where_from: Optional[str] = None, 
    branch_where: Optional[str] = None,
    state: Optional[str] = None, 
    device_model: Optional[str] = None,
    uploaded_file: UploadFile = None
    ):
    '''
    **Add feedback. Depending on the type of ticket, some fields are required, some are not**

    **Добавить заявку. В зависимости от типа тикета некоторые поля обязательны к заполнению, некоторые нет**

    **Ilova qo'shing. Chipta turiga qarab, ba'zi maydonlarni to'ldirish kerak, ba'zilari esa yo'q**
    '''
    try:
        if type == model.FeedbackType.DEVICE_FEEDBACK:
            await FeedbackService.add_atm_support_feedback(user_id, client_form, category, device_uid)
            logger.info(f"Inserted feedback DEVICE_FEEDBACK: user_id: {user_id}, client_form: {client_form}, category: {category}, device_uid: {device_uid}")
            return JSONResponse(status_code=201, content={"status": "DEVICE_FEEDBACK Feedback was successfully inserted"})
        elif type == model.FeedbackType.HUMO_CANCEL:
            await FeedbackService.add_humo_feedback(user_id, uploaded_file)
            logger.info(f"Inserted feedback HUMO: user_id: {user_id}")
            return JSONResponse(status_code=201, content={"status": "HUMO Feedback was successfully inserted"})
        elif type == model.FeedbackType.UZCARD_CANCEL:
            await FeedbackService.add_uzcard_feedback(user_id, date, pan, amount, terminal_id, merchant_id)
            logger.info(f"Inserted feedback UZCARD: user_id: {user_id}, date: {date}, pan: {pan}, amount: {amount}, terminal_id: {terminal_id}, merchant_id: {merchant_id}")
            return JSONResponse(status_code=201, content={"status": "UZCARD Feedback was successfully inserted"})
        elif type == model.FeedbackType.TRANSFER:
            await FeedbackService.add_transfer_feedback(user_id, cardholder_name, pan, branch_where_from, branch_where)
            logger.info(f"Inserted feedback TRANSFER: user_id: {user_id}, cardholder_name: {cardholder_name}, pan: {pan}, branch_where_from: {branch_where_from}, branch_where: {branch_where}")
            return JSONResponse(status_code=201, content={"status": "TRANSFER Feedback was successfully inserted"})
        elif type == model.FeedbackType.DEVICE_REPAIR:
            await FeedbackService.add_atm_repair_feedback(user_id, client_form, state, device_model, device_uid)
            logger.info(f"Inserted feedback TRANSFER: user_id: {user_id}, client_form: {client_form}, state: {state}, device_model: {device_model}, device_uid: {device_uid}")
            return JSONResponse(status_code=201, content={"status": "ATM_Repair Feedback was successfully inserted"})
        else:
            logger.error(f"Error: Feedback type {type} doesn't exist")
            raise HTTPException(status_code=404, detail="Feedback type " + type + " doesn't exist")
    except Exception as e:
        logger.error(
            f"""Error create feedback: {e}. Form:
            type: {type}, 
            user_id: {user_id}, 
            client_form: {client_form}, 
            category: {category}, 
            device_uid: {device_uid}, 
            date: {date}, 
            pan: {pan}, 
            amount: {amount}, 
            terminal_id: {terminal_id}, 
            merchant_id: {merchant_id},
            cardholder_name: {cardholder_name}, 
            branch_where_from: {branch_where_from}, 
            branch_where: {branch_where},
            state: {state}, 
            device_model: {device_model},
            uploaded_file: {uploaded_file}"""
            )
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/feedback/{feedback_id}/status", summary="Update the status of the specified feedback", responses={
    200: {"model": model.FeedbackUpdate, "description": "Status for feedback № was successfully updeted on ' '"},
    404: {"description": "Feedback not found"},
    })
async def put_feedback_status(
    feedback_id: str, 
    status: model.StatusType
    ):
    '''
    **Обновить статус указанной заявки**

    **Belgilangan chipta holatini yangilang**
    '''
    try:
        await FeedbackService.put_feedback_status(feedback_id, status.value)
        logger.info(f"Status for feedback №{feedback_id} was successfully updeted on '{status}'")
        return JSONResponse(status_code=200, content={"status": "Status for feedback №" + str(feedback_id) + " was successfully updeted on '" + str(status) + "'"})
    except Exception as e:
        logger.error(f"Error put feedback status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/feedback/{feedback_id}/answer", summary="Update the answer of the specified feedback", responses={
    200: {"model": model.FeedbackUpdate, "description": "Answer for feedback № was successfully updeted on ' '"},
    404: {"description": "Feedback not found"},
    })
async def put_feedback_answer(
    feedback_id: str, 
    answer: str
    ):
    '''
    **Обновить ответ указанной заявки**

    **Ko'rsatilgan arizaning javobini yangilang**
    '''
    try:
        await FeedbackService.put_feedback_answer(feedback_id, answer)
        logger.info(f"Answer for feedback №{feedback_id} was successfully updeted on '{answer}'")
        return JSONResponse(status_code=200, content={"status": "Answer for feedback №" + str(feedback_id) + " was successfully updeted on '" + str(answer) + "'"})
    except Exception as e:
        logger.error(f"Error put feedback answer: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/{feedback_id}", summary="Get information on the specified feedback", responses={
    200: {"model": model.Feedback, "description": "Feedback found"},
    404: {"description": "Feedback not found"},
    })
async def get_feedback(
    feedback_id: str
    ):
    """
        **Get information on the specified application. Depending on the type of feedback, the returned json's differ**

        **Получить информацию по указанной заявке. В зависимости от типа тикета возвращаемые json'ы отличаются**

        **Ko'rsatilgan ariza bo'yicha ma'lumot oling. Chipta turiga qarab, JSON-ning qaytarilishi boshqacha**
    """
    try:
        json_structure = await FeedbackService.get_feedback(feedback_id)
        logger.info(f"Selected feedback: {feedback_id}")
        return JSONResponse(status_code=200, content=json_structure)
    except IndexError:
        logger.error(f"Feedback not found: {feedback_id}")
        raise HTTPException(status_code=404, detail="Feedback not found")
    except Exception as e:
        logger.error(f"Error select feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/feedback/{feedback_id}/file", summary="To get a file (for example, for a feedback of the humo type)", responses={
    200: {"model": model.FileResponse, "description": "Feedback file found"},
    404: {"description": "Feedback (file) not found"},
    })
async def get_file(
    feedback_id: str
    ):
    '''
    **Получить файл (к примеру, для заявки типа humo)**

    **Faylni oling (masalan, humo chiptasi uchun)**
    '''
    try:
        streaming_response = await FeedbackService.get_file(feedback_id)

        def file_generator():
            with open(streaming_response[0], "rb") as file:
                yield from file

        return StreamingResponse(file_generator(), media_type=streaming_response[1], headers=streaming_response[2])
    except IndexError:
        logger.error(f"Feedback not found: {feedback_id}")
        raise HTTPException(status_code=404, detail="Feedback not found")
    except FileNotFoundError:
        logger.error(f"Feedback file not found: {feedback_id}")
        raise HTTPException(status_code=404, detail="Feedback file not found")
    except Exception as e:
        try:
            return StreamingResponse(file_generator(), media_type=streaming_response[1])
        except:
            logger.error(f"Internal Error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/feedback/list/", summary="Output a summary of all feedbacks of the specified type", responses={
    200: {"model": model.FeedbackList, "description": "Feedback found"},
    404: {"description": "Feedback list not found"},
    })
async def list_feedback(
    feedback_type: model.FeedbackType = None,
    status_type: model.StatusType = None
    ):
    '''
    **Вывод краткого содержания всех заявок указанного типа**

    **Belgilangan turdagi barcha chiptalarning qisqacha mazmuni**
    '''
    try:
        json_structure = await FeedbackService.structure_list_json(feedback_type, status_type)
        logger.info(f"Listed {feedback_type} feedbacks with status: {status_type}")
        return JSONResponse(status_code=200, content=json_structure)
    except Exception as e:
        logger.error(f"Error list feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))

