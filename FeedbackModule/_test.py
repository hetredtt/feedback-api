import pytest
from aiohttp import ClientSession

@pytest.mark.asyncio
async def test_feedback_atm_support_success():
    async with ClientSession() as session:           
        async with session.get('http://127.0.0.1:7000/feedback/3') as response:
            assert response.status == 200
            data = await response.json()
            assert data == {
                    "feedback_id": 3,
                    "user_id": "12",
                    "client_form": {
                        "message": None
                    },
                    "feedback_status": "Заявка отправлена",
                    "feedback_answer": "Ответа нет",
                    "feedback_type_id": 1,
                    "category": "None",
                    "atm_unique_id": "None",
                    "uploaded_file": "None"
                    }

@pytest.mark.asyncio
async def test_feedback_uzcard_success():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:7000/feedback/8') as response:
            assert response.status == 200
            data = await response.json()
            assert data == {
                    "feedback_id": 8,
                    "user_id": "12",
                    "client_form": {
                        "pan": "2412412",
                        "date": "1231214",
                        "amount": "21412",
                        "merchant_id": "1241241",
                        "terminal_id": "12412412"
                    },
                    "feedback_status": "Заявка отправлена",
                    "feedback_answer": "Ответа нет",
                    "feedback_type_id": 2,
                    "category": "None",
                    "atm_unique_id": "None",
                    "uploaded_file": "None"
                    }

@pytest.mark.asyncio
async def test_feedback_humo_success():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:7000/feedback/1') as response:
            assert response.status == 200
            data = await response.json()
            assert data == {
                    "feedback_id": 1,
                    "user_id": "135131241",
                    "client_form": None,
                    "feedback_status": "Заявка отправлена",
                    "feedback_answer": "Ответа нет",
                    "feedback_type_id": 3,
                    "category": "txt",
                    "atm_unique_id": "None",
                    "uploaded_file": "humo/перевод.txt"
                    }
            
@pytest.mark.asyncio
async def test_feedback_transfer_success():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:7000/feedback/10') as response:
            assert response.status == 200
            data = await response.json()
            assert data == {
                    "feedback_id": 10,
                    "user_id": "12",
                    "client_form": {
                        "pan": "2412412",
                        "branch_where": "2",
                        "cardholder_name": "hetredtt",
                        "branch_where_from": "1"
                    },
                    "feedback_status": "Заявка отправлена",
                    "feedback_answer": "Ответа нет",
                    "feedback_type_id": 4,
                    "category": "None",
                    "atm_unique_id": "None",
                    "uploaded_file": "None"
                    }
            
@pytest.mark.asyncio
async def test_feedback_atm_repair_success():
    async with ClientSession() as session:
        async with session.get('http://127.0.0.1:7000/feedback/9') as response:
            assert response.status == 200
            data = await response.json()
            assert data == {
                    "feedback_id": 9,
                    "user_id": "12",
                    "client_form": {
                        "state": "awad",
                        "message": "adawda",
                        "device_model": "1412412"
                    },
                    "feedback_status": "Заявка отправлена",
                    "feedback_answer": "Ответа нет",
                    "feedback_type_id": 5,
                    "category": "None",
                    "atm_unique_id": "adawdaw",
                    "uploaded_file": "None"
                    }
            
@pytest.mark.asyncio
async def test_feedback_fail():
    async with ClientSession() as session:           
        async with session.get('http://127.0.0.1:7000/feedback/0') as response:
            assert response.status == 404