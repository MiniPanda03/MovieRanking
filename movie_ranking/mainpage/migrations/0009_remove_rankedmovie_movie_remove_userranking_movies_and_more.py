# Generated by Django 4.2.1 on 2023-05-26 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainpage', '0008_alter_movie_table_alter_rankedmovie_table_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rankedmovie',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='userranking',
            name='movies',
        ),
        migrations.AddField(
            model_name='rankedmovie',
            name='movie_id',
            field=models.IntegerField(default=0),
        ),
    ]
