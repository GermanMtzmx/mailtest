# Generated by Django 2.0 on 2017-12-15 06:29

import accounts.utils
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SignUpCode',
            fields=[
                ('id', models.CharField(editable=False, max_length=22, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('code', models.CharField(default=accounts.utils.generate_code, editable=False, max_length=4)),
                ('expired', models.DateTimeField(default=accounts.utils.generate_code_expired, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'sign up code',
                'verbose_name_plural': 'sign up codes',
                'db_table': 'accounts_sign_up_code',
                'ordering': ('email',),
            },
        ),
        migrations.CreateModel(
            name='SocialToken',
            fields=[
                ('id', models.CharField(editable=False, max_length=22, primary_key=True, serialize=False)),
                ('social', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter')], max_length=10)),
                ('token', models.CharField(max_length=120, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'social token',
                'verbose_name_plural': 'social tokens',
                'db_table': 'accounts_social_token',
                'ordering': ('token',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.CharField(editable=False, max_length=22, primary_key=True, serialize=False)),
                ('firstName', models.CharField(max_length=150)),
                ('lastName', models.CharField(max_length=150)),
                ('username', models.CharField(max_length=200, unique=True, validators=[django.core.validators.RegexValidator('^[a-z0-9\\.]{4,40}$')])),
                ('password', models.CharField(max_length=106)),
                ('email', models.EmailField(max_length=254)),
                ('birthday', models.DateField()),
                ('phone', models.CharField(max_length=15)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='files/avatars/d%Y%m%d/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg'])])),
                ('renewed', models.BigIntegerField(blank=True, default=accounts.utils.generate_user_renewed, null=True)),
                ('isActive', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'ordering': ('username',),
            },
        ),
        migrations.AddField(
            model_name='socialtoken',
            name='user',
            field=models.OneToOneField(db_column='user', on_delete=django.db.models.deletion.CASCADE, to='accounts.User'),
        ),
    ]
