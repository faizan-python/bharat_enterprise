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
    Item
)


def item_amount_calculate(item_data):
    item_obj = []
    item_total_cost = 0
    total_weight = 0
    for item in item_data:
        if item:
            if item.get('item_name') and item.get('price') and item.get('weight'):
                total_amount = float(
                    item.get('price')) * float(item.get('weight'))
                obj = Item.objects.create(item_name=item.get('item_name'),
                                          price=item.get('price'),
                                          weight=item.get(
                                              'weight'),
                                          total_amount=total_amount)

                item_total_cost += (float(obj.price)
                                    * float(obj.weight))
                total_weight += float(obj.weight)
                item_obj.append(obj)
    return (item_obj, item_total_cost, total_weight)


@require_http_methods(["GET"])
@login_required(login_url='/')
def invoice_add(request):
    if request.method == "GET":
        context = RequestContext(request, {
            "companys": Company.objects.filter(is_active=True),
            "vendors": Vendor.objects.filter(is_active=True)})
        return render_to_response('invoice/invoice.html',
                                  context_instance=context)


@require_http_methods(["POST"])
@login_required(login_url='/')
def invoice_create(request):
    if request.method == "POST":
        data = request.POST.dict()
        forms = json.loads(data.keys()[0])
        vendor_form = forms.get('vendor')
        invoice_form = forms.get('invoice_deatils')
        company_id = forms.get('company')
        gender = forms.get('gender')
        vendor = Vendor.objects.filter(
            **vendor_form)
        if not vendor:
            vendor_form['created_by'] = request.user
            vendor_form['account'] = request.user.userprofile.account
            vendor_obj = Vendor.objects.create(**vendor_form)
        else:
            vendor_obj = vendor[0]
        invoice_form['vendor'] = vendor_obj

        # Vehicle form
        vehicle_form = forms.get("vehicle_form")
        vehicle_form['vendor'] = vendor_obj
        vehicle = Vehicle.objects.filter(**vehicle_form)
        if not vehicle:
            vehicle_form['created_by'] = request.user
            vehicle_form['last_visited_date'] = timezone.now()
            vehicle = Vehicle.objects.create(**vehicle_form)
        else:
            vehicle = vehicle[0]
            vehicle.last_visited_date = timezone.now()
            vehicle.save()
        invoice_form['vehicle'] = vehicle

        if company_id:
            invoice_form['company'] = Company.objects.get(id=company_id)
        invoice_form['created_by'] = request.user
        advance_payment = False
        if invoice_form.get('advance_payment'):
            if int(invoice_form.get('advance_payment')) > 0:
                invoice_form['advance_payment'] = int(
                    invoice_form.get('advance_payment'))
                advance_payment = True
                payment = Payment.objects.create(
                    payment_amount=float(invoice.get('advance_payment')),
                    recieved_by=request.user)
        else:
            invoice_form['advance_payment'] = 0

        invoice_form['account'] = request.user.userprofile.account
        invoice = Invoice.objects.create(**invoice_form)

        invoice.tax = forms.get('tax', 0)
        invoice.total_cost = forms.get('total_cost', 0)
        invoice.remark = forms.get('remark', "")
        invoice.total_paid = float(forms.get('total_paid', 0))

        total_pending = float(
            forms.get('total_cost', 0)) - float(forms.get('total_paid', 0))
        invoice.total_pending = total_pending
        if total_pending < 1:
            invoice.complete_payment = True

        if int(forms.get('total_paid')) > 0:
            payment = Payment.objects.create(payment_amount=forms.get('total_paid'),
                                             recieved_by=request.user)
            invoice.payment.add(payment)

        item_data, total_item_cost, total_weight = item_amount_calculate(
            forms.get('item_data'))

        invoice.item.add(*item_data)
        invoice.total_item_cost = total_item_cost
        invoice.total_weight = total_weight

        invoice.save()

        obj = list(Invoice.objects.filter(
            invoice_number=invoice.invoice_number).values())
        json.JSONEncoder.default = lambda self, obj: (
            obj.isoformat() if isinstance(obj, datetime.datetime) else None)
        return HttpResponse(json.dumps(obj), content_type="application/json")


