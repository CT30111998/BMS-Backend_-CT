from BMSystem import response_messages
from base.common_helpers import create_response as my_response


def get_all_cat():
    # user_id = my_session_get(request, constants.SESSION_USER_ID)
    # if not user_id:
    #     user_id = loads(request.body)[model_fields.USER_ID]
    #     return my_response(result=False, alert=constants.USER_NOT_LOGGED_IN)
    # get_cats = CatMaster.objects.all()
    cat_list = []
    # for cat in get_cats:
    #     get_user = MasterUser.objects.get(**{model_fields.USER: user_id})
    #     user_name = my_name_create(get_user)
    #     cat_dict = {
    #         constants.WORK_MODEL_FIELDS["cat_name"]: getattr(cat, constants.WORK_MODEL_FIELDS['cat_name']),
    #         constants.WORK_MODEL_FIELDS["created_by"]: {
    #             "id": user_id, "name": user_name
    #         }
    #     }
    #     cat_list.append(cat_dict)
    return my_response(result=True, alert=response_messages.DATA_FETCH_SUCCESSFUL, data=cat_list)


def create_category(request):
    if not request:
        return my_response(result=False, alert=response_messages.UNEXPECTED_ERROR)
    # try:
    #     get_json_response = loads(request.body)
    #     get_cat_name = get_json_response[constants.WORK_MODEL_FIELDS['cat_name']].capitalize()
    #     cat_id = None
    #     if constants.WORK_MODEL_FIELDS['get_cat_id'] in get_json_response:
    #         cat_id = get_json_response['get_cat_id']
    #
    # except:
    #     alert = my_payload_error(
    #         constants.WORK_MODEL_FIELDS['cat_name'],
    #     )
    #     return my_response(result=False, alert=alert)
    # get_user_master = AuthUser.objects.get(
    #     **{model_fields.ID: user_id}
    # )
    # cat_params = {
    #     constants.WORK_MODEL_FIELDS['cat_name']: get_cat_name,
    #     model_fields.CREATED_BY: get_user_master
    # }
    # if cat_id:
    #     get_cat = CatMaster.objects.filter(**{
    #         constants.WORK_MODEL_FIELDS['cat_id']: cat_id
    #     })
    #     if not get_cat:
    #         alert = constants.CAT_NOT_EXIST
    #     else:
    #         get_cat.update(**cat_params)
    #         alert = constants.CAT_UPDATE_SUCCESSFUL
    # else:
    #     try:
    #         get_cat = CatMaster.objects.get(**{
    #             constants.WORK_MODEL_FIELDS['cat_name']: get_cat_name
    #         })
    #         alert = constants.CAT_ALREADY_EXIST
    #     except:
    #         create_cat = CatMaster(**cat_params)
    #         create_cat.save()
    #         alert = constants.CATEGORY_CREATE_SUCCESSFUL
    return my_response(result=True)
