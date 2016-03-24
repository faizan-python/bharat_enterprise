import json

from django.core import serializers
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.http import (
    HttpResponse,
    HttpResponseBadRequest
)
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response

from vendor.models import Vendor
from vehicle.models import Vehicle
import datetime


@require_http_methods(["POST"])
@login_required(login_url='/')
def get_vendor_vehicle(request):
    if request.method == "POST":
        context = RequestContext(request)
        context_dict = {}
        vendor_id = request.POST['id']
        vendor_obj = Vendor.objects.get(id=vendor_id,
                                        is_active=True)
        vehicle = list(Vehicle.objects.filter(vendor=vendor_obj,
                                               is_active=True).values())
        vendor_obj = list(Vendor.objects.filter(id=vendor_id,
                                                is_active=True).values())
        obj = {
            "vehicle": vehicle,
            "vendor": vendor_obj
        }
        json.JSONEncoder.default = lambda self, obj: (
            obj.isoformat() if isinstance(obj, datetime.datetime) else None)
        return HttpResponse(json.dumps(obj), content_type="application/json")