@require_http_methods(["GET"])
@login_required(login_url='/')
def invoice_search(request):
    if request.method == "GET":
        context = RequestContext(request, {
            "invoices": Invoice.objects.filter(
                account=request.user.userprofile.account,
                is_active=True).only("invoice_number",
                                     "company",
                                     "vehicle",
                                     "total_weight",
                                     "date",
                                     "total_cost",
                                     "vendor")})
        return render_to_response('invoice/invoicesearch.html',
                                  context_instance=context)


# @require_http_methods(["GET"])
# @login_required(login_url='/')
# def service_view(request, id):
#     if request.method == "GET":
#         service_obj = Service.objects.filter(invoice_number=id)
#         if service_obj:
#             context = RequestContext(request, {
#                 "service": service_obj[0]})
#             return render_to_response('service/viewservice.html',
#                                       context_instance=context)
#         return HttpResponseRedirect("/home/")


# @require_http_methods(["GET"])
# @login_required(login_url='/')
# def service_pending(request):
#     if request.method == "GET":
#         context = RequestContext(request, {
#             "services": Service.objects.filter(
#                 is_active=True, is_serviced=False)})
#         return render_to_response('service/pendingservice.html',
#                                   context_instance=context)


# @require_http_methods(["GET", "POST"])
# @login_required(login_url='/')
# def service_edit(request, id):
#     if request.method == "GET":
#         service_obj = Service.objects.filter(invoice_number=id)
#         if service_obj:
#             context = RequestContext(request, {
#                 "service": service_obj[0]})
#             return render_to_response('service/editservice.html',
#                                       context_instance=context)
#         return HttpResponseRedirect("/home/")
#     if request.method == "POST":
#         return HttpResponse("EDit")


# @require_http_methods(["GET"])
# @login_required(login_url='/')
# def invoice_get(request, id):
#     if request.method == "GET":
#         service_obj = Service.objects.filter(invoice_number=id)
#         if service_obj:
#             context = RequestContext(request, {
#                 "service": service_obj[0]})
#             return render_to_response('service/invoice.html',
#                                       context_instance=context)
#         return HttpResponseRedirect("/home/")
#     if request.method == "POST":
#         return HttpResponse("EDit")


# @require_http_methods(["GET", "POST"])
# @login_required(login_url='/')
# def create_invoice(request):
#     if request.method == "GET":
#         service_objs = Service.objects.filter(
#             is_serviced=False, is_active=True)
#         context = RequestContext(request, {
#             "services": service_objs})
#         return render_to_response('service/invoicecreate.html',
#                                   context_instance=context)

#     if request.method == "POST":
#         return HttpResponse("EDit")


# @require_http_methods(["GET", "POST"])
# @login_required(login_url='/')
# def invoice(request):
#     if request.method == "POST":
#         request_dict = request.POST.dict()
#         data = json.loads(request_dict.keys()[0])
#         service_obj = Service.objects.filter(
#             invoice_number=data.get('service_id'))
#         if service_obj:
#             service_obj = service_obj[0]
#             if not service_obj.is_serviced:
#                 service_obj.is_serviced = True
#                 service_obj.labour_cost = data.get('labour_cost', 0)
#                 service_obj.tax = data.get('tax', 0)
#                 service_obj.total_cost = data.get('total_cost', 0)
#                 service_obj.remark = data.get('remark', "")
#                 if data.get('next_service_date'):
#                     service_obj.next_service_date = datetime.datetime.strptime(
#                         data.get('next_service_date'), "%m/%d/%Y").date()
#                 service_obj.delivery_date = timezone.now()
#                 service_obj.total_paid += int(data.get('total_paid', 0))
#                 if int(data.get('total_paid')) > 0:
#                     payment = Payment.objects.create(payment_amount=data.get('total_paid'),
#                                                      recieved_by=request.user)
#                     service_obj.payment.add(payment)
#                 total_pending = int(
#                     data.get('total_cost', 0)) - int(data.get('total_paid', 0))
#                 total_pending -= service_obj.advance_payment
#                 service_obj.total_pending = total_pending
#                 if total_pending < 1:
#                     service_obj.complete_payment = True

