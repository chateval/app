# Generated by Django 2.0.7 on 2018-09-03 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0003_auto_20180903_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluationdataset',
            name='baselines',
            field=models.ManyToManyField(blank=True, to='orm.Model'),
        ),
    ]
