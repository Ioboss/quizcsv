from django.db.models import Sum
from django.shortcuts import render, redirect

from quiz.base.forms import CandidatoForm
from quiz.base.models import Pergunta, Candidato, Resposta


def home(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            candidato = Candidato.objects.get(email=email)
            return redirect('/podio/')
        except Candidato.DoesNotExist:
            formulario = CandidatoForm(request.POST)
            if formulario.is_valid():
                candidato = formulario.save()
                request.session['candidato_id'] = candidato.id
                return redirect('/perguntas/1')
            else:
                contexto = {'formulario': formulario}
                return render(request, 'base/home.html', contexto)

    return render(request, 'base/home.html')


PONTUACAO_MAXIMA = 100
erradas = 0


def perguntas(request, indice):
    global erradas
    try:
        candidato_id = request.session['candidato_id']
    except KeyError:
        return redirect('/')
    else:
        try:
            pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
        except IndexError:
            erradas = 0
            return redirect('/podio')
        else:
            contexto = {'indice_da_questao': indice, 'pergunta': pergunta}
            if request.method == 'POST':
                resposta_indice = int(request.POST['resposta_indice'])
                if resposta_indice == pergunta.alternativa_correta:
                    pontos = max(PONTUACAO_MAXIMA - erradas, 10)
                    Resposta(candidato_id=candidato_id, pergunta=pergunta, pontos=pontos).save()
                    erradas = 0
                    return redirect(f'/perguntas/{indice + 1}')
                else:
                    erradas += 25
                    contexto['resposta_indice'] = resposta_indice

            return render(request, 'base/game.html', context=contexto)



def podio(request):
    try:
        candidato_id = request.session['candidato_id']
    except KeyError:
        return redirect('/')
    else:
        pontos_dct = Resposta.objects.filter(candidato_id=candidato_id).aggregate(Sum('pontos'))
        pontuacao_do_candidato = pontos_dct['pontos__sum']

        numero_de_candidatos_com_maior_pontuacao = Resposta.objects.values('candidato').annotate(Sum('pontos')).filter(
            pontos__sum__gt=pontuacao_do_candidato).count()
        primeiros_candidato_do_podio = list(
            Resposta.objects.values('candidato', 'candidato__nome').annotate(Sum('pontos')).order_by('-pontos__sum')[:5]
        )
        contexto = {
            'pontuacao_do_candidato': pontuacao_do_candidato,
            'posicao_do_candidato': numero_de_candidatos_com_maior_pontuacao + 1,
            'primeiros_candidato_do_podio': primeiros_candidato_do_podio
        }
        return render(request, 'base/podio.html', contexto)
