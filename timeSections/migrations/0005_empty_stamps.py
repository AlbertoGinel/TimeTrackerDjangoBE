# timeSections/migrations/00XX_empty_stamps.py
from django.db import migrations

def empty_stamps(apps, schema_editor):
    Stamp = apps.get_model('timeSections', 'Stamp')
    Stamp.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('timeSections', '0004_migrate_to_uuid'),  # Replace with actual last migration
    ]
    
    operations = [
        migrations.RunPython(empty_stamps),
    ]