#                 part_data = data.get('part_data')
#                 part_obj = []
#                 part_total_cost = 0
#                 for part in part_data:
#                     if part:
#                         if part.get('part_name') and part.get('price'):
#                             obj = Part.objects.create(part_name=part.get('part_name'),
#                                                       price=part.get('price'),
#                                                       part_quantity=part.get(
#                                                           'part_quantity'),
#                                                       created_by=request.user)
#                             part_total_cost += (int(obj.price)
#                                                 * int(obj.part_quantity))
#                             part_obj.append(obj)

#                 labour_data = data.get('labour_data')
#                 labour_obj = []
#                 labour_total_cost = 0
#                 for labour in labour_data:
#                     if labour:
#                         if labour.get('name') and labour.get('labour_price'):
#                             obj = LabourCost.objects.create(
#                                 name=labour.get('name'),
#                                 labour_price=labour.get('labour_price'),
#                                 created_by=request.user)
#                             labour_total_cost += int(obj.labour_price)
#                             labour_obj.append(obj)

#                 service_obj.parts.add(*part_obj)
#                 service_obj.labourcost_detail.add(*labour_obj)
#                 service_obj.part_cost = part_total_cost
#                 service_obj.save()
#                 return HttpResponse("Invoice Generated Successfilly")
#             return HttpResponseRedirect("/home/")


# @require_http_methods(["POST"])
# @login_required(login_url='/')
# def pending_payment(request):
#     if request.method == "POST":
#         request_dict = request.POST.dict()
#         data = json.loads(request_dict.keys()[0])
#         service_obj = Service.objects.filter(
#             invoice_number=data.get('service_id'))
#         if service_obj:
#             service_obj = service_obj[0]
#             if service_obj.is_serviced:
#                 pending_amount = service_obj.total_pending - \
#                     data.get('pending_payment')

#                 if int(data.get('pending_payment')) > 0:
#                     payment = Payment.objects.create(
#                         payment_amount=data.get('pending_payment'),
#                         recieved_by=request.user)
#                     service_obj.payment.add(payment)
#                 if pending_amount < 1:
#                     service_obj.complete_payment = True

#                 service_obj.total_paid += data.get('pending_payment')
#                 service_obj.total_pending = pending_amount
#                 service_obj.save()
#                 return HttpResponse("Pending payment Complete")
#             return HttpResponseRedirect("/home/")


# @require_http_methods(["GET"])
# @login_required(login_url='/')
# def invoice_view(request, id):
#     if request.method == "GET":
#         service_obj = Service.objects.filter(is_active=True, invoice_number=id)
#         if service_obj:
#             context = RequestContext(request, {
#                 "service": service_obj[0]})
#             return render_to_response('service/invoicepdf.html',
#                                       context_instance=context)


# @require_http_methods(["GET", "POST"])
# @login_required(login_url='/')
# def report(request):
#     if request.method == "GET":
#         context = RequestContext(request, {})
#         return render_to_response('service/report.html',
#                                   context_instance=context)
#     if request.method == "POST":
#         request_dict = request.POST.dict()
#         from_date = datetime.datetime.strptime(request_dict.get("from_date"), "%m/%d/%Y").date()
#         till_date = datetime.datetime.strptime(request_dict.get("till_date"), "%m/%d/%Y").date()
#         if request_dict.get('pending'):
#             complete_payment = False
#         else:
#             complete_payment = True

