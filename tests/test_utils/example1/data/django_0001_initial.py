from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExampleModel1",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False, verbose_name="ID", auto_created=True)),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
