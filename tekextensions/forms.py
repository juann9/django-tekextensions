from django.forms.models import modelform_factory
from django.db.models import ForeignKey
from django.db.models.loading import get_models, get_apps


from tekextensions.widgets import SelectWithPopUp, MultipleSelectWithPopUp


def get_model(model_name):
    app_list = get_apps()
    for app in app_list:
        for model in get_models(app):
            if model.__name__ == model_name:
                return model

    raise Exception('Did not find the model %s' % model_name)


def get_model_form(model_name):
    model = get_model(model_name)
    form = modelform_factory(model)
    return form


def add_popup_to_fields(model, form):
    for field_name in model._meta.get_all_field_names():
        field_obj, model_obj, direct, m2m = model._meta.get_field_by_name(
            field_name)
        if not m2m and direct and isinstance(field_obj, ForeignKey):
            form.base_fields[field_name].widget = SelectWithPopUp()
        elif m2m and direct:
            form.base_fields[field_name].widget = MultipleSelectWithPopUp()

    return form
