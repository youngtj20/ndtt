import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import requests
from xhtml2pdf import pisa
from decimal import Decimal

SECRET_KEY = os.environ.get('PIE_SECRET_KEY', '')


def render_to_pdf(template_src, context_dict={}):
     template = get_template(template_src)
     html  = template.render(context_dict)
     result = BytesIO()
     pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
     if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
     return None


def verify_payment(trans_id, mobile_number, amount):
     url = "https://pie.ng/transaction/verify/" + trans_id
     headers = {'authorization': SECRET_KEY}
     req = requests.get(url, headers=headers)
     if req.status_code == 200:
          res = req.json()
          if Decimal(res['data']['amountToPay']) >= Decimal(amount):
               return True
          else:
               return False
     else:
          return False