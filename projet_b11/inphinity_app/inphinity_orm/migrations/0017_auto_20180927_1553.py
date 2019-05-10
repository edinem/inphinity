# Generated by Django 2.1.1 on 2018-09-27 13:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0016_auto_20180927_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='PFAMMethodScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.TextField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='PPICOGcore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('date_creation', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='PPIPFAMScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('date_creation', models.DateField(default=django.utils.timezone.now)),
                ('pfam_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inphinity_orm.PFAMMethodScore')),
                ('ppi_interaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inphinity_orm.PPI')),
            ],
        ),
        migrations.CreateModel(
            name='ProteinCog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SourceCog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.TextField(unique=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='COGSInterationsPair',
            new_name='COGInterationsPair',
        ),
        migrations.RenameModel(
            old_name='PPIMethodScore',
            new_name='COGSourceInformation',
        ),
        migrations.RenameModel(
            old_name='ProteinsPfams',
            new_name='ProteinPfam',
        ),
        migrations.RemoveField(
            model_name='ppiscore',
            name='ppi_interaction',
        ),
        migrations.RemoveField(
            model_name='ppiscore',
            name='ppi_method',
        ),
        migrations.RenameModel(
            old_name='COGS',
            new_name='COG',
        ),
        migrations.RenameModel(
            old_name='COGSSourceInformation',
            new_name='COGMethodScore',
        ),
        migrations.DeleteModel(
            name='PPIScore',
        ),
        migrations.AddField(
            model_name='proteincog',
            name='cog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inphinity_orm.COG'),
        ),
        migrations.AddField(
            model_name='proteincog',
            name='person_responsible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inphinity_orm.PersonResponsible'),
        ),
        migrations.AddField(
            model_name='proteincog',
            name='protein',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inphinity_orm.Protein'),
        ),
        migrations.AddField(
            model_name='proteincog',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inphinity_orm.SourceCog'),
        ),
        migrations.AddField(
            model_name='ppicogcore',
            name='cog_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inphinity_orm.COGMethodScore'),
        ),
        migrations.AddField(
            model_name='ppicogcore',
            name='ppi_interaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inphinity_orm.PPI'),
        ),
    ]
