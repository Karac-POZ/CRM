# Generated by Django 3.1.4 on 2023-03-23 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agent',
            options={'verbose_name': 'Агенты', 'verbose_name_plural': 'Агенты'},
        ),
        migrations.AlterModelOptions(
            name='lead',
            options={'verbose_name': 'Лиды', 'verbose_name_plural': 'Лиды'},
        ),
        migrations.AlterField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='age',
            field=models.IntegerField(default=0, verbose_name='Возраст'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='agent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.agent', verbose_name='Агент'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='first_name',
            field=models.CharField(max_length=20, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='lead',
            name='last_name',
            field=models.CharField(max_length=25, verbose_name='Фамилия'),
        ),
        migrations.CreateModel(
            name='UserPortfolio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Портфолио пользователя',
                'verbose_name_plural': 'Портфолио пользователя',
            },
        ),
        migrations.AddField(
            model_name='agent',
            name='company',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to='leads.userportfolio'),
            preserve_default=False,
        ),
    ]