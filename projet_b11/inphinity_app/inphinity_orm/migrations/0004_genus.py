# Generated by Django 2.1.1 on 2018-09-26 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inphinity_orm', '0003_auto_20180926_1138'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.TextField(unique=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inphinity_orm.Family')),
            ],
        ),
    ]