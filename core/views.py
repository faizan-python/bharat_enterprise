from datetime import datetime

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home/')
    return render(request, 'core/login.html')


@login_required(login_url='/')
def home(request):
    today = datetime.now()
    context = RequestContext(request, {})
    return render_to_response('core/context.html',
                              context_instance=context)


@require_http_methods(["POST"])
def verify(request):
    username = request.POST['username']
    password = request.POST['password']
    import pdb;pdb.set_trace()
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            return HttpResponse("Success")
    else:
        return HttpResponse("Username and Password do not match")


@login_required(login_url='/')
def page_not_found_error(request, template_name='404.html'):
    return render_to_response(template_name,
                              context_instance=RequestContext(request))


@require_http_methods(["POST"])
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponse("Success")
    else:
        return HttpResponse("Username and Password do not match")
