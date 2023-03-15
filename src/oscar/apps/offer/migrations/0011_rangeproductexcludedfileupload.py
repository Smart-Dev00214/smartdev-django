# Generated by Django 3.2.18 on 2023-03-14 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offer', '0010_conditionaloffer_combinations'),
    ]

    operations = [
        migrations.CreateModel(
            name='RangeProductExcludedFileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filepath', models.CharField(max_length=255, verbose_name='File Path')),
                ('size', models.PositiveIntegerField(verbose_name='Size')),
                ('date_uploaded', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date Uploaded')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Failed', 'Failed'), ('Processed', 'Processed')], default='Pending', max_length=32, verbose_name='Status')),
                ('error_message', models.CharField(blank=True, max_length=255, verbose_name='Error Message')),
                ('date_processed', models.DateTimeField(null=True, verbose_name='Date Processed')),
                ('num_new_skus', models.PositiveIntegerField(null=True, verbose_name='Number of New SKUs')),
                ('num_unknown_skus', models.PositiveIntegerField(null=True, verbose_name='Number of Unknown SKUs')),
                ('num_duplicate_skus', models.PositiveIntegerField(null=True, verbose_name='Number of Duplicate SKUs')),
                ('range', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_uploads_excluded', to='offer.range', verbose_name='Range')),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Uploaded By')),
            ],
            options={
                'verbose_name': 'Range Product Uploaded File',
                'verbose_name_plural': 'Range Product Uploaded Files',
                'ordering': ('-date_uploaded',),
                'abstract': False,
            },
        ),
    ]
