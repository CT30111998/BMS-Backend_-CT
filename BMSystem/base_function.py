from rest_framework.response import Response


def create_response(result=False, alert=None, data=None):
    get = {"result": result, 'alert': alert, 'data': data}
    return Response(get)