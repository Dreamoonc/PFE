
import json
from pyexpat import model
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.utils import timezone
from channels.layers import  get_channel_layer
from asgiref.sync import async_to_sync

# Create your models here.

TYPE_ANNONCE=(
    ('demande','demande'),
    ("don","don")
)
TYPE_BENEVOLE =(
("SOLIDARITÉ ET INSERTION","SOLIDARITÉ ET INSERTION"),
("ÉDUCATION POUR TOUS","ÉDUCATION POUR TOUS"),
("PRÉVENTION ET PROTECTION","PRÉVENTION ET PROTECTION"),
("ART ET CULTURE POUR TOUS","ART ET CULTURE POUR TOUS"),
("PROTECTION DE LA NATURE","PROTECTION DE LA NATURE"),
("SPORT POUR TOUS","SPORT POUR TOUS"),
("SANTE POUR TOUS","SANTE POUR TOUS")

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
CATEGORY_ANNONCE =(
    ("Alimentaire", "Alimentaire"),
    ('Medical','Medical'),
    ("Vestimentaire","Vestimentaire"),
    ('Educatif' , 'Educatif'),
    ("Financière","Financière"),
    ("Autre","Autre")
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

class UserManager(BaseUserManager):
    def create_user(self , email ,username ,   phone , password=None):
        if not email : 
            raise ValueError ("email is not require")
        if not username: 
            raise ValueError ("username is not require")
        if not phone : 
            raise ValueError ("phone is not require")
        
        user=self.model(
            email=self.normalize_email(email),
            phone = phone ,
            username=username,
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
        

    def create_superuser(self,email,username ,phone  , password=None ):
        user=self.create_user(email =self.normalize_email(email) ,username=username,phone=phone , password=password)
        user.is_admin=True 
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user 
        

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name = "email adress",max_length=60,unique=True )
    username = models.CharField(verbose_name = "username",max_length=60,unique=True)
    phone = models.CharField(max_length=10 , verbose_name="phone number ")
    img = models.ImageField(verbose_name="image", upload_to='images/' ,default='profile.png')
    signial = models.IntegerField(default=0)

    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    is_association = models.BooleanField(default=False)
    is_person = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=['username','phone']

    objects = UserManager()


    def __str__(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return True 
    
    def has_module_perms(self , app_label ):
        return True

class localisation (models.Model):
    id= models.IntegerField(primary_key=True)
    commune_name= models.CharField(max_length=255)
    daira_name=models.CharField(max_length=255)
    wilaya_name=models.CharField(max_length=255)


  
class PhysicalUser (models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE, primary_key=True,)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    willaya=models.CharField(choices=WILLAYA ,  max_length=10)
    adresse = models.ForeignKey(localisation , on_delete=models.CASCADE, default = 1)
    
    

class Association (models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE, primary_key=True,)
    file = models.ImageField(verbose_name="image", upload_to='images/')
    type = models.CharField(choices=TYPE_ASSOCIATION ,  max_length=10)
    category = models.CharField(choices=CATEGORY_ASSOCIATION ,  max_length=50)
    adresse = models.ForeignKey(localisation , on_delete=models.CASCADE, default = 1)
    local=models.CharField(max_length=200,null=True ,blank=True )
    description=models.TextField(max_length=800 , null=True ,blank=True)
    is_valid = models.BooleanField(default=False)

class Annonce (models.Model):
    contenu=models.TextField(max_length=600)
    date=models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True , blank=True, upload_to='images/')
    type=models.CharField(choices=TYPE_ANNONCE,max_length=10,default='demande')
    auteur= models.ForeignKey(User,on_delete=models.CASCADE)
    signial = models.IntegerField(default=0)
    category=models.TextField(choices=CATEGORY_ANNONCE , max_length=50, default="Autre")
    def __str__(self):
        return str(self.id)
    class Meta:
        ordering = ['-date']

class Comment(models.Model):
    annonce=models.ForeignKey(Annonce, related_name="comments",on_delete=models.CASCADE)
    contenu=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)
    auteur=models.ForeignKey(User,on_delete=models.CASCADE)
    
class Cagniote (models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField(max_length=600)
    sommeDemander= models.FloatField()
    sommeRecolter = models.FloatField(default=0)
    dateCreation = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Association , on_delete=models.CASCADE)
    arret=models.BooleanField(default=False)    
    def __str__(self):
        return self.titre


    
class Benevole (models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField(max_length=600)
    nbr_max = models.IntegerField()
    nbr_actuel = models.IntegerField(default=0)
    date =models.DateField()
    type = models.CharField(choices=TYPE_BENEVOLE  ,  max_length=60)
    arret=models.BooleanField(default=False) 
    association = models.ForeignKey(Association ,on_delete=models.CASCADE)
    adresse = models.ForeignKey(localisation , on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class Notification(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    notification=models.TextField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)        
    is_seen=models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']

    def save(self, *args,**kwars):
        print('save called')
        channel_layer = get_channel_layer()
        notification_objs = Notification.objects.filter(is_seen=False).count()
        data = {'count' : notification_objs , 'current_notification' : self.notification }

        print(data)
        async_to_sync(channel_layer.group_send)(
            'test_consumer_group' , {
                'type' : 'send_notification',
                'value' : json.dumps(data)
            }
            
        )
        super(Notification, self).save(*args,**kwars)
    