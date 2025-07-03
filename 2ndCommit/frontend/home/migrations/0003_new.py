

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_login_output_signup'),
    ]

    operations = [
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
