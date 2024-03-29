from django import forms

from .models import AcaoIntencao, Texto, Historia, PartesHistoria

class HistoriaForm(forms.ModelForm):

    class Meta:
        model = Historia
        fields = ('nome',)
        labels = {
            "nome": "Nome:",
        }   
        widgets = {
            "nome": forms.TextInput(
                attrs={"class": "form-control",},
            ),
        }

class PartesHistoriaForm(forms.ModelForm):

    class Meta:
        model = PartesHistoria
        fields = ('historia', 'ordem', 'componente',)
        labels = {
            "historia": "",
            "ordem": "",
            "componente":"",
        }   
        widgets = {
            "historia": forms.Select(
                attrs={"class": "selectpicker form-control", "style": "display:none"}
            ),
            "ordem": forms.NumberInput(
                attrs={"class": "form-control", "style": "display:none"}
            ),
            "componente": forms.Select(
                attrs={"class": "selectpicker form-control",},
            ),
        }

class AcaoIntencaoForm(forms.ModelForm):

    class Meta:
        model = AcaoIntencao
        fields = ('nome', 'tipo',)
        labels = {
            "nome": "Nome:",
            "tipo": "",
        }   
        widgets = {
            "nome": forms.TextInput(
                attrs={"class": "form-control",},
            ),
            "tipo": forms.Select(
                attrs={"class": "selectpicker form-control", "style":"display:none"}
            ),
        }

class TextoForm(forms.ModelForm):

    class Meta:
        model = Texto
        fields = ('id_acao_intencao', 'texto',)
        labels = {
            "id_acao_intencao": "",
            "texto": "Exemplo",
        }   
        widgets = {
            "id_acao_intencao": forms.Select(
                attrs={"class": "selectpicker form-control", "style": "display:none"}
            ),
            "texto": forms.TextInput(
                attrs={"class": "form-control",},
            ),
        }