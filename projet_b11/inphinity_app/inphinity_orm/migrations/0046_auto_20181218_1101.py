# Generated by Django 2.1.1 on 2018-12-18 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0045_auto_20181122_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='proteinpfam',
            name='e_value',
            field=models.FloatField(default=-1.0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='protein',
            name='gene',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='protein_gene', to='inphinity_orm.Gene'),
        ),
    ]
