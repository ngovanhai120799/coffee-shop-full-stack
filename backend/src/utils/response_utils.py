import json
from flask import Response


def get_response(status_code, body):
    response = json.dumps({
        "success": True,
        **body
    })
    return Response(response=response, status=status_code, mimetype="application/json")


def get_response_json_error(e):
    response = json.dumps({
        "success": False,
        "message": e.error["message"],
        "error": e.error["error"]
    })
    return Response(response=response, status=e.status_code, mimetype="application/json")

