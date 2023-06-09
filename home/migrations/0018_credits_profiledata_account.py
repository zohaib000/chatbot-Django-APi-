# Generated by Django 4.1.7 on 2023-05-20 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_savedprompts_pid'),
    ]

    operations = [
        migrations.CreateModel(
            name='credits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available', models.IntegerField()),
                ('user', models.CharField(max_length=400)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='profiledata',
            name='account',
            field=models.CharField(default='Free', max_length=400),
            preserve_default=False,
        ),
    ]
