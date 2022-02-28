from typing import Any, Dict
from django.urls import reverse

from django.http import  HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import Measurement

class HomeView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'measurements/index.html'
    context_object_name = 'latest_measurement_list'
    paginate_by = 10

    
    def get_queryset(self):
        return Measurement.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        measurements = Measurement.objects.filter(user=self.request.user).order_by('-created_at')[:7]
        dates = [data.created_at.strftime('%m/%d') for data in measurements]
        weight_data = [data.weight for data in measurements]
        fat_percentage_data = [data.fat_percentage for data in measurements]
        muscle_percentage_data = [data.muscle_percentage for data in measurements]
        calories_data = [data.calories for data in measurements]
        
        return {
                "latest_measurement_list": measurements, 
                "weight_data": weight_data, 
                "labels": dates, 
                'fat_percentage_data': fat_percentage_data, 
                'muscle_percentage_data': muscle_percentage_data,
                'calories_data': calories_data
                }
        
        
class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'measurements/list.html'
    context_object_name = 'latest_measurement_list'
    paginate_by = 10
    
    def get_queryset(self):
        return Measurement.objects.filter(user=self.request.user).order_by('-created_at')
    
    

class CreateView(LoginRequiredMixin, generic.CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Measurement
    fields = ['weight', 'fat_percentage', 'muscle_percentage', 'calories']
    
    def post(self, request, *args, **kwargs):
        print('THIS IS THE LOGGED IN USER: ', request.user.id)
        try:
            weight = request.POST['weight']
            fat_percentage = request.POST['fat_percentage']
            muscle_percentage = request.POST['muscle_percentage']
            calories = request.POST['calories']
        except (KeyError, Measurement.DoesNotExist):
            return render(request, 'measurements/create.html', {'error_message': "Debes llenar todos los campos"})
        except:
            return render(request, 'measurements/create.html', {'measurement': measurement, 'error_message': "Asegúrate de que los campos sean numéricos."})
        else:   
            measurement = Measurement.objects.create(weight=weight, fat_percentage=fat_percentage, muscle_percentage=muscle_percentage, calories=calories, user=request.user)
            measurement.save()
            
            return HttpResponseRedirect(reverse('index')) 

class DetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    model = Measurement
    template_name = 'measurements/detail.html'
    
        
def edit(request, measurement_id):
    measurement = get_object_or_404(Measurement, pk=measurement_id)
    try:
        measurement.weight = float(request.POST['weight'])
        measurement.fat_percentage = float(request.POST['fat_percentage'])
        measurement.muscle_percentage = float(request.POST['muscle_percentage'])
        measurement.calories = float(request.POST['calories'])
    except (KeyError, Measurement.DoesNotExist):
        return render(request, f'measurements/detail.html', {'measurement': measurement, 'error_message': "Debes llenar todos los campos"})
    except:
        return render(request, f'measurements/detail.html', {'measurement': measurement, 'error_message': "Asegúrate de que los campos sean numéricos."})
    else:   
        measurement.save()
        return HttpResponseRedirect(reverse('index'))

def delete(request, measurement_id):
    try:
        measurement = get_object_or_404(Measurement, pk=measurement_id)
    except Exception as e:
        return HttpResponseRedirect(reverse('index'))
    else:   
        measurement.delete()
        return HttpResponseRedirect(reverse('index'))

