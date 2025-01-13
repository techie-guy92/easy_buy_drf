# Generated by Django 5.1.4 on 2025-01-12 13:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_payment_users_payme_subscri_0849b8_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='users.premiumsubscription', verbose_name='Subscription'),
        ),
        migrations.AddIndex(
            model_name='payment',
            index=models.Index(fields=['user'], name='users_payme_user_id_f4ee05_idx'),
        ),
    ]
