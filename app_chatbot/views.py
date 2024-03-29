from django.shortcuts import render, redirect
from django.urls import reverse
from django.forms.models import modelformset_factory


from . import forms, models

def index(request):
    N = 2

    acoes = models.AcaoIntencao.objects.filter(tipo = "Ação")
    intencoes = models.AcaoIntencao.objects.filter(tipo = "Intenção")
    historias = models.Historia.objects.all()

    context = {
        'acoes': acoes[:N],
        'intencoes': intencoes[:N],
        'historias': historias[:N],
    }

    return render(request, "app_chatbot/index.html", context)

def listar_historia(request):
    textos = models.Texto.objects.all()
    return render(request, 'app_chatbot/historia.html', {'textos': textos})

def criar_historia(request):
    N = 15
    N_EXTRA = 10
    
    PartesFormset = modelformset_factory(
        models.PartesHistoria, form=forms.PartesHistoriaForm, extra=N_EXTRA, min_num=1,
    )
    queryset = models.Historia.objects.none()
    
    def primeiros(objeto):
        ids = set()
        for x in objeto:
            id_ai = x.id_acao_intencao.pk
            if id_ai not in ids:
                ids.add(id_ai)
            else:
                objeto = objeto.exclude(pk = x.pk)    
        return objeto

    acoes = primeiros(
        models.Texto.objects.filter(id_acao_intencao__tipo__contains = "Ação")
    )

    intencoes = primeiros(
        models.Texto.objects.filter(id_acao_intencao__tipo__contains = "Intenção")
    )
    
    form = forms.HistoriaForm(request.POST or None)
    formset = PartesFormset(request.POST or None, queryset=queryset)
    
    context = {
        'acoes': acoes[:N],
        'intencoes': intencoes[:N],
        'form': form,
        'formset': formset,
    }
    
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        id_hist = instance.pk
        ordem = 1
        instancias = formset.save(commit=False)
        for insta in instancias:
            insta.ordem = ordem
            insta.historia_id = id_hist
            insta.save()
            ordem += 1
        return redirect(reverse("index"))

    return render(request, 'app_chatbot/criar_historia.html', context)

def editar_historia(request, id):
    return render(request, 'app_chatbot/index.html', {'id': id})

def criar_acao_intencao(request, tipo):
    N_EXTRA = 10
    TextoFormset = modelformset_factory(
        models.Texto, form=forms.TextoForm, extra=N_EXTRA, min_num=1,
    )
    if tipo == "acao":
        tipo_txt = "Ação"
    else:
        tipo_txt = "Intenção"

    queryset = models.Texto.objects.none()
    formset = TextoFormset(request.POST or None, queryset=queryset)
    form = forms.AcaoIntencaoForm(request.POST or None)

    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        saved_id = instance.pk
        instances = formset.save(commit=False)
        for insta in instances:
            insta.id_acao_intencao_id = saved_id
            insta.save()
        return redirect(reverse("index"))
    context = {
        "form": form,
        "formset": formset,
        "tipo": tipo_txt,
    }
    return render(request, 'app_chatbot/criar_acao_intencao.html', context)

def editar_acao_intencao(request, tipo, id):
    return render(request, 'app_chatbot/index.html', {'tipo': tipo, 'id': id})

    
# 2. Criar view em que há uma lista de todas as intenções
# deve listar os X primeiros (uma uma amostra de tamanho X) exemplos
def listar_acoesintencoes(request, tipo):
    # ta errado mas a logica é essa
    if tipo == "acao":
        tipo_txt = "Ação"
    else:
        tipo_txt = "Intenção"

    acao_intencao = models.AcaoIntencao.objects.all().filter(tipo = tipo_txt)
    textos = models.Texto.objects.all()
    
    context = {
        "pais": acao_intencao,
        "textos": textos,
    }
    return render(request, 'app_chatbot/listar_acoesintencoes.html', context)

def escrever_intencoes(caminho):
    intencoes = models.AcaoIntencao.objects.filter(tipo = "Intenção")

    intents = ""
    for i in intencoes:
        intents += f"## intent:{i}\n"
        textos_intentencoes = models.Texto.objects.filter(id_acao_intencao = i.pk)
        for t in textos_intentencoes:
            intents += f"- {t}\n"
        intents += "\n"

    with open(caminho, "w") as file:
        file.write(intents) 

def escrever_domain(caminho):
    def juntar(vetor, f_ish_string):
        string = ""
        for elem in vetor:
            string += f_ish_string.format(elem = elem)
        return string + "\n"
    
    domain = "intents:\n"
    intencoes = models.AcaoIntencao.objects.filter(tipo = "Intenção")
    domain += juntar(intencoes, "  - {elem}\n")

    domain += "actions:\n"
    acoes = models.AcaoIntencao.objects.filter(tipo = "Ação")
    domain += juntar(acoes, "  - {elem}\n")
    
    domain += "templates:\n"
    for a in acoes:
        domain += f"  {a}:\n"
        textos_acoes = models.Texto.objects.filter(id_acao_intencao = a.pk)
        for t in textos_acoes:
            domain += f"    - text : |\n       {t}\n\n"

    with open(caminho, "w") as file:
        file.write(domain) 

def escrever_historias(caminho):
    historias = models.Historia.objects.all()
    stories = ""
    for h in historias:
        stories += f"## {h}\n"
        partes = models.PartesHistoria.objects.filter(historia = h.pk)
        for p in partes:
            if p.componente.tipo == "Intenção":
                stories += f"* {p.componente}\n"
            else :
                stories += f"    - {p.componente}\n"
        stories += "\n"

    with open(caminho, "w") as file:
        file.write(stories) 

def escrever_md(request):
    escrever_intencoes("intents.md")
    escrever_domain("domain.yml")
    escrever_historias("stories.md")

    return render(request, "app_chatbot/escrever_md.html", None)



