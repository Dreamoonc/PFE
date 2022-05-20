from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
TYPE_ANNONCE=(
    ("Demande","Demande"),
    ("Don","Don")
)



WILLAYA=(
(1,	'Adrar'	),
(2,	'Chlef'	),
(3,	'Laghouat'	),
(4	,'Oum-El-Bouaghi'),
(5,	'Batna'	),
(6	,'Béjaïa'	),
(7,	'Biskra'	),
(8,	'Béchar'	),
(9	,'Blida'),
(10,'Bouira'),
(11,	'Tamanrasset'),
(12	,'Tébessa'),
(13,	'Tlemcen'	),
(14	,'Tiaret'	),
(15	,'Tizi-Ouzou'),
(16	,'Alger'	),
(17,'Djelfa'),
(18	,'Jijel'	),
(19	,'Sétif'),
(20,	'Saïda'	),
(21	,'Skikda')	,
(22,	'Sidi Bel' ),
(23	,'Annaba'	),
(24,	'Guelma')	,
(25,	'Constantine'	),
(26,	'Médéa'	),
(27,	'Mostaganem'	),
(28,	'M’sila')	,
(29,	'Mascara'	),
(30,	'Ouargla'	),
(31,	'Oran')	,
(32,	'El Bayadh')	,
(33,	'Illizi'	),
(34,	'Bordj' ),
(35,	'Boumerdès'	),
(36,	'El-Tarf	'),
(37,	'Tindouf')	,
(38,	'Tissemsilt'	),
(39,	'El-Oued	'),
(40,	'Khenchela'	),
(41,	'Souk-Ahras'),
(42,	'Tipaza	'),
(43,	'Mila'	),
(44,	'Aïn-Defla	'),
(45,	'Naâma'	),
(46,	'Aïn-Témouchent'	),
(47,	'Ghardaïa'	),
(48,	'Relizane')	,
(49,	'El M-Ghair	'),
(50,	'El Meniaa	'),
(51,	'Ouled Djellal'	),
(52,	'Bordj Badji '),
(53	,'Béni Abbès'	),
(54	,'Timimoun'),
(55,	'Touggourt'	),
(56,	'Djanet'),
(57,	"In Salah"	),
(58	,"In Guezzam"	)
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




  
class PhysicalUser (models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE, primary_key=True,)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    

class Association (models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=255)
    file = models.CharField (max_length=200)


