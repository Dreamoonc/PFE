from django.db import models

# Create your models here.
TYPE_ANNONCE=(
    ("Demande","Demande"),
    ("Don","Don")
)
class Annonce (models.Model):
    titre=models.CharField(max_length=150)
    contenu=models.TextField(max_length=400)
    type=models.CharField(choices=TYPE_ANNONCE ,  max_length=10)
    image=models.BinaryField()
    date=models.DateTimeField()

class Notification (models.Model):
    contenu=models.TextField(max_length=400)
    date=models.DateTimeField()

class Commentaire (models.Model):
    contenu=models.TextField(max_length=400)
    date=models.DateTimeField()

class Cagniote (models.Model):
    titre=models.CharField(max_length=150)
    sommeDemander=models.FloatField()
    sommeRecolter=models.FloatField()
    raison=models.TextField(max_length=400)




