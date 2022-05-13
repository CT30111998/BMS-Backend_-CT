from BMSystem import model_fields, decimal_constants, response_messages
from base.query_modules import save_data, get_data, update_data_by_fields, delete_data_by_filters
from base.common_helpers import create_response
from Auth.models import AuthMaster
from .models import DepartmentMaster
from .serializers import DepartmentSerializer
from django.utils import timezone


def api_get_department(request_data):
    dept_id = request_data.get(model_fields.DEPARTMENT_ID, None)
    department_object = get_data(DepartmentMaster, filters={model_fields.ID: dept_id} if dept_id else None)
    if not department_object:
        return create_response(alert=response_messages.DEPARTMENT_NOT_EXIST)

    if len(department_object) != 1:
        serialize = DepartmentSerializer(department_object, many=True)
    else:
        serialize = DepartmentSerializer(department_object.first(), many=False)
    return create_response(result=True, alert=response_messages.DEPARTMENT_GET_SUCCESS, data=serialize.data)


def api_create_update_depart(request_data, user_id):
    department = request_data.get(model_fields.DEPARTMENT)
    department = department.title() if not department.isupper() or not len(department) < 4 else department
    department_id = request_data.get(model_fields.DEPARTMENT_ID, None)

    department_params = {
        model_fields.DEPARTMENT: department,
    }

    user_object = get_data(model=AuthMaster, filters={
        model_fields.ID: user_id,
        model_fields.IS_DELETED: decimal_constants.NOT_DELETED
    })

    if not user_object:
        return create_response(alert=response_messages.USER_NOT_EXIST)

    same_department_object = get_data(model=DepartmentMaster, filters={model_fields.DEPARTMENT: department})
    if same_department_object:
        return create_response(alert=response_messages.DEPARTMENT_EXIST)

    department_object = get_data(
        model=DepartmentMaster, filters={
            model_fields.ID: department_id
        }
    )

    if not department_object:
        department_params.update({
            model_fields.CREATED_AT: timezone.now(),
            model_fields.CREATED_BY: user_object.first()
        })

        save_data(model=DepartmentMaster, fields=department_params)
        alert = response_messages.DEPARTMENT_CREATE_SUCCESS

    else:
        department_params.update({
            model_fields.UPDATED_AT: timezone.now(),
            model_fields.UPDATED_BY: user_object.first()
        })
        update_data_by_fields(model_object=department_object, fields=department_params)
        alert = response_messages.DEPARTMENT_UPDATE_SUCCESS

    return create_response(result=True, alert=alert)


def api_delete_department(department_id=None):
    delete_data = delete_data_by_filters(
        model=DepartmentMaster,
        filters={model_fields.ID: department_id}
    )
    if not delete_data:
        return create_response(alert=response_messages.DEPARTMENT_NOT_EXIST)

    return create_response(result=True, alert=response_messages.DEPARTMENT_DELETE_SUCCESS)


# def api_get_user_department():
#     user_department_object = get_data(model=UserDepartment)
#     return create_response(result=True, data=user_department_object)
#
#
# def api_create_user_department(request_data=None, user_id=None):
#     emp_id = request_data.get(model_fields.USER_ID)
#     department_id = request_data.get(model_fields.DEPARTMENT_ID)
#
#     user_department_object = get_data(model=UserDepartment, filters={model_fields.USER: emp_id})
#     if user_department_object:
#         return create_response(alert=response_messages.USER_DEPARTMENT_EXIST)
#
#     user_object = get_data(model=AuthMaster, filters={model_fields.ID: user_id})
#     if not user_object:
#         return create_response(alert=response_messages.UNEXPECTED_ERROR)
#
#     emp_object = get_data(model=AuthMaster, filters={model_fields.ID: emp_id})
#     if not emp_object:
#         return create_response(alert=response_messages.EMP_NOT_EXIST)
#
#     department_object = get_data(model=DepartmentMaster, filters={model_fields.ID: department_id})
#     if not department_object:
#         return create_response(alert=response_messages.DEPARTMENT_NOT_EXIST)
#
#     save_data(
#         model=UserDepartment,
#         fields={
#             model_fields.USER: emp_object.first(),
#             model_fields.DEPARTMENT: department_object.first(),
#             model_fields.CREATED_BY: user_object.first(),
#             model_fields.CREATED_AT: timezone.now()
#         }
#     )
#     return create_response(result=True, alert=response_messages.USER_DEPARTMENT_CREATE_SUCCESS)
#
#
# def api_update_user_department(request_data, user_id=None):
#     user_department_id = request_data.get(model_fields.USER_DEPARTMENT_ID, None)
#     department_id = request_data.get(model_fields.DEPARTMENT_ID, None)
#     emp_id = request_data.get(model_fields.USER_ID, None)
#
#     user_object = get_data(model=AuthMaster, filters={model_fields.ID: user_id})
#     if not user_object:
#         return create_response(alert=response_messages.UNEXPECTED_ERROR)
#
#     user_department_object = get_data(model=UserDepartment, filters={model_fields.ID: user_department_id})
#     if not user_department_object:
#         return create_response(alert=response_messages.USER_DEPARTMENT_NOT_EXIST)
#
#     user_department_params = {
#         model_fields.UPDATED_BY: user_object.first(),
#         model_fields.UPDATED_AT: timezone.now()
#     }
#
#     if department_id:
#         update_object = get_data(model=DepartmentMaster, filters={model_fields.ID: department_id})
#     else:
#         update_object = get_data(model=AuthMaster, filters={model_fields.ID: emp_id})
#     if not update_object:
#         return create_response(alert=response_messages.UNEXPECTED_ERROR)
#
#     user_department_params.update({
#         model_fields.DEPARTMENT if department_id else model_fields.USER: update_object.first()
#     })
#
#     update_data_by_fields(
#         model_object=user_department_object,
#         fields=user_department_params
#     )
#
#     return create_response(result=True, alert=response_messages.USER_DEPARTMENT_UPDATE_SUCCESS)
#
#
# def api_delete_user_department(request_data=None):
#     user_department_id = request_data.get(model_fields.USER_DEPARTMENT_ID, None)
#     if not user_department_id:
#         return create_response(alert=response_messages.UNEXPECTED_ERROR)
#
#     user_department_object = get_data(model=UserDepartment, filters={model_fields.ID: user_department_id})
#     if not user_department_object:
#         return create_response(alert=response_messages.USER_DEPARTMENT_NOT_EXIST)
#
#     user_department_object.delete()
#     return create_response(result=True, alert=response_messages.USER_DEPARTMENT_DELETE_SUCCESS)