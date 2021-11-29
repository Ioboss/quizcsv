from django.contrib import admin

from quiz.base.models import Pergunta, Candidato, Resposta


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'enunciado', 'disponivel', 'alternativa_correta')


@admin.register(Candidato)
class CandidatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'criado_em')


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('respondida_em', 'candidato', 'pergunta', 'pontos')

