from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.generic import TemplateView, DetailView, ListView, View, CreateView

from icecream import ic
from datetime import datetime

from .models import StocksModel, CustomerModel, BillModel, BillIDModel, CompanyDetailsModel
from .forms import CustomerCreationForm

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


class IndexView(TemplateView):
    template_name = "index.html"
    
class StocksView(ListView):
    template_name = "stocks.html"
    model = StocksModel
    paginate_by = 10
    
class StockSearchView(ListView):    
    model = StocksModel
    context_object_name = "stocks"
    
    def get_queryset(self):
        query = self.request.GET.get("query", "")
        if query:
            return StocksModel.objects.filter(product_name__icontains=query).values("product_name", "product_stock", "product_prize")[:10]
        return StocksModel.objects.all().values("id", "product_name", "product_stock", "product_prize")[:10]
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
            return JsonResponse(list(self.get_queryset()), safe=False) 
        return redirect("billing:index")

class CustomerSearchView(ListView):
    model = CustomerModel
    context_object_name = "customer"
    
    def get_queryset(self):
        query = self.request.GET.get("query", "")
        return CustomerModel.objects.filter(phone_no__icontains=query).values()[:5]
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            queryset = self.get_queryset()
            users = [
                {
                    "id": user["id"],
                    "phone_no": f"+{user['phone_no'].country_code}{user['phone_no'].national_number}",
                    "username": user["username"],
                    "email": user["email"],
                    "address": user["address"],
                }
                for user in queryset
            ]
            return JsonResponse(users, safe=False)
        return redirect("billing:index")

class SaveBillView(CreateView):
    model = CustomerModel
    form_class = CustomerCreationForm
    success_url = reverse_lazy('billing:index')
    
    def form_valid(self, form):
        phone_no=self.request.POST.get("phone_no", "")
        if not phone_no:
            phone_no = "1234567890" # default admin
            
        ic(phone_no)

        if CustomerModel.objects.filter(phone_no=phone_no).exists():
            customer = CustomerModel.objects.get(phone_no=phone_no)
        else:
            customer = form.save()
        
        ic(customer)
        
        bill_id = datetime.now().strftime("%Y%m%d%H%M%S")
        while BillIDModel.objects.filter(bill_id=bill_id).exists():
            bill_id += "a"
        
        billIDModel = BillIDModel.objects.create(bill_id=bill_id,
                                                 customer=customer)
        
        igst = form.cleaned_data.get("igst")
        date = form.cleaned_data.get("date")
        
        for index in range(1, int(form.cleaned_data.get("indexValue"))+1):
            BillModel.objects.create(bill=billIDModel,
                                     igst=igst,
                                     date=date,
                                     product=self.request.POST.get(f"product{index}"),
                                     price=self.request.POST.get(f"price{index}"),
                                     quantity=self.request.POST.get(f"quantity{index}"),
                                     actualamount=self.request.POST.get(f"actualamount{index}"),
                                     gstamount=self.request.POST.get(f"gstamount{index}"),
                                     totalamount=self.request.POST.get(f"totalamount{index}"))
            
        return redirect(self.success_url)
    
    def form_invalid(self, form):
        ic(form.errors)
        return redirect("billing:stocks")
    
class AllBillsView(ListView):
    template_name = "bills.html"
    model = BillIDModel
    context_object_name = 'bills' 
    paginate_by = 10
    
class SingleBillView(DetailView):
    model = BillIDModel
    template_name = "bill_detail.html"
    context_object_name = 'bill'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bill_id = self.kwargs.get('bill_id')  
        bill = BillIDModel.objects.get(bill_id=bill_id)
        products = BillModel.objects.filter(bill=bill)

        context['products'] = products 
        return context
    
    def get_object(self):
        bill_id = self.kwargs.get('bill_id')  
        return get_object_or_404(BillIDModel, bill_id=bill_id)  
    
