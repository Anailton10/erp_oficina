from django.db import migrations


def create_permissions_owner(owner, Permission):
    permissions = Permission.objects.filter(
        content_type__app_label__in=["clients", "orders", "products"]
    )
    owner.permissions.set(permissions)


def create_permissions_agent(agent, Permission):
    permissions = Permission.objects.filter(
        content_type__app_label__in=["clients", "orders", "products"]
    ).exclude(codename__startswith="delete")

    agent.permissions.set(permissions)


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    owner = Group.objects.create(name="Owner")
    agent = Group.objects.create(name="Attendant")

    create_permissions_owner(owner, Permission)
    create_permissions_agent(agent, Permission)


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.RunPython(create_groups),
    ]
