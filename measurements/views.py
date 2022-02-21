from django.urls import reverse

from django.http import  HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Measurement


class IndexView(generic.ListView):
    template_name = 'measurements/index.html'
    context_object_name = 'latest_measurement_list'
    
    def  get_queryset(self):
        return Measurement.objects.order_by('-created_at')[:5]
    
class DetailView(generic.DetailView):
    model = Measurement
    template_name = 'measurements/detail.html'

def edit(request, measurement_id):
    measurement = get_object_or_404(Measurement, pk=measurement_id)
    try:
        measurement.weight = request.POST['weight']
        measurement.fat_percentage = request.POST['fat_percentage']
        measurement.muscle_percentage = request.POST['muscle_percentage']
        measurement.calories = request.POST['calories']
    except (KeyError, Measurement.DoesNotExist):
        return render(request, 'measurements/edit.html', {'measurement': measurement, 'error_message': "Debes llenar todos los campos"})
    else:   
        measurement.save()
        return HttpResponseRedirect(reverse('index'))