class PDFView(View):
    def get(self, request, *args, **kwargs):
        
        bill_id = kwargs.get("bill_id")
        
        ######################################################################
        # details schorcut
        company_details = CompanyDetailsModel.objects.get(data_name="main")
        ######################################################################
        
        # create httpsresponse content type set to pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = "inline; filename='invoice.pdf'"
        
        # create canvas
        c = canvas.Canvas(response, pagesize=A4)
        
        width, height = A4
        print("width: ", width, "height: ", height) 
        # width:  595.2755905511812 height:  841.8897637795277
        
        ######################################################################
        ####################           :)             ########################
        ######################################################################
        
        # root values
        width, height = 595, 841
        
        font_family = "Helvetica"
        font_family_bold = "Helvetica-Bold"
        font_medium = 10
        font_large = 13
        line_spacing = 15
        
        margin_page_x = 25
        margin_page_y = 20
        margin_page_x_text = 5
        
        margin_x = 60
        margin_y = 30
        
        y_span = 0
        
        x_address = width - margin_page_x
        y_address = height - margin_page_y - margin_y
        
        img_logo_height = 53
        
        # set title
        c.setTitle("Invoice")
        
        # img bg
        c.drawImage(r"c:\Users\SUPER-POTATO\Desktop\Picture1.png", x=125, y=200, height=350, width=350, mask="auto")
        
        # img margin top
        c.drawImage(r"c:\Users\SUPER-POTATO\Desktop\Picture11.png", x=0, y=height - margin_page_y)
        
        # img logo
        c.drawImage(r"c:\Users\SUPER-POTATO\Desktop\Capture.PNG", x=margin_page_x, y=height - margin_page_y - margin_y - img_logo_height, width=207, height=img_logo_height)
        
        # address
        address = f"""
                        {company_details.address_line1}
                        {company_details.address_line2}
                        {company_details.address_line3}"""
        call_us = f"{company_details.contacts}"

        c.setFont(font_family_bold, font_medium)
        for line in address.splitlines():
            c.drawRightString(x_address, y_address, line)
            y_address -= line_spacing
        
        c.setFont(font_family, font_medium)
        c.drawRightString(x_address, y_address, call_us) 
        
        # Heading invoice
        heading_x = width / 2
        heading_y = 688
        heading_text = f"{company_details.bill_type}"
        c.setFont(font_family_bold, font_large) 
        c.drawCentredString(heading_x, heading_y, heading_text)  

        # Draw a box around the heading
        padding = 7
        c.setLineWidth(2)
        c.rect(margin_page_x, heading_y - padding, width-(2*margin_page_x), 18 + padding, stroke=1, fill=0)  
        
        # receiver bill
        receiver_heading = "RECEIVER (BILLTO)"
        c.drawString(margin_page_x + margin_page_x_text, y_span := heading_y - (1.5*margin_y), receiver_heading)
        y_span = 625
        y_rspan = y_span - (2*line_spacing)
        
        # receiver details
        receiver_name = "AJ"
        receiver_address = """81/4181, Ambili Towers,
Opp. Kgof Press Club Road,
Ootukuzhy Junction,
Statue Area, Trivandrum,
Kerala- 695 001."""
        
        receiver_details = f"""Name: {receiver_name}
Billing Address: 
{receiver_address}
    """
        
        c.setFont(font_family, font_medium)
        for line in receiver_details.strip().splitlines():
            c.drawString(margin_page_x+margin_page_x_text, y_span := y_span - line_spacing, line)
        
        # gst Number
        gst_number = f"GSTIN: {company_details.gst_in}"
        c.setFont(font_family_bold, font_medium)
        c.drawString(margin_page_x+margin_page_x_text, y_span:=y_span-line_spacing, gst_number)
        
        # invoice
        invoice_number = "Invoice No.: CTI0005"
        invoice_date = "Invoice Date: 18/12/2024"
        c.setFont(font_family, font_medium)
        c.drawRightString(width - margin_page_x - margin_page_x_text, y_rspan, invoice_number)
        c.drawRightString(width - margin_page_x - margin_page_x_text, y_rspan-line_spacing, invoice_date)
        y_span -= margin_y
        
        ###################################################################################
        
        def description_formatter(des: str) -> str:
            # Split the description into words
            words = des.split()
            
            # Initialize variables
            line = ""
            formatted_description = []
            
            for word in words:
                # Check if adding the next word would exceed the 32 character limit
                if len(line) + len(word) + 1 <= 32:
                    # Add the word to the current line
                    if line:
                        line += " " + word  # Add space before the word if it's not the first word
                    else:
                        line = word
                else:
                    # If the line exceeds 32 characters, add it to the formatted list and start a new line
                    formatted_description.append(line)
                    line = word  # Start the new line with the current word
            
            # Add the last line to the formatted description
            if line:
                formatted_description.append(line)
            
            # Join the lines with newline characters
            return "\n".join(formatted_description)
            
        # Sample data for the invoice
        invoice_data = [
            # table head
            ["Sn\nNo.", "Description of Services", "Qty", "Rate", "Actual\nAmt.", "IGST", "", "Total"],
            ["", "", "", "", "", "%", "Amt.", ""],
            # table body
            ["1", description_formatter("Year"), "1", "8,475.00", "8,475.00", "18", "1,525.50", "10,0.00"],
            # table footer
            ["Total", "", "", "", "", "10,000.00", "", ""],
            ["Total Amt. Before Tax:", "", "", "", "", "10,000.00", "", ""],
            ["GST:", "", "", "", "", "10,000.00", "", ""],
            ["Total Amt. Round Off.", "", "", "", "", "10,000.00", "", ""],
        ]
        
        # 00 10 20 30 40 50 60 70 
        # 01 11 21 31 41 51 61 71 
        
        # .. .. .. .. .. .. -2-2 -1-2
        # .. .. .. .. .. .. -2-1 -1-1
        
        # create table
        table = Table(invoice_data, colWidths=[30, 195, 25, 60, 60, 40, 65, 65])
        
        # Add styles to the table
        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1.5, colors.black),
            
            # table header
            ('SPAN', (0,0), (0,1)),
            ('SPAN', (1,0), (1,1)),
            ('SPAN', (2,0), (2,1)),
            ('SPAN', (3,0), (3,1)),
            ('SPAN', (4,0), (4,1)),
            ('SPAN', (7,0), (7,1)),
            ('SPAN', (5,0), (6,0)),
            
            # table footer -1
            ('SPAN', (-1,-1), (-3,-1)),
            ('SPAN', (-4,-1), (-8,-1)),
            
            # table footer -2
            ('SPAN', (-1,-2), (-3,-2)),
            ('SPAN', (-4,-2), (-8,-2)),
            
            # table footer -3
            ('SPAN', (-1,-3), (-3,-3)),
            ('SPAN', (-4,-3), (-8,-3)),
            
            # table footer -4
            ('SPAN', (-1,-4), (-3,-4)),
            ('SPAN', (-4,-4), (-8,-4)),
            
            # alignments
            ('VALIGN', (0, 2), (-1, -5), 'TOP'),   
            ('ALIGN', (2, 2), (-1, -5), 'CENTER'),   
            ('ALIGN', (2, 2), (-1, -5), 'CENTER'),   
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  
            
            # ('ALIGN', (-1, -1), (-1, -3), 'LEFT'),   
            
            ('FONTNAME', (0, 0), (-1, 0), font_family_bold),  
            ('FONTNAME', (2, 2), (-1, -1), font_family),  
            ('FONTSIZE', (0, 0), (-1, -1), font_medium),   
            
        ])
        table.setStyle(style)
        
        table_width, table_height = table.wrapOn(c, width, height)
        x_position = margin_page_x
        y_position = y_span - table_height
        y_span -= table_height 

        # Draw the table on the canvas
        table.drawOn(c, x_position, y_position)

        ###################################################################################
        
        # bank details
        y_span -= 20
        bank_details = f"""Account Holder Name: {company_details.account_holder_name}
Bank Account Number: {company_details.bank_acc_no}
Bank & Branch: {company_details.bank_branch}
IFSC Code: {company_details.ifsc_code}
UPIID: {company_details.upi_id}
GST IN: {company_details.gst_in}"""

        c.setFont(font_family_bold, font_medium)
        c.drawString(margin_page_x+margin_page_x_text, y_span:=y_span-line_spacing, "Our Bank Account Details")
        
        c.setFont(font_family, font_medium)
        for line in bank_details.splitlines():
            c.drawString(margin_page_x+margin_page_x_text, y_span:=y_span-line_spacing, line)
            
        # yspan right
        c.setFont(font_family_bold, font_medium)
        c.drawRightString(width-margin_page_x-margin_page_x_text, y_span, "For Clovion Tech Solutions Pvt. Ltd")
            
        # invoice status
        c.drawString(margin_page_x+margin_page_x_text, y_span:=y_span-line_spacing-margin_y, "Invoice Status: ")
        c.setFillColor(colors.green)
        title = "Paid" if company_details.invoice_status else "Pending"
        c.drawString(margin_page_x+margin_page_x_text+90, y_span, title)
        

        ######################################################################
        
        # finishing canvas
        c.showPage()
        c.save()
        
        return response

