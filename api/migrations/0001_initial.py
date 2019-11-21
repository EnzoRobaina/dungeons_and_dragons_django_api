# Generated by Django 2.2.7 on 2019-11-21 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=266, verbose_name='Name')),
                ('strength', models.PositiveIntegerField(verbose_name='Strength')),
                ('dexterity', models.PositiveIntegerField(verbose_name='Dexterity')),
                ('constitution', models.PositiveIntegerField(verbose_name='Constitution')),
                ('intelligence', models.PositiveIntegerField(verbose_name='Intelligence')),
                ('wisdom', models.PositiveIntegerField(verbose_name='Wisdom')),
                ('charisma', models.PositiveIntegerField(verbose_name='Charisma')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Character',
                'verbose_name_plural': 'Characters',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=266, verbose_name='Name')),
                ('ability', models.CharField(max_length=266, verbose_name='Ability')),
                ('proficient', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('character', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Character')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
            },
        ),
    ]