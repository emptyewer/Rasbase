from django.shortcuts import render

from db.models import Experiment
from upload.models import Upload
# Create your views here.
def dashboard(request):
    exp_count = Experiment.objects.count()
    pending_count = Upload.objects.count()
    baits = Experiment.objects.values('bait').distinct().count()
    request.session['pending'] = pending_count
    return render(request, 'dashboard/dashboard.html', {'bait': baits,
                                                        'pending': pending_count,
                                                        'total': exp_count})
