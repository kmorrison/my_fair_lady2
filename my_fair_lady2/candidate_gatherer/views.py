import csv
from collections import namedtuple

from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render

from candidate_gatherer import models

class CandidateForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    first_name.widget = forms.TextInput(attrs={'placeholder': "First Name"})

    last_name = forms.CharField(max_length=200)
    last_name.widget = forms.TextInput(attrs={'placeholder': "Last Name"})

    email_address = forms.EmailField()
    email_address.widget = forms.TextInput(attrs={'placeholder': "Email"})

    phone_number = forms.CharField(max_length=200, required=False)
    phone_number.widget = forms.TextInput(attrs={'placeholder': "Phone (optional)"})


class SourceForm(forms.Form):
    name = forms.CharField(max_length=200)
    name.widget = forms.TextInput(attrs={'placeholder': "Source Name"})


@login_required
def landing_page(request):
    return render(
        request,
        'landing.html',
        dict(
            source_form=SourceForm(),
            recent_sources=models.recent_sources(),
        ),
    )

def upsert_source(source_type_id, source_name):
    # TODO: Move this logic out of the view.
    existing_sources = models.Source.objects.filter(
        source_type_id=source_type_id,
        name=source_name,
    ).order_by(
        '-time_created',
    ).all()
    if existing_sources:
        return existing_sources[0]

    source = models.Source(
        name=source_name,
        source_type_id=source_type_id,
    )
    source.save()
    return source.id


@login_required
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

    source = upsert_source(source_type_id, name)

    return redirect(
        '/candidate_gatherer/%s' % (source.id,),
    )


# Create your views here.
@login_required
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


# TODO: Move this logic out of views.
def upsert_candidate(new_params):
    existing_candidates = models.Candidate.objects.filter(
        **new_params
    ).order_by(
        '-time_created',
    ).all()
    if existing_candidates:
        return existing_candidates[0]
    candidate = models.Candidate(**new_params)
    candidate.save()
    return candidate


@login_required
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
    candidate = upsert_candidate(new_params)

    return redirect(
        '/candidate_gatherer/%s?success_candidate_id=%s' % (source_id, candidate.id),
    )

SourcePresenter = namedtuple('SourcePresenter', [
    'id',
    'name',
    'time_created',
    'candidate_count',
])

def build_source_presenters(sources):
    # TODO: Broken record; move this logic out of views.
    return [
        SourcePresenter(
            id=source.id,
            name=source.name,
            time_created=source.time_created,
            candidate_count=models.Candidate.objects.filter(source_id=source.id).count(),
        )
        for source in sources
    ]
        

@login_required
def downloads(request):
    return render(
        request,
        'downloads.html',
        dict(
            recent_sources=models.recent_sources(),
            sources=build_source_presenters(
                models.Source.objects.order_by("-time_created").all()
            ),
        ),
    )

@login_required
def download(request, source_id):
    source = models.Source.objects.get(id=source_id)
    source_type = models.SourceType.objects.get(id=source.source_type_id)
    candidates = models.Candidate.objects.filter(
        source_id=source.id
    ).order_by("time_created").all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s%s.csv"' % (source.name, source.time_created.date().isoformat())

    field_names = [
        'First Name', 
        'Last Name', 
        'Company',
        'Job Title',
        'Tags',
        'Notes',
        'Source Type',
        'Source Name', 
        'Email', 
        'Email 2', 
        'Email 3', 
        'Home Phone', 
        'Cell Phone', 
        'Work Phone', 
        'Address 1',
        'Address 2',
        'City',
        'State/Province',
        'Zip/Postal',
        'Country',
        'URL1',
        'Facebook',
        'LinkedIn',
        'Twitter',
        'Contact Status',
        'Assigned To',
        'Email Campaign',
        'Email Status',
    ]
    writer = csv.DictWriter(response, field_names)
    writer.writeheader()
    for candidate in candidates:
        row = dict((key, '') for key in field_names)
        row.update(
            {
                "First Name": candidate.first_name,
                "Last Name": candidate.last_name,
                "Email": candidate.email_address.lower(),
                "Cell Phone": candidate.phone_number,
                "Source Name": source.name,
                "Source Type": source_type.name,
            }
        )
        writer.writerow(row)
    return response
