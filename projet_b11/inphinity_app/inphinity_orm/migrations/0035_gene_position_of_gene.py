# Generated by Django 2.1.1 on 2018-10-26 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0034_auto_20181016_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='position_of_gene',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
