from BMSystem import model_fields, decimal_constants, response_messages
from base.query_modules import save_data, get_data, update_data_by_fields, delete_data_by_filters
from base.common_helpers import create_response
from Auth.models import AuthMaster
from .models import ShiftMaster
from .serializers import ShiftSerializer
from django.utils import timezone


def api_get_shift(request_data):
    shift_id = request_data.get(model_fields.SHIFT_ID, None)
    shift_object = get_data(ShiftMaster, filters={model_fields.ID: shift_id} if shift_id else None)
    if not shift_object:
        return create_response(alert=response_messages.SHIFT_NOT_EXIST)

    if len(shift_object) != 1:
        serialize = ShiftSerializer(shift_object, many=True)
    else:
        serialize = ShiftSerializer(shift_object.first(), many=False)
    return create_response(result=True, alert=response_messages.SHIFT_GET_SUCCESS, data=serialize.data)


def api_create_update_shift(request_data, user_id):
    shift = request_data.get(model_fields.DEPARTMENT)
    shift = shift.title() if not shift.isupper() or not len(shift) < 3 else shift
    shift_id = request_data.get(model_fields.SHIFT_ID, None)

    shift_params = {
        model_fields.SHIFT: shift,
    }

    user_object = get_data(model=AuthMaster, filters={
        model_fields.ID: user_id,
        model_fields.IS_DELETED: decimal_constants.NOT_DELETED
    })

    if not user_object:
        return create_response(alert=response_messages.USER_NOT_EXIST)

    same_shift_object = get_data(model=ShiftMaster, filters={model_fields.SHIFT: shift})
    if same_shift_object:
        return create_response(alert=response_messages.SHIFT_EXIST)

    shift_object = get_data(
        model=ShiftMaster, filters={
            model_fields.ID: shift_id
        }
    )

    if not shift_object:
        shift_params.update({
            model_fields.CREATED_AT: timezone.now(),
            model_fields.CREATED_BY: user_object.first()
        })

        save_data(model=ShiftMaster, fields=shift_params)
        alert = response_messages.DEPARTMENT_CREATE_SUCCESS

    else:
        shift_params.update({
            model_fields.UPDATED_AT: timezone.now(),
            model_fields.UPDATED_BY: user_object.first()
        })
        update_data_by_fields(model_object=shift_object, fields=shift_params)
        alert = response_messages.SHIFT_UPDATE_SUCCESS

    return create_response(result=True, alert=alert)


def api_delete_shift(shift_id=None):
    delete_data = delete_data_by_filters(
        model=ShiftMaster,
        filters={model_fields.ID: shift_id}
    )
    if not delete_data:
        return create_response(alert=response_messages.SHIFT_NOT_EXIST)

    return create_response(result=True, alert=response_messages.SHIFT_DELETE_SUCCESS)


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
