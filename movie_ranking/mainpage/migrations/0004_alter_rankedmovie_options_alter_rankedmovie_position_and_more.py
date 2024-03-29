# Generated by Django 4.2.1 on 2023-05-25 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0003_alter_userranking_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rankedmovie',
            options={},
        ),
        migrations.AlterField(
            model_name='rankedmovie',
            name='position',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='rankedmovie',
            unique_together={('ranking', 'movie')},
        ),
    ]
