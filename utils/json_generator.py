from database.repository import monitoring_queries
from datetime import datetime
import json
import os
import re

async def structure_status_json(text_file):
    pattern = r"USB Device: (?P<device>[^###]+) ### Status: (?P<status>[^###]+) ### ConfigManagerErrorCode: (?P<error_code>\d+)"
    matches = re.finditer(pattern, text_file)

    devices = []

    for match in matches:
        device_info = {
            "device": match.group("device").strip(),
            "status": match.group("status").strip(),
            "config_manager_error_code": int(match.group("error_code"))
        }
        devices.append(device_info)

    pattern_for_msg = r"Error connecting to OpenVPN server: (?P<openvpn>[^###]+)"
    match = re.search(pattern_for_msg, text_file)

    if match:
        result = {
            "devices": devices,
            "vpn": {
                "message": match.group("openvpn").strip()
            }
        }
    else:
        result = {
            "devices": devices,
            "vpn": {
                "message": "Connection to OpenVPN server is successful."
            }
        }

    return result

async def structure_device_list_json(data):
    devices = []
    date_format = "%Y-%m-%d %H:%M:%S"

    for section in data:
        date_object = datetime.strptime(section[2], date_format)
        current_time = datetime.now()
        time_difference = current_time - date_object
        status = 0 if time_difference.total_seconds() >= 400 else 1
        atm_data = await monitoring_queries.get_atm_info_by_id(section[1])
        atm_data = atm_data[0]
        device_info = {
            "unique_id": section[1],
            "status": str(status),
            "state": str(atm_data[1]),
            "terminal_id": str(atm_data[2]),
            "type": str(atm_data[3]),
            "model": str(atm_data[4]),
            "location": str(atm_data[5]),
        }
        devices.append(device_info)
    result = {
        "devices": devices
    }
    return result

async def structure_exist_date_files_json(jrn_files):
    jrn_files_without_extension = []
    for jrn_file in jrn_files:
        name_without_extension = os.path.splitext(jrn_file)[0]
        jrn_files_without_extension.append(name_without_extension)
    result = {
        "datetime": jrn_files_without_extension,
    }
    return result

async def structure_simple_message_json(client_form):
    result = {
        "message": client_form,
    }
    return result

async def structure_atm_repair_client_form_json(client_form, state, device_model):
    result = {
        "message": client_form,
        "state": state,
        "device_model": device_model
    }
    return result

async def structure_uzcard_client_form_json(date, pan, amount, terminal_id, merchant_id):
    result = {
        "date": date,
        "pan": pan,
        "amount": amount,
        "terminal_id": terminal_id,
        "merchant_id": merchant_id,
    }
    return result

async def structure_transfer_client_form_json(cardholder_name, pan, branch_where_from, branch_where):
    result = {
        "cardholder_name": cardholder_name,
        "pan": pan,
        "branch_where_from": branch_where_from,
        "branch_where": branch_where,
    }
    return result

async def structure_list_json(feedback, status_type):
    contents = []
    if str(status_type) != 'StatusType.CLOSED' and str(status_type) != 'StatusType.DECLINED':
        print('11111222222222')
        for feedback_contents in feedback:
            if feedback_contents['feedback_status'] != "StatusType.CLOSED" and feedback_contents['feedback_status'] != "StatusType.DECLINED":
                if feedback_contents['feedback_type_id'] != 3:
                    feedback_contents['client_form'] = json.loads(feedback_contents['client_form'])
                contents.append(feedback_contents)
    else:
        print('11111')
        for feedback_contents in feedback:
            if feedback_contents['feedback_type_id'] != 3:
                feedback_contents['client_form'] = json.loads(feedback_contents['client_form'])
            contents.append(feedback_contents)
    json_structure = {
        "contents": contents
    }
    return json_structure