class TempDebug(View):
    def get(self, request):
        bill_id = 20250103115952
        bill_id_model = BillIDModel.objects.get(bill_id=bill_id)
        billq = BillModel.objects.filter(bill = bill_id_model)
        
        value = ""
        # value += str(bill_id)
        for b in billq:
            value += str(b.product)
        
        return HttpResponse(f"value: {value}")
            
    def post(self):
        ...
    
class DownloadBill(View):
    def get(self, request, *args, **kwargs):
        
        bill_id = kwargs.get("bill_id")
        bill_id_model = get_object_or_404(BillIDModel,bill_id = bill_id)
        
        bill_datas = BillModel.objects.filter(bill = bill_id_model)
        
        ######################################################################
                
        def description_formatter(des: str, length: int = 32) -> str:
            # Split the description into words
            words = des.split()
            
            # Initialize variables
            line = ""
            formatted_description = []
            
            for word in words:
                # Check if adding the next word would exceed the 32 character limit
                if len(line) + len(word) + 1 <= length:
                    # Add the word to the current line
                    if line:
                        line += " " + word  # Add space before the word if it's not the first word
                    else:
                        line = word
                else:
                    # If the line exceeds 32 characters, add it to the formatted list and start a new line
                    formatted_description.append(line)
                    line = word  # Start the new line with the current word
            
            # Add the last line to the formatted description
            if line:
                formatted_description.append(line)
            
            # Join the lines with newline characters
            return "\n".join(formatted_description)
      
        ######################################################################
        # details schorcut
        company_details = CompanyDetailsModel.objects.get(data_name="main")
        ######################################################################
        
        # create httpsresponse content type set to pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = "inline; filename='invoice.pdf'"
        
        # create canvas
        c = canvas.Canvas(response, pagesize=A4)
        
        width, height = A4
        print("width: ", width, "height: ", height) 
        # width:  595.2755905511812 height:  841.8897637795277
        
        ######################################################################
        ####################           :)             ########################
        ######################################################################
        
        # root values
        width, height = 595, 841
        
        font_family = "Helvetica"
        font_family_bold = "Helvetica-Bold"
        font_medium = 10
        font_large = 13
        line_spacing = 15
        
        margin_page_x = 25
        margin_page_y = 20
        margin_page_x_text = 5
        
        margin_x = 60
        margin_y = 30
        
        y_span = 0
        
        x_address = width - margin_page_x
        y_address = height - margin_page_y - margin_y
        
        img_logo_height = 53
        
        # set title
        c.setTitle("INVOICE")
        
        # img bg
        c.drawImage(r"c:\Users\SUPER-POTATO\Desktop\Picture1.png", x=125, y=200, height=350, width=350, mask="auto")
        
        # img margin top
        c.drawImage(r"c:\Users\SUPER-POTATO\Desktop\Picture11.png", x=0, y=height - margin_page_y)
        
        # img logo
        c.drawImage(r"c:\Users\SUPER-POTATO\Desktop\Capture.PNG", x=margin_page_x, y=height - margin_page_y - margin_y - img_logo_height, width=207, height=img_logo_height)
        
        # address
        address = f"""
                        {company_details.address_line1}
                        {company_details.address_line2}
                        {company_details.address_line3}"""
        call_us = f"{company_details.contacts}"

        c.setFont(font_family_bold, font_medium)
        for line in address.splitlines():
            c.drawRightString(x_address, y_address, line)
            y_address -= line_spacing
        
        c.setFont(font_family, font_medium)
        c.drawRightString(x_address, y_address, call_us) 
        
        # Heading invoice
        heading_x = width / 2
        heading_y = 688
        heading_text = f"{company_details.bill_type}"
        c.setFont(font_family_bold, font_large) 
        c.drawCentredString(heading_x, heading_y, heading_text)  

        # Draw a box around the heading
        padding = 7
        c.setLineWidth(2)
        c.rect(margin_page_x, heading_y - padding, width-(2*margin_page_x), 18 + padding, stroke=1, fill=0)  
        
        # receiver bill
        receiver_heading = "RECEIVER (BILLTO)"
        c.drawString(margin_page_x + margin_page_x_text, y_span := heading_y - (1.5*margin_y), receiver_heading)
        y_span = 625
        y_rspan = y_span - (2*line_spacing)
        
        # receiver details
        receiver_name = str(bill_id_model.customer.username)
        receiver_address = description_formatter(str(bill_id_model.customer.address))
