# Generated by Django 3.2.5 on 2021-08-05 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceApiUrlConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('api_url', models.CharField(help_text='Enter An Easily Identifiable Name', max_length=255)),
                ('key_identifier', models.CharField(choices=[('ThirdPartyQoute', 'ThirdPartyQoute'), ('ThirdPartyPayment', 'ThirdPartyPayment'), ('ThirdPartyPolicy', 'ThirdPartyPolicy'), ('ZinaraQuote', 'ZinaraQuote'), ('RadioQuote', 'RadioQuote'), ('LicensingPayment', 'LicensingPayment'), ('LicensingPolicy', 'LicensingPolicy'), ('ThirdPartyZinaraQoute', 'ThirdPartyZinaraQoute'), ('ThirdPartyZinaraPayment', 'ThirdPartyZinaraPayment'), ('ThirdPartyZinaraPolicy', 'ThirdPartyZinaraPolicy'), ('CheckVehicle', 'CheckVehicle')], max_length=255, unique=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
