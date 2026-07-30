from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound,HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string

# Create your views here.
months_list = {
    "january": "The first month of the year, often associated with new beginnings and winter in the Northern Hemisphere.",
    "february": "The second month of the year, known for being the shortest month and for Valentine's Day.",
    "march": "The third month of the year, marking the beginning of spring in the Northern Hemisphere.",
    "april": "The fourth month of the year, commonly associated with blooming flowers and warmer weather.",
    "may": "The fifth month of the year, known for pleasant spring weather and outdoor activities.",
    "june": "The sixth month of the year, marking the start of summer in the Northern Hemisphere.",
    "july": "The seventh month of the year, typically one of the warmest months in many regions.",
    "august": "The eighth month of the year, often associated with vacations and late summer.",
    "september": "The ninth month of the year, marking the beginning of autumn in the Northern Hemisphere.",
    "october": "The tenth month of the year, known for colorful autumn leaves and Halloween.",
    "november": "The eleventh month of the year, associated with cooler weather and Thanksgiving in some countries.",
    "december": "The twelfth and final month of the year, widely known for holiday celebrations and the start of winter in the Northern Hemisphere.",
}


def index(request):
    # final_list_html_li=""
    # for item in months_list.keys():
    #   name=item.capitalize()
    #   link=reverse("monthly-challenges",args=[item])
    #   final_list_html_li +=f"<li><a href=\"{link}\">{name}</a></li>"
    # wrapper=f"<ul>{final_list_html_li}</ul>"  
    # return HttpResponse(wrapper)
    return render(request,"challenges/index.html",{"months":months_list.keys(),'title':"Homepage"})

def dynamic_month_by_name(request, month):
    
    try:
        month_val = months_list.get(str(month.lower()),None)
        #return HttpResponse(f"<h1>{month_val}<h1>")
        if month_val is not None :
         return render(request,"challenges/dynamic-challege.html",{"text":month_val,'month_name':month.capitalize(),'month_dictonary':months_list})
        else:
         return HttpResponse(render_to_string("404.html"))
    except ValueError:
        # return HttpResponseNotFound("This month is not supported!")
       return HttpResponse(render_to_string("404.html"))
  
    
def dynamic_month_by_index(request, month):
 month_list=list(months_list.keys())
 search_key=month-1
 if search_key < 0 or search_key >= len(month_list):
    #  return HttpResponseNotFound("This month is not supported!")
    return HttpResponse(render_to_string("404.html"))
 else:  
    redirect_month_in_string=month_list[search_key]
    dynamic_redirect_route=reverse("monthly-challenges",args=[redirect_month_in_string])
    return HttpResponseRedirect(dynamic_redirect_route)

def template_rendering(request):
    return HttpResponse(render_to_string("challenges/index.html"))