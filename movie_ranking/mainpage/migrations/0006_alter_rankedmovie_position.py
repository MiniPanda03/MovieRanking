# Generated by Django 4.2.1 on 2023-05-26 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0005_alter_rankedmovie_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rankedmovie',
            name='position',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
