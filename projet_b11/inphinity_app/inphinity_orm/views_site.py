from .forms import FamilyForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Family


# Create your views here.
def family_all(request):
    families_list = Family.objects.filter(designation__contains='a')
    return render(request, 'inphinity_orm/list_elements.html', {'Family': families_list})

def family_detail(request, fam_id):
    family = get_object_or_404(Family, id=fam_id)
    return render(request, 'inphinity_orm/family_detail.html', {'Family': family})

def family_new(request):
    if request.method == "POST":
        form = FamilyForm(request.POST)
        if form.is_valid():
            family = form.save(commit=False)
            family.save()
            return redirect('family_detail', fam_id=family.id )
    else:
        form = FamilyForm()
    return render(request, 'inphinity_orm/family_edit.html', {'form' : form})
