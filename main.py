from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import FeedbackModule.controller as feedback
import AdministrationModule.controller as admin
import BotHelperModule.controller as bot

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, tags=["Administration Module"])
app.include_router(feedback.router, tags=["Feedback Module"])
app.include_router(bot.router, tags=["Bot Helper Module"])

