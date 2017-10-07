from django.http import HttpResponse
from django.http import JsonResponse
def fetchdata_getcitylist(request):
    response_data = {}
    #city_list = ["Delhi","Noida","Banglore","Gurgaon"]
    city_list = [{"name":"Delhi","url":"http://52.77.1.30:8000/static/delhi.jpg"},{"name":"Noida","url":"http://52.77.1.30:8000/static/noida.jpg"},{"name":"Bangalore","url":"http://52.77.1.30:8000/static/bangalore.jpg"},{"name":"Gurgaon","url":"http://52.77.1.30:8000/static/gurgaon.jpg"}]
    default_city = "Noida"
    response_data['result'] = 'success'
    response_data['data'] = {}
    response_data['data']["cities"] = city_list
    response_data['data']["default"] = default_city 
    return JsonResponse(response_data)
