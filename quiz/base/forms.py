from django.forms import ModelForm

from quiz.base.models import Candidato


class CandidatoForm(ModelForm):
    class Meta:
        model = Candidato
        fields = ['nome', 'email']