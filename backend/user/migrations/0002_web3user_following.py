# Generated by Django 5.1.1 on 2024-09-08 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='web3user',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to='user.web3user'),
        ),
    ]
