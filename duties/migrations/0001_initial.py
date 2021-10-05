# Generated by Django 3.2.7 on 2021-10-05 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_alter_user_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('nurse', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='accounts.user')),
                ('off_choices', models.JSONField()),
                ('duties', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]