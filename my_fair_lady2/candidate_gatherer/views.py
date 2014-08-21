from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.forms import ModelForm

from candidate_gatherer import models

class CandidateForm(ModelForm):
    class Meta:
        model = models.Candidate
        fields = [
            'first_name',
            'last_name',
            'email_address',
            'phone_number',
        ]

class SourceForm(ModelForm):
    class Meta:
        model = models.Source
        fields = [
            'name',
        ]


def landing_page(request):
    return render(
        request,
        'landing.html',
        dict(
            source_form=SourceForm(),
            recent_sources=models.recent_sources(),
        ),
    )

def source_post(request):
    form = SourceForm(request.POST)
    if not form.is_valid():
        return render(
            request,
            'landing.html',
            dict(
                source_form=form,
                recent_source=models.recent_sources(),
            ),
        )
    name = form.cleaned_data['name']
    source_type_id = models.SourceType.objects.get(
        is_active=True
    ).id

    #TODO: Check if something with this name and source_type already exists
    source = models.Source(
        name=name,
        source_type_id=source_type_id,
    )
    source.save()

    return redirect(
        '/candidate_gatherer/%s' % (source.id,),
    )


# Create your views here.
def candidate_form(request, source_id):
    source = models.Source.objects.get(id=source_id)
    context = dict(
        source_name=source.name,
        source_id=source_id,
        candidate_form=CandidateForm(),
    )
    success_candidate_id = request.GET.get('success_candidate_id', None)
    if  success_candidate_id is not None:
        candidate = models.Candidate.objects.get(id=int(success_candidate_id))
        context['success_candidate_name'] = candidate.full_name
    return render(
        request,
        'candidate.html',
        context,
    )


def candidate_post(request):
    form = CandidateForm(request.POST)
    source_id = request.POST['source_id']
    source = models.Source.objects.get(id=source_id)
    if not form.is_valid():
        return render(
            request,
            'candidate.html',
            dict(
                source_id=source_id,
                source_name=source.name,
                candidate_form=form,
            ),
        )

    new_params = dict(
        first_name=form.cleaned_data['first_name'],
        last_name=form.cleaned_data['last_name'],
        email_address=form.cleaned_data['email_address'],
        source_id=source_id,
    )
    if form.cleaned_data['phone_number']:
        new_params['phone_number'] = form.cleaned_data['phone_number']
    candidate = models.Candidate(**new_params)
    candidate.save()

    return redirect(
        '/candidate_gatherer/%s?success_candidate_id=%s' % (source_id, candidate.id),
    )
