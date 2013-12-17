from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.html import escape

from tekextensions.forms import get_model_form
from tekextensions.utils import get_model_class, get_normalized_model_name


@login_required
def add_new_model(request, model_name, form=None):
    model_class = get_model_class(model_name)
    verbose_name = get_normalized_model_name(model_class)

    if not form:
        form = get_model_form(model_class)

    if request.method == 'POST':
        form = form(request.POST)
        if form.is_valid():
            try:
                new_obj = form.save()
            except ValidationError:
                new_obj = None

            if new_obj:
                script = ('<script type="text/javascript">'
                          'opener.dismissAddAnotherPopup(window, "%s", "%s");'
                          '</script>')
                content = script % (escape(new_obj._get_pk_val()),
                                    escape(new_obj))
                return HttpResponse(content)

    else:
        form = form()

    context = {'form': form, 'field': model_name,
               'verbose_field': verbose_name}
    return render_to_response('popup.html', context,
                              context_instance=RequestContext(request))
