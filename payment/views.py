import json
import datetime

from django.template import Context, Template
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect
)
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils import timezone
from django.template.loader import get_template

from company.models import Company
from vendor.models import Vendor
from vehicle.models import (
    Vehicle)
from invoice.models import Invoice
from payment.models import (
    Payment,
    Item,
    AdvancePayment
)


@require_http_methods(["GET"])
@login_required(login_url='/')
def advance_payment(request):
    if request.method == "GET":
        context = RequestContext(request, {
            "vendors": Vendor.objects.filter(is_active=True)})
        return render_to_response('payment/advance_payment.html',
                                  context_instance=context)


@require_http_methods(["POST"])
@login_required(login_url='/')
def advance_payment_pay(request):
    if request.method == "POST":
        vendor_id = request.POST['id']
        vendor_obj = Vendor.objects.get(id=vendor_id,
                                        is_active=True)
        advance_amount = float(request.POST['advance_amount'])
        if advance_amount > 0:
            payment = Payment.objects.create(
                payment_amount=advance_amount,
                recieved_by=request.user)

            advance_obj = AdvancePayment.objects.create(
                account=request.user.userprofile.account,
                payment=payment,
                vendor=vendor_obj,
                created_by=request.user)
            vendor_obj.advance_amount += advance_amount
            vendor_obj.save()
            return HttpResponse("Payment Successfully Done")
