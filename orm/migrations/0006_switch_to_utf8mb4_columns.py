# Generated by Django 2.0.7 on 2018-11-07 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orm', '0005_auto_20180926_1931'),
    ]

    operations = [
        migrations.RunSQL(
            sql=['ALTER TABLE ModelResponse MODIFY response_text LONGTEXT CHARSET utf8mb4 COLLATE utf8mb4_unicode_ci'],
            reverse_sql=['ALTER TABLE ModelResponse MODIFY response_text LONGTEXT']  
        )
    ]
