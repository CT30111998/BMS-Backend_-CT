from BMSystem import response_messages, model_fields
from base.common_helpers import create_response as my_response
from Auth.models import AuthMaster as AuthUser
from .models import FeedbackMaster
from django.utils import timezone
from base.query_modules import save_data, get_data, update_data_by_filters


def get_feedback(request_data):
    feedback_object = get_data(
        model=FeedbackMaster,
        filters={'id': request_data['feedback_id']} if 'feedback_id' in request_data else None
    )
    if not feedback_object:
        return my_response(alert=response_messages.FEEDBACK_NOT_EXIST)
    data_list = list()
    for feedback in feedback_object:
        feedback_dict = {
            'id': feedback.id,
            'feedback': feedback.feedback,
            'created_by': feedback.created_by.id,
        }
        data_list.append(feedback_dict)
    return my_response(result=True, alert=response_messages.FEEDBACK_GET_SUCCESS, data=data_list)


def create_feedback(request_data, user_id=None):
    user_object = get_data(model=AuthUser, filters={'id': user_id})
    if not user_object:
        return my_response(alert=response_messages.USER_NOT_EXIST)

    feedback_save = save_data(model=FeedbackMaster, fields={
        model_fields.CREATED_BY: user_object.first(),
        'feedback': request_data['feedback'].capitalize(),
        model_fields.CREATED_AT: timezone.now()
    })

    if not feedback_save:
        return my_response(alert=response_messages.UNEXPECTED_ERROR)

    return my_response(result=True, alert=response_messages.FEEDBACK_CREATE_SUCCESS)


def update_feedback(request_data):
    feedback_id = request_data['feedback_id']
    feedback = request_data['feedback'].capitalize()

    feedback_object = update_data_by_filters(
        model=FeedbackMaster,
        filters={'id': feedback_id},
        fields={'feedback': feedback}
    )
    if not feedback_object:
        return my_response(alert=response_messages.UNEXPECTED_ERROR)

    return my_response(result=True, alert=response_messages.FEEDBACK_UPDATE_SUCCESS)


def delete_feedback(request_data):
    feedback_id = request_data['feedback_id']
    feedback_object = get_data(model=FeedbackMaster, filters={'id': feedback_id})
    if not feedback_object:
        return my_response(alert=response_messages.FEEDBACK_NOT_EXIST)

    feedback_object.delete()
    return my_response(result=True, alert=response_messages.FEEDBACK_DELETE_SUCCESS)
