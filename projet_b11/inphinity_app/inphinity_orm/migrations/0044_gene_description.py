# Generated by Django 2.1.1 on 2018-11-21 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0043_auto_20181112_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='description',
            field=models.TextField(null=True),
        ),
    ]