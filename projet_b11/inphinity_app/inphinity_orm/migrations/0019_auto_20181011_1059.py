# Generated by Django 2.1.1 on 2018-10-11 08:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0018_auto_20181008_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genus',
            name='designation',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='genus',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genuses', to='inphinity_orm.Family'),
        ),
        migrations.AlterField(
            model_name='specie',
            name='designation',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='specie',
            name='genus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='species', to='inphinity_orm.Genus'),
        ),
        migrations.AlterUniqueTogether(
            name='genus',
            unique_together={('family', 'designation')},
        ),
        migrations.AlterUniqueTogether(
            name='specie',
            unique_together={('genus', 'designation')},
        ),
    ]
