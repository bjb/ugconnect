
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import decorators    # for decorators.login_required
from django.contrib.auth import models  # for models.User

import datetime


def index (request):

    return render_to_response ('index.html',
                               {},
                               context_instance = RequestContext (request))


def sponsorships (request):
    return render_to_response ('sponsorships.html',
                               {},
                               context_instance = RequestContext (request))

def whenwhere (request):
    return render_to_response ('whenwhere.html',
                               {},
                               context_instance = RequestContext (request))

def exhibitors (request):
    return render_to_response ('exhibitors.html',
                               {},
                               context_instance = RequestContext (request))
