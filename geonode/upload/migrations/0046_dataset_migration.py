# Generated by Django 3.2.15 on 2022-10-04 13:03

from django.db import migrations
from geonode.upload.orchestrator import orchestrator
from geonode.layers.models import Dataset


def dataset_migration(apps, _):
    NewResources = apps.get_model("upload", "ResourceHandlerInfo")
    for old_resource in Dataset.objects.exclude(
        pk__in=NewResources.objects.values_list("resource_id", flat=True)
    ).exclude(subtype__in=["remote", None]):
        if hasattr(old_resource, 'files'):
            # generating orchestrator expected data file
            if not old_resource.files:
                if old_resource.is_vector():
                    converted_files = [{"base_file": "placeholder.shp"}]
                else:
                    converted_files = [{"base_file": "placeholder.tiff"}]
            else:
                converted_files = [{"base_file": x} for x in old_resource.files]
            # try to get the handler for the file of the old resource
            # when is found, we can exit
            handler_to_use = None
            for _input in converted_files:
                handler = orchestrator.get_handler(_input)
                if handler is not None:
                    handler_to_use = handler
                    break
            handler_to_use.create_resourcehandlerinfo(
                handler_module_path=str(handler_to_use),
                resource=old_resource,
                execution_id=None,
                kwargs={"is_legacy": True},
            )


class Migration(migrations.Migration):
    dependencies = [
        ("upload", "0045_fixup_dynamic_shema_table_names"),
    ]

    operations = [
        migrations.RunPython(dataset_migration),
    ]
