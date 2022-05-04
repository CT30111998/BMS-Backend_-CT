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
DASHBOARD_URL = ''
USER_URLS = {
    'user': 'user/',
    'get_all': '',
    'admin': 'admin/',
    'register': 'signup/',
    'login': 'login/',
    'logout': 'logout/',
    'profile': 'profile/'
}
EMPLOYEE_REPORT_URLS = {
    'me': 'me/',
    'attend': 'attendance/',
    'all_attend': 'all-attendance/',
    'category': 'category/',
}
BLOG_URLS = {
    'blog': 'blog/',
    'upload': 'upload/<int:blog_id>',
    'dashboard': '',
    'blog_update': 'delete/',
    'blog_like': 'like/',
    'blog_comment': 'comment/',
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
# Common
COMMON_MODEL_FIELDS = {
    "order_by": "order_by"
}
# End Common
# User 
USER_MODEL_FIELDS = {
    'username': 'username',
    'id': 'id',
    'user': 'user',
    'get_user_id': 'user_id',
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
    'get_blog_id': "blog_id",
    'blog_created_at': 'created_at',
    'blog_title': 'postTitle',
    'blog_image': 'postImage',
    'blog_desc': 'postDescription',
    'blog_created_by': 'created_by',
    'blog_modify_at': 'modified_at',
    'blog_delete': 'deleted',
    'like_id': 'id',
    'like_by': 'like_by',
    'like_status': "like_status",
    'blog': 'blog',
    'like': 'like',
    'like_at': 'liked_at',
    'comment_id': 'id',
    'comment': 'comment',
    'comment_by': 'comment_by',
    'comment_created_at': 'created_at'
}
# End Blog
# Work Model
WORK_MODEL_FIELDS = {
    'punch_in': 'punchIn',
    'punch_out': 'punchOut',
    'attendance_id': 'id',
    'day': 'day',
    'month': 'month',
    'year': 'year',
    'date': 'date',
    'punch_status': 'punch_status',
    'attend_id': 'attend_id',
    'created_by': 'created_by',
    'updated_by': 'updated_by',
    'emp_id': 'emp_id',
    'cat_name': "categoryName",
    'get_cat_id': 'cat_id',
    'cat_id': 'id',
}
#   ** End MODEL FIELDS **

# Session Key
SESSION_USER_ID = 'user_id'
SESSION_EMAIL = 'email'
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
BLOG_DELETE_NUM = 1
BLOG_NOT_DELETE_NUM = 0
# End Like
# Work
PUNCH_IN_STATUS = 1
PUNCH_OUT_STATUS = 2
# End work
#   Order by
ORDER_BY_DATE_DESCENDING = 1
ORDER_BY_DATE_ASCENDING = 2
ORDER_BY_FIRST_ASCENDING = 3
ORDER_BY_FIRST_DESCENDING = 4
ORDER_BY_LAST_NAME_ASCENDING = 5
ORDER_BY_LAST_NAME_DESCENDING = 6
#   End Order by

#   ** Alert massage **
# Common
ALL_FIELD_REQUIRE = 'All field required!'
DATA_FETCH_SUCCESSFUL = 'Data fetch successful!'
DATA_FETCH_FAIL = 'Data fetch fail!'
STARED_FIELD_REQUIRE = 'All star field require!'
DATA_NOT_FOUND = 'Data not found!'
PAYLOAD_DATA_ERROR = 'Expect payload data:'
PAYLOAD_DATA_FORMAT = 'JSON format'
DATABASE_SERVER_ERROR = 'Database server error! Data save fail.'
UNEXPECTED_ERROR = "Unexpected error!"
# End Common

# User
LOGIN_SUCCESSFUL = 'Login successful!'
REGISTER_SUCCESSFUL = "Account create successful!"
USER_CREATE_FAIL_USER_MASTER = "User create fail at User Master!"
USER_CREATE_FAIL_USER_PERMISSION = "User create fail at User Permission!"
REGISTER_FAIL = "Account create fail!"
USER_EXIST_MASSAGE = "Already exist account with this email!"
PASSWORD_LENGTH_ALERT = 'Password should have min 8 characters!'
PASSWORD_NOT_MATCH = "Password does not match!"
USER_AND_PASSWORD_NOT_MATCH = "Email and password could not match!"
ACCOUNT_NOT_EXIST_WITH_EMAIL = 'Account not exist with this email!'
UPDATE_SUCCESSFUL = "Update successful!"
UPDATE_FAIL = 'Update fail!'
LOGOUT_SUCCESSFUL = 'Logout successful!'
LOGOUT_FAIL = 'Could not logout!'
USER_NOT_LOGGED_IN = 'User not logged in!'
USER_LOGGED_IN = "User already logged in! please logout and try again."
UPLOAD_FAIL = 'File could not upload! try again later!'
DELETE_USER_SUCCESSFUL = 'User delete successful!'
USER_NOT_EXIST = 'User not exits!'
# End User

# Blog
GET_ALL_BLOG_DATA_SUCCESSFUL = 'Fetch data successful!'
GET_ALL_BLOG_DATA_FAIL = 'Fetch data fail!'
ONE_FIELD_REQUIRED_FROM_FIELDS = "One field required from"
CREATE_BLOG_SUCCESSFUL = "Blog create successful!"
BLOG_UPDATE_SUCCESSFUL = "Blog update successful!"
BLOG_NOT_EXIST = "Blog not exist!"
BLOG_NOT_DELETE = "Blog could not delete!"
BLOG_DELETE_SUCCESSFUL = "Blog delete successful!"
BLOG_LIKE_SUCCESSFUL = 'Blog like successful!'
BLOG_UNLIKE_SUCCESSFUL = 'Blog unlike successful!'
CREATE_COMMENT_SUCCESSFUL = "Comment create successful!"
UPDATE_COMMENT_SUCCESSFUL = "Comment update successful!"
DELETE_COMMENT_SUCCESSFUL = 'Comment delete successful!'
COMMENT_NOT_EXIST = 'Comment not exist!'
# End Blog

# Attendance Work
CREATE_ATTENDANCE_SUCCESSFUL = "Attendance create Successful!"
CREATE_ATTENDANCE_FAIL = "Attendance create Fail!"
UPDATE_ATTENDANCE_SUCCESSFUL = "Attendance update Successful!"
UPDATE_ATTENDANCE_FAIL = "Attendance update Fail!"
DELETE_ATTENDANCE_SUCCESSFUL = "Attendance delete Successful!"
DELETE_ATTENDANCE_FAIL = "Attendance delete Fail!"
ATTEND_NOT_FOUND = "Attendance not exist!"
EMP_NOT_EXIST = "Employee not exist!"
# End Attendance Work
# Category work
CATEGORY_CREATE_SUCCESSFUL = "Category create successful!"
CAT_UPDATE_SUCCESSFUL = "Category update successful!"
CAT_NOT_EXIST = "Category not exist!"
CAT_ALREADY_EXIST = "Category already exist! please create different category."
# End Category work
FILE_UPLOAD_FAILURE = "File upload failed!"
INVALID_FILE_TYPE = "Invalid file type"
MAX_FILE_SIZE_LIMIT_REACHED = "Max file size limit reached!"
FILE_DELETION_FAILURE = "File deletion failure!"
FILE_UPLOAD_SUCCESS = "File upload successful!"
#   ** End alert massage **

IMAGE_MIME_TYPES = ['image/jpeg', 'image/png']
MAX_FILE_SIZE = 5000000  # 5 MB
