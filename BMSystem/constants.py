# static attribute


#   ** PATH **

# Static PATH
CSS_URL = "/media/css/"
JS_URL = "/media/js/"
# End Static PATH

# Uploads media path 
UPLOAD_PATH = 'Uploads/'
PROFILE_PATH = 'Profiles/'
BLOG_PATH = 'Blog/'
MEDIA_PATH = 'media/'
# End Uploads media path

#   ** End PATH **

#   ** URLS **

URLS_PATH = {
    'USERS': 'users/',
    'AUTH': 'auth/',
    'DEPARTMENT': 'department/',
    'ATTENDANCE': 'attendance/',
    'FEEDBACK': 'feedback/',
    'CATEGORY': 'category/',
    'BLOG': 'blog/',
    'WORK': 'me/'
}

AUTH_URLS = {
    'ADMIN': 'admin/',
    'REGISTER': 'signup/',
    'LOGIN': 'login/',
    'LOGOUT': 'logout/',
}

USER_URLS = {
    'GET_ALL': '',
    'PROFILE': 'profile/',
    'DEPARTMENT': ''
}

EMPLOYEE_REPORT_URLS = {
    'ATTEND': '',
    'GET_ALL_ATTEND': 'all-attendance/',
    'CATEGORY': '',
    'FEEDBACK': '',
}

BLOG_URLS = {
    'UPLOAD': 'upload/<int:blog_id>',
    'GET_BLOG': '<int:blog_id>',
    'BLOG': '',
    'blog_update': 'delete/',
    'LIKE': 'like/',
    'COMMENT': 'comment/',
}
#   ** End URLS **


#   ** Views **
DASHBOARD_VIEW = 'home'
USER_VIEWS = {
    'dashboard': 'home',
    'admin': 'admin',
    'register': 'signup',
    'login': 'login',
    'logout': 'logout',
    'profile': 'profile'
}

EMPLOYEE_REPORT_VIEWS = {
    'dashboard': 'me',
    'attend': 'attend',
    'all_attend': 'all_attend',
}

BLOG_VIEWS = {
    'dashboard': 'blog',
}
#   ** End Views **


#   ** Views name **

USER_VIEWS_NAME = {
    'dashboard': 'home',
    'admin': 'admin',
    'register': 'signup',
    'login': 'login',
    'logout': 'logout',
    'profile': 'profile',
    'get_all': 'user',
}

EMPLOYEE_REPORT_VIEWS_NAME = {
    'dashboard': 'work_dashboard',
    'attend': 'attend',
    'all_attend': 'all_attend',
    'category': 'category'
}

BLOG_VIEWS_NAME = {
    'dashboard': 'blog',
    'create_blog': 'create_blog',
    'blog_update': 'blog_update',
    'blog_like': 'blog_like',
    'blog_comment': 'blog_comment',
}

#   ** End Views name **

#   ** METHODS **
POST = 'POST'
GET = 'GET'
PUT = 'PUT'
PATCH = "PATCH"
DELETE = 'DELETE'
#   ** End Methods **


#   ** APPS **
AUTH_APP = 'Auth'
USER_APP = 'User'
BLOG_APP = 'Blog'
WORK_APP = 'Work'
#   ** End APPS **


#   ** FILE UPLOAD **

IMAGE_MIME_TYPES = ['image/jpeg', 'image/png']
MAX_FILE_SIZE = 5000000  # 5 MB
