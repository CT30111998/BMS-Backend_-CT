def createSession(request, key, value):
    try:
        request.session[key] = value
        return value
    except:
        return None


def getSession(request, key):
    try:
        value = request.session[key]
        return value
    except:
        return None


def delSession(request, key):
    try:
        del request.session[key]
        return 1
    except:
        return None