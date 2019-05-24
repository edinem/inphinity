# Generated by Django 2.1.1 on 2018-10-16 09:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0029_auto_20181015_1320'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainInteractionScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('date_creation', models.DateField(default=django.utils.timezone.now)),
                ('domain_interaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inphinity_orm.DomainInterationsPair')),
            ],
        ),
        migrations.CreateModel(
            name='DomainMethodScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.TextField(unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='domaininteractionsource',
            unique_together={('domain_interaction', 'information_source')},
        ),
        migrations.AlterUniqueTogether(
            name='ppipfamscore',
            unique_together={('ppi_interaction', 'pfam_method')},
        ),
        migrations.AddField(
            model_name='domaininteractionscore',
            name='score_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='inphinity_orm.DomainMethodScore'),
        ),
    ]