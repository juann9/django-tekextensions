from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_models, get_apps


# TODO: remove it?
def get_model(model_name):
    app_list = get_apps()
    for app in app_list:
        for model in get_models(app):
            if model.__name__ == model_name:
                return model

    raise Exception('Did not find the model %s' % model_name)


def get_model_class(model_name):
    # TODO: Handle possible model name repetition between apps
    model_type = ContentType.objects.get(model=model_name)
    return model_type.model_class()


def get_model_verbose_name(model):
    return model._meta.verbose_name or model.__name__


def get_normalized_model_name(model):
    model_name = get_model_verbose_name(model)

    # Normalize the model name
    if model_name.lower() == model_name:
        normal_model_name = model_name.capitalize()
    else:
        normal_model_name = model_name

    return normal_model_name
