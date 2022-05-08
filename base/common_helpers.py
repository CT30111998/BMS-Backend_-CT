from rest_framework.response import Response
from pagecalc import Paginator
from datetime import datetime
import re

from BMSystem import constants, decimal_constants


def create_response(result=False, alert=None, data=None):
    get = {"result": result, 'alert': alert, 'data': data}
    return Response(get)


def convert_time_to_timestamp(time=None):
    if not time:
        time = datetime.now()
    return int(datetime.timestamp(time))


# email validation functions
def check_email_format(email):
    regex = r"^[a-z0-9]+[\._-]*[a-z0-9]*[@][a-z0-9]+[.][a-z]{1,3}[.]?[a-z]{0,2}$"
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def get_sort_key(sort_field=None, sort_id=None):
    if sort_id:
        sort_id = int(sort_id)
    return '-' + sort_field if sort_id == decimal_constants.DESCENDING_ORDER else sort_field


def get_search_params(
        query_params=None, search_query_param='filters', search_field=None, search_value=None
):
    if search_value:
        query_param = {'{}__icontains'.format(search_field): search_value}
        query_params[search_query_param].update(query_param)


def paginate_records(page=None, record_list=None, records_per_page=decimal_constants.PAGE_SIZE, list_name=None):
    page = page - 1
    paginator = Paginator(total=len(record_list), by=records_per_page)
    page_details = paginator.paginate(page + 1)

    starting_record = page * records_per_page
    end_record = page * records_per_page + records_per_page
    required_record_list = record_list[starting_record: end_record]

    required_page_details = {
        'page': {
            'page': page_details['page']['current'],
            'pageSize': records_per_page,
            'totalEntrys': page_details['item']['totalCount'],
            'totalpage': page_details['page']['count'],
            'start': starting_record + 1,
            'end': starting_record + len(required_record_list)
        },
        list_name: required_record_list
    }
    return required_page_details
