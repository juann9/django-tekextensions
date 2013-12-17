from django.db.models import ForeignKey
from django.forms import ModelForm
from django.forms.models import modelform_factory

from tekextensions.widgets import SelectWithPopUp, MultipleSelectWithPopUp


def add_another_popup_widget(model, form):
    """
    Adds "add another popup" widgets to FK/m2m fields of the given model form.

    If a field is not in the base fields, it would be ignore.
    """
    # Add 'add another popup' widget to all necessary fields
    for field_name in model._meta.get_all_field_names():
        field_obj, model_obj, direct, m2m = model._meta.get_field_by_name(
            field_name)
        # TODO: Improve this conditionals
        if ((not m2m and direct and isinstance(field_obj, ForeignKey)) and
                field_name in form.base_fields):
            # TODO: Improve the way the model name is acquired
            form.base_fields[field_name].widget = SelectWithPopUp(
                model=field_obj.related.parent_model.__name__.lower()
            )
        elif (m2m and direct) and field_name in form.base_fields:
            # TODO: check if this is the correct way to acquire the name
            form.base_fields[field_name].widget = MultipleSelectWithPopUp(
                model=field_obj.related.parent_model.__name__.lower()
            )


def get_model_form(model):
    form = modelform_factory(model)
    add_another_popup_widget(model, form)

    return form


class AddAnotherPopupForm(ModelForm):
    """
    Base form to inherit from, that automatically adds "Add another popup"
    widgets to the form fields.
    """
    def __init__(self, *args, **kwargs):
        model = self.Meta.model
        add_another_popup_widget(model, self)
        super(AddAnotherPopupForm, self).__init__(*args, **kwargs)
