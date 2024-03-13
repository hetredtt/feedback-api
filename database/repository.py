from database.db import database

class monitoring_queries:
    async def update_device_status(current_datetime_str, client_host, output_json, device_id):
        await database.connect()
        await database.execute_query("UPDATE device_status SET datetime = '%s', status = '%s', ipaddr = '%s', device_manager = '%s' WHERE device_id = '%s'" % (str(current_datetime_str), "", str(client_host), output_json, str(device_id)))

    async def select_all_device_status():
        await database.connect()
        data = await database.execute_query_select("SELECT * FROM device_status")
        return data
    
    async def get_atm_info_by_id(unique_id):
        await database.connect()
        atm_data = await database.execute_query_select(f"SELECT * FROM atm WHERE UniqueID = '{unique_id}'")
        return atm_data
    
class ticket_queries:

    async def insert_feedback(user_id = None, output_json = None, category = None, device_uid = None, file_base64 = None, ticket_type = None):
        await database.connect_to_support()
        if output_json is not None:
            query = """
            INSERT INTO feedback (user_id, client_form, feedback_status, feedback_answer, feedback_type_id) 
            VALUES ('%s', '%s', 'Заявка отправлена', 'Ответа нет', '%d')""" % (str(user_id), output_json, int(ticket_type)) + ';' + '\n' + """
            INSERT INTO feedback_additional (category, atm_unique_id, uploaded_file, feedback_type_id) 
            VALUES ('%s', '%s', '%s', '%d')""" % (str(category), str(device_uid), str(file_base64), int(ticket_type))
        else:
            query = """
            INSERT INTO feedback (user_id, client_form, feedback_status, feedback_answer, feedback_type_id) 
            VALUES ('%s', NULL, 'Заявка отправлена', 'Ответа нет', '%d')""" % (str(user_id), int(ticket_type)) + ';' + '\n' + """
            INSERT INTO feedback_additional (category, atm_unique_id, uploaded_file, feedback_type_id) 
            VALUES ('%s', '%s', '%s', '%d')""" % (str(category), str(device_uid), str(file_base64), int(ticket_type))
        await database.execute_query(query)

    async def update_feedback_status(ticket_id, new_status):
        await database.connect_to_support()
        query = "UPDATE feedback SET feedback_status = '%s' WHERE feedback_id = %d" % (str(new_status), int(ticket_id))
        await database.execute_query(query)

    async def update_feedback_answer(ticket_id, new_answer):
        await database.connect_to_support()
        query = "UPDATE feedback SET feedback_answer = '%s' WHERE feedback_id = %d" % (str(new_answer), int(ticket_id))
        await database.execute_query(query)

    async def get_feedback_by_feedback_id(ticket_id):
        await database.connect_to_support()
        query = "SELECT * FROM feedback WHERE feedback_id = %d" % (int(ticket_id))
        result = await database.execute_query_select(query, as_dict=True)
        return result[0]
    
    async def get_feedback_additional_by_feedback_id(ticket_id):
        await database.connect_to_support()
        query = "SELECT * FROM feedback_additional WHERE feedback_id = %d" % (int(ticket_id))
        result = await database.execute_query_select(query, as_dict=True)
        return result[0]
    
    async def get_feedback_by_feedback_type(ticket_type, status_type):
        await database.connect_to_support()
        if status_type == None: query = f"SELECT * FROM feedback WHERE feedback_type_id = {ticket_type}"
        else: query = f"SELECT * FROM feedback WHERE feedback_type_id = {ticket_type} AND feedback_status = '{status_type}'"
        print(query)
        result = await database.execute_query_select(query, as_dict=True)
        return result
    
    async def get_feedback(status_type):
        await database.connect_to_support()
        if status_type == None: query = f"SELECT * FROM feedback"
        else: query = f"SELECT * FROM feedback WHERE feedback_status = '{status_type}'"
        print(query)
        result = await database.execute_query_select(query, as_dict=True)
        return result

    async def get_feedback_type_by_feedback_id(ticket_id):
        await database.connect_to_support()
        query = f"SELECT feedback_type_id FROM feedback WHERE feedback_id = {ticket_id}"
        result = await database.execute_query_select(query, as_dict=True)
        return result[0]
    
class administration_queries:

    async def get_user_by_id(telegram_user_id):
        await database.connect_to_support()
        query = f"SELECT * FROM feedback_users WHERE telegram_user_id = {telegram_user_id}"
        return await database.execute_query_select(query, as_dict=True)
    
    async def insert_user(name, mobile, telegram_user_id):
        await database.connect_to_support()
        query = f"INSERT INTO feedback_users (name, mobile, telegram_user_id) VALUES ('{name}','{mobile}','{telegram_user_id}')"
        return await database.execute_query(query)
    
class helper_queries:

    async def get_feedback_id_by_user_id(user_id):
        await database.connect_to_support()
        query = f"SELECT feedback_id FROM feedback WHERE user_id = {user_id}"
        return await database.execute_query_select(query, as_dict=True)
    
    async def get_feedback_id_by_user_id_open(user_id):
        await database.connect_to_support()
        query = f"SELECT feedback_id FROM feedback WHERE user_id = {user_id} AND feedback_status != 'StatusType.CLOSED' AND feedback_status != 'StatusType.DECLINED'"
        return await database.execute_query_select(query, as_dict=True)