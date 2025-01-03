from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import Letter_info_form,Add_items_form

from .models import letter_information,list_of_items

# Create your views here.
def homepage(request):
    if(request.method=='POST'):
        form=Letter_info_form(request.POST)
        if form.is_valid():
            form.save()
            last=letter_information.objects.last()
            data_row = [str(getattr(last, field.name)) for field in letter_information._meta.fields]
            return redirect('add-items',id=data_row[1])

    else:
        form=Letter_info_form()

    context={
        'form':form
    }

    return render(request,'Invoice/letter_info.html',context)


def add_items(request,id):

    items=list_of_items.objects.all()
    information = letter_information.objects.get(letter_id=id)

    if(request.method=='POST'):
        form=Add_items_form(request.POST)
        form_info=Letter_info_form(request.POST,instance=information)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.table_id=id
            instance.save()
            return redirect('add-items',id=id)
        
        if form_info.is_valid():
            form_info.save()
            return redirect('add-items',id=id)
    else:
        form=Add_items_form()
        form_info=Letter_info_form(instance=information)

    context = {
        'form':form,
        'form_info':form_info,
        'items':items,
        'id':id,
    }

    return render(request,'Invoice/letter_items.html',context)

def item_update(request,id,pk):
    item=list_of_items.objects.get(id=pk)
    if(request.method=='POST'):
        form=Add_items_form(request.POST, instance=item)
        if(form.is_valid()):
            form.save()
            return redirect('add-items',id=id)
    else:
        form=Add_items_form(instance=item)

    context={
        'form':form,
        'id':id,
    }
    return render(request,'Invoice/item_update.html',context)

def item_delete(request,id,pk):
    item=list_of_items.objects.get(id=pk) 
    if(request.method=='POST'):
        item.delete()
        return redirect('add-items',id=id)

    context={
        'id':id
    }
    return render(request,'Invoice/item_delete.html',context)


def history(request,id):
    if id==' ':
        info=letter_information.objects.last()   
        data_row = [str(getattr(info, field.name)) for field in letter_information._meta.fields ]
        letter_id=data_row[1]
    else:
        letter_id=id

    information = letter_information.objects.get(letter_id=letter_id)

    info=letter_information.objects.all().order_by('-id')
    items=list_of_items.objects.all()

    if(request.method=='POST'):
        new_id=request.POST.get('id')
        return redirect('history',id=new_id)

    context = {
        'id': letter_id,
        'information':information,
        'info':info,
        'items':items,
    }

    return render(request,'Invoice/history.html',context)




from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from django.apps import apps

def generate_pdf(request, id, type):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = f'{type}; filename=Letter.pdf'

    pdf=canvas.Canvas(response,pagesize=letter)
    pdf.setTitle('PDF Report')

    image_path = 'images/indianoil_image.png'  # Replace with the actual path to your image
    image = ImageReader(image_path)
    pdf.drawImage(image, x=0, y=600, width=620, height=200, mask='auto', preserveAspectRatio=True)

    info_model=letter_information.objects.get(letter_id=id)

    fontsize=12

    pdf.setFont("Helvetica-Bold", fontsize)
    
    address_start = 550
    pdf.drawString(30,address_start,'To,')
    pdf.drawString(30,address_start- fontsize - 3,'The Security In-charge')
    pdf.drawString(30,address_start- fontsize*2 - 6,f'{info_model.address}')

    pdf.drawString(470,address_start,f'Date: {info_model.date.strftime("%d/%m/%Y")}')
    
    subject_start_x=130
    subject_start_y=470
    subject_string = f'Sub: Request for {info_model.returnable} Gate Pass'
    pdf.drawString(subject_start_x,subject_start_y,subject_string)
    
    # Draw the underline
    text_width = pdf.stringWidth(subject_string, "Helvetica-Bold", fontsize)
    underline_y = subject_start_y - 2  # Position the underline slightly below the text
    pdf.line(subject_start_x, underline_y, subject_start_x + text_width, underline_y)

    pdf.setFont("Helvetica", fontsize)

    main_letter_1=f'This is to request you to allow the following from {info_model.source}'
    main_letter_2=f'to {info_model.destination}'
    pdf.drawString(40,400,main_letter_1)
    pdf.drawString(40,400-fontsize-3,main_letter_2)

    headers = [field.verbose_name.capitalize() for field in list_of_items._meta.fields]
    del headers[0]
    headers[0]='Sr.No.'
    data = [headers]

    counter=1
    queryset=list_of_items.objects.all()
    for obj in queryset:
        data_row = [str(getattr(obj, field.name)) for field in list_of_items._meta.fields ]
        if data_row[1]==id:
            del data_row[0]
            data_row[0] = str(counter)
            counter=counter+1
            data.append(data_row)

    col_widths = [50, 300, 80]
    table = Table(data,colWidths=col_widths)
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header row font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header row bottom padding
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
    ]))

    canvas_width = 600
    canvas_height = 600

    # table.wrapOn(pdf, canvas_width, canvas_height)
    table_width, table_height = table.wrapOn(pdf, canvas_width, canvas_height)
    table_y = 350 - table_height
    table.drawOn(pdf, 80, table_y)

    pdf.setFont("Helvetica-Bold", fontsize)
    pdf.drawString(400,100,info_model.name.upper())
    text_width = pdf.stringWidth(info_model.name.upper(), "Helvetica-Bold", fontsize)
    pdf.drawCentredString(400+text_width/2,100-fontsize-3,'ISO')

    pdf.save()
    return response
