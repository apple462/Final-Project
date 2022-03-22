from werkzeug.exceptions import HTTPException
from flask import make_response
import json


class NotFoundError(HTTPException):
    def __init__(self, item):
        res = {
             "error_code": 404,
             "error_message": f'{item} not found',
             "error_description": f"The {item} you requested was not found."
             }
        self.response = make_response(json.dumps(res), 404)


class BadRequestError(HTTPException):
    def __init__(self, message):
        res = {
             "error_code": 400,
             "error_message": message,
             "error_description": "This is an invalid request. One or more of the required parameters was missing or invalid."
             }
        self.response = make_response(json.dumps(res), 404)
    