#         service_obj = Service.objects.filter(service_date__gte=from_date,
#                                              service_date__lte=till_date,
#                                              complete_payment=complete_payment,
#                                              is_serviced=True)
#         template = get_template('service/reportview.html')
#         context = Context({'services': service_obj, 'from': from_date,
#                            "till": till_date})
#         content = template.render(context)
#         return HttpResponse(content)


# @require_http_methods(["GET", "POST"])
# @login_required(login_url='/')
# def customer_report(request):
#     if request.method == "GET":
#         context = RequestContext(request, {
#             "customers": Customer.objects.filter(is_active=True)
#             })
#         return render_to_response('service/customerreport.html',
#                                   context_instance=context)
#     if request.method == "POST":
#         request_dict = dict(request.POST.iterlists())
#         customer_id = request_dict.get("customer_id")
#         pending = request_dict.get("pending")
#         if pending:
#             complete_payment = False
#         else:
#             complete_payment = True

#         customer_obj = Customer.objects.get(id=customer_id[0])

#         service_obj = Service.objects.filter(customer=customer_obj,
#                                              is_serviced=True)
#         template = get_template('service/customerreportview.html')
#         context = Context({'services': service_obj, 'customer': customer_obj})
#         content = template.render(context)
#         return HttpResponse(content)


# @require_http_methods(["GET"])
# @login_required(login_url='/')
# def invoice_list(request):
#     if request.method == "GET":
#         context = RequestContext(request, {
#             "services": Service.objects.filter(
#                 is_active=True,
#                 is_serviced=True).only("invoice_number",
#                                        "customer",
#                                        "vehical",
#                                        "is_serviced",
#                                        "service_date",
#                                        "total_pending",
#                                        "total_paid")})
#         return render_to_response('service/listinvoice.html',
#                                   context_instance=context)


# @require_http_methods(["GET"])
# @login_required(login_url='/')
# def customer_report_generate(request, id):
#     if request.method == "GET":
#         customer_obj = Customer.objects.get(id=id)

#         service_obj = Service.objects.filter(customer = customer_obj,
#                                              is_serviced=True)
#         total_cost = 0
#         total_paid = 0
#         total_pending = 0
#         for service in service_obj:
#             total_cost += service.total_cost
#             total_paid += service.total_paid
#             total_pending += service.total_pending

#         context = RequestContext(request, {
#             'services': service_obj,
#             'customer': customer_obj,
#             'total_pending': total_pending,
#             'total_paid': total_paid,
#             'total_cost': total_cost})
#         return render_to_response('service/customerreportpdf.html',
#                           context_instance=context)


# @require_http_methods(["GET", "POST"])
# @login_required(login_url='/')
# def report_generate(request):
#     if request.method == "POST":
#         request_dict = request.POST.dict()
#         from_date = datetime.datetime.strptime(request_dict.get("from_date"), "%m/%d/%Y")
#         till_date = datetime.datetime.strptime(request_dict.get("till_date"), "%m/%d/%Y")
#         if request_dict.get('pending'):
#             complete_payment = False
#         else:
#             complete_payment = True

#         service_obj = Service.objects.filter(service_date__gt=from_date,
#                                              service_date__lt=till_date,
#                                              complete_payment=complete_payment,
#                                              is_serviced=True)

#         total_cost = 0
#         total_paid = 0
#         total_pending = 0
#         for service in service_obj:
#             total_cost += service.total_cost
#             total_paid += service.total_paid
#             total_pending += service.total_pending

#         context = RequestContext(request, {
#             "services": service_obj,
#             "from_date": from_date.date(),
#             "till_date": till_date.date(),
#             'total_pending': total_pending,
#             'total_paid': total_paid,
#             'total_cost': total_cost})
#         return render_to_response('service/reportpdf.html',
#                           context_instance=context)
