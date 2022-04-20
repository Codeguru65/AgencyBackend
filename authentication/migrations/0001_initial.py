# Generated by Django 3.2.5 on 2021-08-02 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent_check', models.BooleanField(default=False)),
                ('client_address', models.CharField(blank=True, max_length=500)),
                ('mobile_1', models.CharField(blank=True, max_length=30)),
                ('mobile_2', models.CharField(blank=True, max_length=30)),
                ('email', models.EmailField(max_length=255)),
                ('industry', models.CharField(choices=[('Consulting', 'Consulting'), ('Electronic Payments', 'Electronic Payments'), ('Banking', 'Banking'), ('Funeral Services', 'Funeral Services'), ('Micro Finance', 'Micro Finance'), ('Tertiary', 'Tertiary')], max_length=50)),
                ('street_name', models.CharField(blank=True, max_length=255)),
                ('approved_logo', models.ImageField(upload_to='logos')),
                ('approved_colors', models.CharField(help_text='Upload Hex Colors Only', max_length=30)),
            ],
            options={
                'verbose_name': 'Institutional Agents',
                'verbose_name_plural': 'Institutional Agents',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, max_length=255, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('mobile_number', models.CharField(db_index=True, max_length=255, unique=True)),
                ('id_number', models.CharField(db_index=True, max_length=255, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auth_provider', models.CharField(default='email', max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.institution')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
