from django.db import models


class Pergunta(models.Model):
    enunciado = models.TextField()
    alternativas = models.JSONField()
    disponivel = models.BooleanField(default=False)
    alternativa_correta = models.IntegerField(choices=[
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
        (3, 'D'),
    ])

    def __str__(self):
        return self.enunciado


class Candidato(models.Model):
    nome = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.email


class Resposta(models.Model):
    candidato=models.ForeignKey(Candidato, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    pontos = models.IntegerField()
    respondida_em = models.DateTimeField(auto_now_add=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['candidato', 'pergunta'], name='resposta_unica')
        ]


