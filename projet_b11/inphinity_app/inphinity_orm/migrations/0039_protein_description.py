# Generated by Django 2.1.1 on 2018-10-29 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0038_auto_20181026_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='protein',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
