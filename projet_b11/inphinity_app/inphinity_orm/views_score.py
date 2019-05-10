import threading
import os
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render
from .score_object.generate_DS_in_memory_multi_thread import GenerateDS
from .score_object.generate_DS_from_thresholds import generateFromThresholds
from .score_object.mail import Emailer
from django.contrib import messages



#Project views
@login_required
def scores_index(request):
    diList = DomainInterationsPair.objects.all()
    dataSources = DomainSourceInformation.objects.all()
    levelInteractions = LevelInteraction.objects.all()
    context= {
        'diList': diList,
        'dataSources': dataSources,
        'levelInteractions' : levelInteractions
        }
    return render(request, 'inphinity_orm/scores/index.html',context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('log_user'))

@login_required
def generate_ds(request):
    if request.method == "POST":
        data = request.POST
        t = threading.Thread(target=ds_thread, args=[data])
        t.setDaemon(True)
        t.start()
        messages.success(request, 'Lancement de la génération des datasets !')
    return HttpResponseRedirect(reverse('scores_index'))
@login_required
def generate_ds_thresholds(request):
    binSize = request.POST.get("binsize")
    gDSThreShold = generateFromThresholds(binSize)
    print(gDSThreShold.generate_csv())

    return HttpResponseRedirect(reverse('scores_index'))

def log_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('scores_index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'inphinity_orm/scores/login.html', {})

def ds_thread(data):
    list_size = data.get("binsize").split(",")
    list_nb = data.get("binnumber").split(",")
    list_size = [ int(x) for x in list_size ]
    list_nb = [ int(x) for x in list_nb ]
    maxval = int(data.get("maxval"))
    list_ds = data.getlist("ds");
    gDS = GenerateDS(list_nb, list_size, maxval, list_ds)
    gDS.launchGeneration()
    email = Emailer("HEIG_PFAM@outlook.com", "danielpaiva@hotmail.fr", "DS generated", "The datasource was sucessfuly generated")
    email.send()

def datasets(request):
    path="./datasets"  # insert the path to your directory
    ds_list = os.listdir(path)
    ds_list.sort();
    return render(request,'inphinity_orm/scores/datasets.html', {'datasets': ds_list})

def ds_download(request, file):
    file_path = os.path.join('./datasets', file)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
