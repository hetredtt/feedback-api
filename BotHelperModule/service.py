from database.repository import helper_queries
from fastapi.exceptions import HTTPException

class HelperService:
    async def get_feedback_id_last(user_id):
        res = await helper_queries.get_feedback_id_by_user_id(user_id)
        return res[len(res)-1]
    
    async def get_feedback_id(user_id):
        res = await helper_queries.get_feedback_id_by_user_id_open(user_id)
        if len(res) == 0: raise IndexError
        else:
            feedback_list = {
                "feedback_list": res
            }
            return feedback_list