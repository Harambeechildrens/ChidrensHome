# Generated by Django 5.1.7 on 2025-03-15 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_child_child_id_alter_staff_staff_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donor',
            fields=[
                ('donor_id', models.AutoField(primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=255)),
                ('contact_info', models.CharField(max_length=255)),
                ('donation_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('donation_date', models.DateField()),
                ('donation_type', models.CharField(choices=[('Cash', 'Cash'), ('Goods', 'Goods'), ('Sponsorship', 'Sponsorship')], max_length=100)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
