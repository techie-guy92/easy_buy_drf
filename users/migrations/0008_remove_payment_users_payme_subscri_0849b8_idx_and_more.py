# Generated by Django 5.1.4 on 2025-01-12 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_payment_user'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='payment',
            name='users_payme_subscri_0849b8_idx',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='subscription',
        ),
    ]
