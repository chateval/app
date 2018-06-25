import datetime
import requests
import boto3
from boto3 import session
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Baseline, Author, Model, ModelSubmission, EvaluationDataset, EvaluationDatasetText, ModelResponse
from .forms import UploadModelForm
from chateval.settings import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_STORAGE_BUCKET_LOCATION
from eval.scripts.human_evaluations import upload
def load_responses(response_file, dataset, model):
    response = requests.get(response_file)
    data = response.text
    responses = data.split('\n')

    prompts = EvaluationDatasetText.objects.all().filter(evaluationdataset=dataset)
    
    for i in range(len(responses)):
        model_response = ModelResponse(evaluationdataset=dataset, prompt=prompts[i], model=model, response_text=responses[i])
        model_response.save()

def splash(request):
    datasets = EvaluationDataset.objects.all()
    baselines = Baseline.objects.all()
    return render(request, 'splash.html', {'datasets': datasets, 'baselines': baselines})

def models(request):
    models = Model.objects.all()
    return render(request, 'models.html', {'models': models})

def conversations(request):
    models = Model.objects.all()
    datasets = EvaluationDataset.objects.all()
    if request.method == "POST":
        return render(request, 'conversations.html', {'POST': True, 'models': models, 'datasets': datasets})
    return render(request, 'conversations.html', {'POST': False, 'models': models, 'datasets': datasets})

def submit(request):
    response_files = EvaluationDataset.objects.all()
    if request.method == "POST":
        form = UploadModelForm(request.POST, files=request.FILES)
        if form.is_valid():
            model = Model(author=Author.objects.get(pk=request.user),
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                repo_location = form.cleaned_data['repo_location'],
                cp_location=form.cleaned_data['checkpoint_location'])
            model.save()

            model_submission = ModelSubmission(model=model, date=datetime.datetime.now().date())
            model_submission.save()

            for response_file in response_files:
                if request.FILES.get(response_file.name) is not None:
                    file_path = 'models/' + str(model_submission.id) + '-' + request.FILES.get(response_file.name).name
                    session = boto3.session.Session(aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
                    s3 = session.resource('s3')
                    s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(Key=file_path, Body=request.FILES.get(response_file.name))
                    dataset = EvaluationDataset.objects.get(name=response_file.name)
                    load_responses(AWS_STORAGE_BUCKET_LOCATION + file_path, dataset, model)

            return HttpResponseRedirect('/evaluation/')
    form = UploadModelForm()
    return render(request, 'submit.html', {'form': form, 'response_files': response_files})

def test(request):
    upload()
    return render(request, 'models.html', {})    
