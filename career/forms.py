from django import forms
from django.forms import ModelForm,widgets
from .models import ApplyJob

class ApplyjobForm(ModelForm):
    class Meta:
        model = ApplyJob
        exclude = ['get_job']
        widgets = {
            'birth': widgets.DateInput(attrs={'type': 'date'}),
            'offer': widgets.DateInput(attrs={'type': 'date'})
        }
        labels = {
            "birth":"Birth Date",
            "cv":"Upload CV",
            "cover_letter":"Upload Cover Letter",
            "hear":"How did you hear about this job ?",
            "refer":"If referred by Subhakamana Footwears employee, please provide their name. If not please write N/A?",
            "next_role":"What are your looking for in next role?",
            'offer':"When would you be able to begin employment?"
        }
        

