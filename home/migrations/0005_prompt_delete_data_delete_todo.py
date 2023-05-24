# Generated by Django 4.1.7 on 2023-04-24 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=500)),
                ('Description', models.TextField()),
                ('prompt_text', models.TextField()),
                ('Time', models.TimeField(auto_now_add=True)),
                ('Date', models.DateField(auto_now_add=True)),
                ('User', models.CharField(max_length=500)),
            ],
        ),
        migrations.DeleteModel(
            name='Data',
        ),
        migrations.DeleteModel(
            name='Todo',
        ),
    ]