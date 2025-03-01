# Generated by Django 3.2.9 on 2022-05-31 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='annonce',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='annonce',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='img',
            field=models.ImageField(default='profile.png', upload_to='images/', verbose_name='image'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('annonce', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='authentification.annonce')),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
