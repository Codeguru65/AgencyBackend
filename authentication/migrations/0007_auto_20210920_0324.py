# Generated by Django 3.2.5 on 2021-09-20 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_user_institution'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_reset_new',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='institution',
            name='industry',
            field=models.CharField(choices=[('Consulting', 'Consulting'), ('Electronic Payments', 'Electronic Payments'), ('Banking', 'Banking'), ('Funeral Services', 'Funeral Services'), ('Micro Finance', 'Micro Finance'), ('Tertiary', 'Tertiary'), ('Clothing', 'Clothing')], max_length=255),
        ),
    ]
