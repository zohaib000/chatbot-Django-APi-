# Generated by Django 4.1.7 on 2023-05-16 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_prompt_user_img_savedprompts_user_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedprompts',
            name='category',
            field=models.CharField(default='web design', max_length=500),
            preserve_default=False,
        ),
    ]