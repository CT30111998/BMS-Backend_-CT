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
# End Uploads media path

#   ** End PATH **


#   ** URLS **
DASHBOARD_URL = '/'
USER_URLS = {
    'user': 'user/',
    'admin': 'admin/',
    'register': 'signup/',
    'login': 'login/',
    'logout': 'logout/',
    'profile': 'profile/<str:user_id>'
}
EMPLOYEE_REPORT_URLS = {
    'me': 'me/',
}
BLOG_URLS = {
    'blog': 'blog/',
    'dashboard': '',
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
    'profile': 'profile'
}

EMPLOYEE_REPORT_VIEWS_NAME = {
    'dashboard': 'me',

}

BLOG_VIEWS_NAME = {
    'dashboard': 'blog',
}

#   ** End Views name **


#   ** Static files **

# CSS File 
BOOTSTRAP_CSS = "bs5.css"
BASE_CSS = "base.css"
HEADER_CSS = "nbs5.css"
# End CSS File

# JS File
BOOTSTRAP_JS = 'bs5.js'
FONT_JS = 'font.js'
# End JS File

# Templates
BASE_TEMPLATES = {
    'dashboard': 'base.html'
}
USER_TEMPLATES = {
    'login': 'login.html',
    'profile': 'profile.html',
    'register': 'signup.html',
}

#   ** End Static files **

#   ** METHODS **
POST = 'POST'
GET = 'GET'
PUT = 'PUT'
PATCH = "PATCH"
DELETE = 'DELETE'
#   ** End Methods **


#   ** APPS **
USER_APP = 'User'
BLOG_APP = 'Blog'
WORK_APP = 'Work'
#   ** End APPS **

#   ** TEMPLATE DIR **
USER_TEMPLATE_DIR = 'user/'
BLOG_TEMPLATE_DIR = 'blog/'
WORK_TEMPLATE_DIR = 'work/'
#   ** End TEMPLATE DIR **

#   ** MODEL FIELDS **
# User 
USER_MODEL_FIELDS = {
    'id': 'id',
    'first_name': 'firstName',
    'last_name': 'lastName',
    'mobile_number': 'mNo',
    'email': 'email',
    'password': 'password',
    'confirm_password': 'confirm_password',
    'image': 'image',
    'address': 'address',
    'city': 'city',
    'state': 'state',
    'country': 'country',
    'employee_number': 'empNo',
    'about': 'about',
    'birth_date': 'birthDate',
    'date_of_joining': 'dateOfJoining',
    'join_title': 'joinTitle',
    'position': 'position',
    'department': 'department',
    'work_type': 'workType',
    'job_type': 'jobType',
    'shift': 'shift',
    'created_at': 'createdAt'}
# End User

# Blog
BLOG_MODEL_FIELDS = {
    'blog_id': 'id',
    'blog_created_at': 'created_at',
    'blog_title': 'blogTitle',
    'blog_image': 'postImage',
    'blog_desc': 'description',
    'blog_created_by': 'created_by',
    'blog_modify_at': 'modified_at',
    'like_id': 'id',
    'like_by': 'like_by',
    'blog': 'blog',
    'like': 'like',
    'like_at': 'liked_at',
    'comment_id': 'id',
    'comment': 'comment',
    'comment_by': 'comment_by',
    'comment_created_at': 'created_at'
}
# End Blog
#   ** End MODEL FIELDS **

# Session Key
SESSION_USER_ID = 'userId'
# End Session Key

#   ** Role and Permission **
OWNER = 1
ADMIN = 2
CO_ADMIN = 3
USER = 4
#   ** End Role and Permission **
# Like
LIKE = 1
UNLIKE = 0
# End Like

#   ** Alert massage **
# Common
ALL_FIELD_REQUIRE = 'All field required!'
DATA_FETCH_SUCCESSFUL = 'Data fetch successful!'
DATA_FETCH_FAIL = 'Data fetch fail!'
STARED_FIELD_REQUIRE = 'All star field require!'
DATA_NOT_FOUND = 'Data not found!'
PAYLOAD_DATA_ERROR = 'Expect payload data: '
PAYLOAD_DATA_FORMAT = 'JSON format'
# End Common
# User
LOGIN_SUCCESSFUL = 'Login successful!'
REGISTER_SUCCESSFUL = "Account create successful!"
REGISTER_FAIL = "Account create fail!"
USER_EXIST_MASSAGE = "Already exist account with this email!"
PASSWORD_LENGTH_ALERT = 'Password should have min 8 characters!'
PASSWORD_NOT_MATCH = "Password does not match!"
USER_AND_PASSWORD_NOT_MATCH = "Email and password could not match!"
UPDATE_SUCCESSFUL = "Update successful!"
LOGOUT_SUCCESSFUL = 'Logout successful!'
LOGOUT_FAIL = 'Could not logout!'
USER_NOT_LOGGED_IN = 'User not logged in!'
UPLOAD_FAIL = 'File could not upload! try again later!'
# End User

# Blog
GET_ALL_BLOG_DATA_SUCCESSFUL = 'Fetch data successful!'
GET_ALL_BLOG_DATA_FAIL = 'Fetch data fail!'
# End Blog
#   ** End alert massage **
