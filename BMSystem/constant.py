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
USER_URLS = {
    'dashboard': '',
    'admin': 'admin/',
    'register': 'signup/',
    'login': 'login/',
    'logout': 'logout/',
    'profile': 'profile/'
    }

EMPLOYEE_REPORT_URLS = {
    'dashboard': 'me/',
    
}

BLOG_URLS = {
    'dashboard': 'blog/',
    
}
#   ** End URLS **



#   ** Views **
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

#   ** End MODEL FIELDS **


#   ** FORM FIELDS **

# User 

#   ** End FORM FIELDS **