from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.utils import timezone
# Create your models here.

TYPE_ANNONCE=(
    ('demande','demande'),
    ("don","don")
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
    img = models.BinaryField(verbose_name="image")

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



  
class PhysicalUser (models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE, primary_key=True,)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    willaya=models.CharField(choices=WILLAYA ,  max_length=10)
    

class Association (models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE, primary_key=True,)
    name = models.CharField(max_length=255)
    file = models.CharField (max_length=200)
    willaya=models.CharField(choices=WILLAYA ,  max_length=10)

class Annonce (models.Model):
    contenu=models.TextField(max_length=600)
    date=models.DateTimeField(default=timezone.now)
    image = models.ImageField(null=True , blank=True, upload_to='images/')
    type=models.CharField(choices=TYPE_ANNONCE,max_length=10,default='demande')
    auteur= models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.auteur +" "+self.date


class Cagniote (models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField(max_length=600)
    sommeDemander= models.FloatField()
    sommeRecolter = models.FloatField(default=0)
    dateCreation = models.DateField(auto_now=True)
    user = models.ForeignKey(Association , on_delete=models.CASCADE)
    arret=models.BooleanField(default=False)
    

    def __str__(self):
        return self.titre