#         """81/4181, Ambili Towers,
# Opp. Kgof Press Club Road,
# Ootukuzhy Junction,
# Statue Area, Trivandrum,
# Kerala- 695 001."""
        
        receiver_details = f"""Name: {receiver_name}
Billing Address: 
{receiver_address}
    """
        
        c.setFont(font_family, font_medium)
        for line in receiver_details.strip().splitlines():
            c.drawString(margin_page_x+margin_page_x_text, y_span := y_span - line_spacing, line)
        
        # gst Number
        gst_number = f"GSTIN: {company_details.gst_in}"
        c.setFont(font_family_bold, font_medium)
        c.drawString(margin_page_x+margin_page_x_text, y_span:=y_span-line_spacing, gst_number)
        
        # invoice
        invoice_number = "Invoice No.: CTI0005"
        invoice_date = "Invoice Date: 18/12/2024"
        c.setFont(font_family, font_medium)
        c.drawRightString(width - margin_page_x - margin_page_x_text, y_rspan, invoice_number)
        c.drawRightString(width - margin_page_x - margin_page_x_text, y_rspan-line_spacing, invoice_date)
        y_span -= margin_y
        
        ###################################################################################
  
        # 
            
        # Sample data for the invoice
        # table head
        invoice_data = [
            ["Sn\nNo.", "Description of Services", "Qty", "Rate", "Actual\nAmt.", "IGST", "", "Total"],
            ["", "", "", "", "", "%", "Amt.", ""],
        ]
        
        # table body
        data_act_total = 0
        data_gstamount = 0
        data_totalamount = 0
        
        for index,bill_data in enumerate(bill_datas, start=1):
            invoice_data.append([str(index), 
                                 str(description_formatter(bill_data.product)), 
                                 str(round(bill_data.quantity)), 
                                 str(bill_data.price), 
                                 str(bill_data.actualamount), 
                                 str(bill_data.igst), 
                                 str(bill_data.gstamount), 
                                 str(bill_data.totalamount)])
            
            data_act_total += bill_data.actualamount
            data_gstamount += bill_data.gstamount
            data_totalamount += bill_data.totalamount

            # table footer
        invoice_data.extend([
            ["Total", "", "", "", "", str(data_totalamount), "", ""],
            ["Total Amt. Before Tax:", "", "", "", "", str(data_act_total), "", ""],
            ["GST:", "", "", "", "", str(data_gstamount), "", ""],
            ["Total Amt. Round Off.", "", "", "", "", str(round(data_totalamount)), "", ""],
        ])
        
        # 00 10 20 30 40 50 60 70 
        # 01 11 21 31 41 51 61 71 
        
        # .. .. .. .. .. .. -2-2 -1-2
        # .. .. .. .. .. .. -2-1 -1-1
        
        # create table
        table = Table(invoice_data, colWidths=[30, 195, 25, 60, 60, 40, 65, 65])
        
        # Add styles to the table
        style = TableStyle([
            ('GRID', (0, 0), (-1, -1), 1.5, colors.black),
            
            # table header
            ('SPAN', (0,0), (0,1)),
            ('SPAN', (1,0), (1,1)),
            ('SPAN', (2,0), (2,1)),
            ('SPAN', (3,0), (3,1)),
            ('SPAN', (4,0), (4,1)),
            ('SPAN', (7,0), (7,1)),
            ('SPAN', (5,0), (6,0)),
            
            # table footer -1
            ('SPAN', (-1,-1), (-3,-1)),
            ('SPAN', (-4,-1), (-8,-1)),
            
            # table footer -2
            ('SPAN', (-1,-2), (-3,-2)),
            ('SPAN', (-4,-2), (-8,-2)),
            
            # table footer -3
            ('SPAN', (-1,-3), (-3,-3)),
            ('SPAN', (-4,-3), (-8,-3)),
            
            # table footer -4
            ('SPAN', (-1,-4), (-3,-4)),
            ('SPAN', (-4,-4), (-8,-4)),
            
            # alignments
            ('VALIGN', (0, 2), (-1, -5), 'TOP'),   
            ('ALIGN', (2, 2), (-1, -5), 'CENTER'),   
            ('ALIGN', (2, 2), (-1, -5), 'CENTER'),   
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  
            
            # ('ALIGN', (-1, -1), (-1, -3), 'LEFT'),   
            
            ('FONTNAME', (0, 0), (-1, 0), font_family_bold),  
            ('FONTNAME', (2, 2), (-1, -1), font_family),  
            ('FONTSIZE', (0, 0), (-1, -1), font_medium),   
            
        ])
        table.setStyle(style)
        
        table_width, table_height = table.wrapOn(c, width, height)
        x_position = margin_page_x
        y_position = y_span - table_height
        y_span -= table_height 

        # Draw the table on the canvas
        table.drawOn(c, x_position, y_position)

        ###################################################################################
        
        # bank details
        y_span -= 20
        bank_details = f"""Account Holder Name: {company_details.account_holder_name}
Bank Account Number: {company_details.bank_acc_no}
Bank & Branch: {company_details.bank_branch}
IFSC Code: {company_details.ifsc_code}
UPIID: {company_details.upi_id}
GST IN: {company_details.gst_in}"""

        c.setFont(font_family_bold, font_medium)
        c.drawString(margin_page_x+margin_page_x_text, y_span:=y_span-line_spacing, "Our Bank Account Details")
        
        c.setFont(font_family, font_medium)
        for line in bank_details.splitlines():
            c.drawString(margin_page_x+margin_page_x_text, y_span:=y_span-line_spacing, line)
            
        # yspan right
        c.setFont(font_family_bold, font_medium)
        c.drawRightString(width-margin_page_x-margin_page_x_text, y_span, "For Clovion Tech Solutions Pvt. Ltd")
            
        # invoice status
        c.drawString(margin_page_x+margin_page_x_text, y_span:=y_span-line_spacing-margin_y, "Invoice Status: ")
        c.setFillColor(colors.green)
        title = "Paid" if company_details.invoice_status else "Pending"
        c.drawString(margin_page_x+margin_page_x_text+90, y_span, title)
        

        ######################################################################
        
        # finishing canvas
        c.showPage()
        c.save()
        
        return response
    
class Error_404_page(TemplateView):
    template_name = "404.html"