# Generated by Django 5.1.4 on 2024-12-29 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_alter_customermodel_phone_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder_name', models.CharField(max_length=150)),
                ('bank_acc_no', models.CharField(max_length=150)),
                ('bank_branch', models.CharField(max_length=250)),
                ('ifsc_code', models.CharField(max_length=150)),
                ('gst_in', models.CharField(max_length=150)),
                ('upi_id', models.CharField(max_length=150)),
                ('address_line1', models.CharField(max_length=150)),
                ('address_line2', models.CharField(max_length=150)),
                ('address_line3', models.CharField(max_length=150)),
                ('contacts', models.CharField(max_length=150)),
            ],
        ),
    ]
