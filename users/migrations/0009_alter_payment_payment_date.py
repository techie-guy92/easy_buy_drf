# Generated by Django 5.1.4 on 2025-01-12 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_payment_users_payme_subscri_0849b8_idx_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Payment Date'),
        ),
    ]
