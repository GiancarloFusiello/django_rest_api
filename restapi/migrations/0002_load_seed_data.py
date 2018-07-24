import json
import os
from datetime import datetime

from django.conf import settings
from django.db import migrations

def load_seed_data(apps, schema_editor):
    Creator = apps.get_model("restapi", "Creator")
    Prezi = apps.get_model("restapi", "Prezi")
    db_alias = schema_editor.connection.alias

    file_path = os.path.join(settings.BASE_DIR, 'big_json_infra_hw.json')
    with open(file_path) as f:
        seed_data = json.load(f)

    for data in seed_data:
        creator, was_created = Creator.objects.using(db_alias).get_or_create(
            id=data['creator']['id'],
            name=data['creator']['name']
        )

        Prezi.objects.using(db_alias).create(
            id=data['id'],
            picture=data['picture'],
            title=data['title'],
            created_at=datetime.strptime(
                data['createdAt'], '%a %b %d %Y %H:%M:%S GMT%z (%Z)'
            ),
            creator=creator
        )

def remove_data(apps, schema_editor):
    Creator = apps.get_model("restapi", "Creator")
    Prezi = apps.get_model("restapi", "Prezi")
    db_alias = schema_editor.connection.alias
    Creator.objects.using(db_alias).all().delete()
    Prezi.objects.using(db_alias).all().delete()

class Migration(migrations.Migration):

    dependencies = [('restapi', '0001_initial')]

    operations = [
        migrations.RunPython(load_seed_data, remove_data),
    ]