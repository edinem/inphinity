# Generated by Django 2.1.1 on 2018-10-08 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0017_auto_20180927_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cogsinteractionsource',
            name='information_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inphinity_orm.COGSourceInformation'),
        ),
    ]
