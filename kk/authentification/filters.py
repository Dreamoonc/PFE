from django.db.models import fields
from django.forms.widgets import *
import django_filters
from django_filters import *
from .models import *


TYPE_ANNONCE=(
    ('demande','demande'),
    ("don","don")
)
TYPE_ASSOCIATION=(
    ('National','National'),
    ('Locale','Locale')
)
CATEGORY_ASSOCIATION =(
    ("Association d'handicapé", "Association d'handicapé"),
    ('association de grands malades ','association de grands malades '),
    ("de solidarité humanitaire","de solidarité humanitaire"),
    ('association des femmes' , 'association des femmes'),
    ("association d'enfances","association d'enfances"),
    ('association culturelles et sport pour handicapés','association culturelles et sport pour handicapés')
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



class AssociationFilter(django_filters.FilterSet):
    willaya=ChoiceFilter(choices=WILLAYA,label='',empty_label="willaya",widget=Select(attrs={'class':'input'}))
    type=ChoiceFilter(choices=TYPE_ASSOCIATION,label='',empty_label="type",widget=Select(attrs={'class':'input'}))
    category=ChoiceFilter(choices=CATEGORY_ASSOCIATION,label='',empty_label="category",widget=Select(attrs={'class':'input'}))

    class  Meta :
       model = Association
       fields = ['willaya','type','category']

