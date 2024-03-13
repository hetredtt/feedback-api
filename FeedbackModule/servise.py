from database.repository import ticket_queries
import utils.json_generator as json_generator
import json
import os
import asyncio

class FeedbackService:
    async def add_atm_support_feedback(user_id, client_form, category, device_uid):
        result = await json_generator.structure_simple_message_json(client_form)
        output_json = json.dumps(result, indent=4, ensure_ascii=False)
        await ticket_queries.insert_feedback(user_id = user_id, output_json = output_json, category = category, device_uid = device_uid, ticket_type = 1)

    async def add_humo_feedback(user_id, uploaded_file):

        folder_path = f"humo"

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = f"humo/{uploaded_file.filename}"

        with open(file_path, "wb") as f:
            contents = await uploaded_file.read()
            f.write(contents)

        file_extension = uploaded_file.filename.split(".")[-1]
        await ticket_queries.insert_feedback(user_id = user_id, category = file_extension, file_base64 = file_path, ticket_type = 3)

    async def add_atm_repair_feedback(user_id, client_form, state, device_model, device_uid):
        result = await json_generator.structure_atm_repair_client_form_json(client_form, state, device_model)
        output_json = json.dumps(result, indent=4, ensure_ascii=False)
        await ticket_queries.insert_feedback(user_id = user_id, output_json = output_json, device_uid = device_uid, ticket_type = 5)

    async def add_uzcard_feedback(user_id, date, pan, amount, terminal_id, merchant_id):
        result = await json_generator.structure_uzcard_client_form_json(date, pan, amount, terminal_id, merchant_id)
        output_json = json.dumps(result, indent=4, ensure_ascii=False)
        await ticket_queries.insert_feedback(user_id = user_id, output_json = output_json, ticket_type = 2)

    async def add_transfer_feedback(user_id, cardholder_name, pan, branch_where_from, branch_where):
        result = await json_generator.structure_transfer_client_form_json(cardholder_name, pan, branch_where_from, branch_where)
        output_json = json.dumps(result, indent=4, ensure_ascii=False)
        await ticket_queries.insert_feedback(user_id = user_id, output_json = output_json, ticket_type = 4)
    
    async def get_feedback(feedback_id):
        result1 = ticket_queries.get_feedback_by_feedback_id(feedback_id)
        result2 = ticket_queries.get_feedback_additional_by_feedback_id(feedback_id)
        result = await asyncio.gather(result1, result2)
        if result[0]['feedback_type_id'] != 3:
            result[0]['client_form'] = json.loads(result[0]['client_form'])
        merged_dict = {**result[0], **result[1]}
        return merged_dict

    async def get_file(feedback_id):
        result = await ticket_queries.get_feedback_additional_by_feedback_id(feedback_id)
        media_type = "application/octet-stream"
        content_disposition = {"Content-Disposition": "attachment; filename=" + os.path.basename(result['uploaded_file'])}
        streaming_response = [result['uploaded_file'], media_type, content_disposition]
        if streaming_response[0] == 'None':
            raise FileNotFoundError
        else:
            return streaming_response

    async def structure_list_json(feedback_type, status_type):
        if feedback_type == 'HUMO':
            result = await ticket_queries.get_feedback_by_feedback_type(3, status_type)
            json_structure = await json_generator.structure_list_json(result, status_type)
            return json_structure
        elif feedback_type == 'UZCARD':
            result = await ticket_queries.get_feedback_by_feedback_type(2, status_type)
            json_structure = await json_generator.structure_list_json(result, status_type)
            return json_structure
        elif feedback_type == 'ATM_FEEDBACK':
            result = await ticket_queries.get_feedback_by_feedback_type(1, status_type)
            json_structure = await json_generator.structure_list_json(result, status_type)
            return json_structure
        elif feedback_type == 'ATM_REPAIR':
            result = await ticket_queries.get_feedback_by_feedback_type(5, status_type)
            json_structure = await json_generator.structure_list_json(result, status_type)
            return json_structure
        elif feedback_type == 'TRANSFER':
            result = await ticket_queries.get_feedback_by_feedback_type(4, status_type)
            json_structure = await json_generator.structure_list_json(result, status_type)
            return json_structure
        elif feedback_type is None:
            result = await ticket_queries.get_feedback(status_type)
            json_structure = await json_generator.structure_list_json(result, status_type)
            return json_structure
        else:
            return {"error": "Ticket type " + feedback_type + " doesn't exist"}
    
    async def put_feedback_status(feedback_id, new_status):
        await ticket_queries.update_feedback_status(feedback_id, new_status)

    async def put_feedback_answer(feedback_id, new_answer):
        await ticket_queries.update_feedback_answer(feedback_id, new_answer)

    