from django.shortcuts import render,redirect
from .forms import CityForm
import requests
from .models import City
def home_view(request):
    url ='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid='
    city = 'Mumbai'
    err_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)


        if form.is_valid():
            new_city = form.cleaned_data['name'] 

            existing_city_count = City.objects.filter(name = new_city).count()

            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City Already Exists in the Database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'


    print(err_msg)
    form = CityForm()




    cities = City.objects.all()

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city)).json()

        city_weather = {
            'city' :city.name,
            'temperature': r['main']['temp'],
            'temp_minimum' : r['main']['temp_min'],
            'temp_maximum' : r['main']['temp_max'],
            'humidity' : r['main']['humidity'],
            'description' :r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }


        weather_data.append(city_weather)

    print(weather_data)

    context = {
    'weather_data' : weather_data,
    'form': form,
    'message' : message,
    'message_class' : message_class
    }

    return render(request,'myapi/weather.html', context)


def  delete_city(request, city_name):
    City.objects.get(name = city_name).delete()

    return redirect('home')