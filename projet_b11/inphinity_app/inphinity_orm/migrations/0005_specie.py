# Generated by Django 2.1.1 on 2018-09-26 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0004_genus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.TextField(unique=True)),
                ('genus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inphinity_orm.Family')),
            ],
        ),
    ]