# Generated by Django 4.2.1 on 2023-05-25 22:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainpage', '0002_userranking_remove_userpreference_favorite_movies_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userranking',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='userranking',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='userranking',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='RankedMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.movie')),
                ('ranking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainpage.userranking')),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.RemoveField(
            model_name='userranking',
            name='movie',
        ),
        migrations.RemoveField(
            model_name='userranking',
            name='position',
        ),
        migrations.AddField(
            model_name='userranking',
            name='movies',
            field=models.ManyToManyField(through='mainpage.RankedMovie', to='mainpage.movie'),
        ),
    ]