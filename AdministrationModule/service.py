from database.repository import administration_queries

class AdministrationService:
    async def find_user(telegram_user_id):
        user = await administration_queries.get_user_by_id(telegram_user_id)
        if len(user) == 0: raise IndexError
        else: return user[0]
        
    async def create_user(name, mobile, telegram_user_id):
        return await administration_queries.insert_user(name, mobile, telegram_user_id)
