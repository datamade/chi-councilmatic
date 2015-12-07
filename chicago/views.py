from django.shortcuts import render
from datetime import date, timedelta
from chicago.models import ChicagoBill
from councilmatic_core.models import Event
from councilmatic_core.views import *


class ChicagoIndexView(IndexView):
    template_name = 'chicago/index.html'
    bill_model = ChicagoBill

class ChicagoAboutView(AboutView):
    template_name = 'chicago/about.html'

class ChicagoBillDetailView(BillDetailView):
    model = ChicagoBill