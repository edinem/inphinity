# Generated by Django 2.1.1 on 2018-09-27 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0008_baltimoreclassification'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonResponsible',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(unique=True)),
            ],
        ),
    ]
