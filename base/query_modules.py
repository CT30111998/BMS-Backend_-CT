
def get_data(model=None, filters=None, order_by='id'):
    if filters:
        get_object = model.objects.filter(**filters).order_by(order_by)
        if not get_object:
            get_object = list()
    else:
        get_object = model.objects.all()
    return get_object


def save_data(model=None, fields=None):
    try:
        create_data = model(**fields)
        create_data.save()
        return create_data
    except:
        return False


def update_data_by_fields(model_object=None, fields=None):
    try:
        model_object.update(**fields)
        return True
    except:
        return False


def bulk_create(model=None, records=None):
    try:
        return model.objects.bulk_create(records)
    except:
        return False


def update_data_by_filters(model=None, filters=None, fields=None):
    try:
        model.objects.filter(**filters).update(**fields)
        return True
    except:
        return False


def delete_data_by_filters(model=None, filters=None):
    query_object = get_data(model=model, filters=filters)
    if not query_object:
        return False
    query_object.delete()
    return True
