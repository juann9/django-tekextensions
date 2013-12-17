from django.forms.models import modelform_factory
from django.db.models.loading import get_models, get_apps


def get_model_form(model_name):
    app_list = get_apps()
    for app in app_list:
        for model in get_models(app):
            if model.__name__ == model_name:
                form = modelform_factory(model)
                return form

    raise Exception('Did not find the model %s' % model_name)
