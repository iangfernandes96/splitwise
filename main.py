#!/usr/bin/python3

from fastapi import FastAPI
from routes.users import user_router
from routes.group import group_router
from routes.bills import bill_router
from routes.tally import tally_router

app = FastAPI(openapi_url="/openapi.json")

app.router.prefix = "/api"
app.include_router(user_router, prefix="/users")
app.include_router(group_router, prefix="/groups")
app.include_router(bill_router, prefix="/bills")
app.include_router(tally_router, prefix="/tally")
