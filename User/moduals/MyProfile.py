from . import MySession
from models import User as UserDetails
from django.contrib.auth.models import User


def getProfile(request):

    userId = MySession.getSession(request, 'userId')
    if userId is None:
        return None
    dataN = UserDetails.objects.get(user=userId)
    dataP = User.objects.get(id=userId)
    data = [dataP, dataN]
    return data