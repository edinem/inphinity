# Generated by Django 2.1.1 on 2018-10-15 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0026_auto_20181012_1621'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='family',
            options={'ordering': ('designation',)},
        ),
    ]