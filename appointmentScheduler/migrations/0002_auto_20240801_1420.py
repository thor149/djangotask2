from django.db import migrations

def create_doctors(apps, schema_editor):
    Profile = apps.get_model('users', 'Profile')
    Doctor = apps.get_model('appointmentScheduler', 'Doctor')

    for profile in Profile.objects.filter(account_user_type='doctor'):
        Doctor.objects.get_or_create(profile=profile)

class Migration(migrations.Migration):

    dependencies = [
        ('appointmentScheduler', '0001_initial'),  # adjust based on your initial migration
        ('users', '0001_initial'),  # adjust based on your initial migration
    ]

    operations = [
        migrations.RunPython(create_doctors),
    ]
