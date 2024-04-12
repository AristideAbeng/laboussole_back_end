# Generated by Django 4.2.10 on 2024-04-07 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BourseEtude",
            fields=[
                ('id_bourse', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(blank=True, max_length=255, null=True)),
                ('date_limite', models.DateField(blank=True, null=True)),
                ('niveau', models.CharField(blank=True, max_length=255, null=True)),
                ('finance', models.CharField(blank=True, max_length=255, null=True)),
                ('ouvert_pour', models.CharField(blank=True, max_length=255, null=True)),
                ('pays', models.CharField(blank=True, max_length=255, null=True)),
                ('statut', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('etablissements_hotes', models.TextField(blank=True, null=True)),
                ('programme_eligible', models.TextField(blank=True, null=True)),
                ('nombre_bourse', models.CharField(blank=True, max_length=255, null=True)),
                ('duree', models.CharField(blank=True, max_length=255, null=True)),
                ('groupe_cible', models.CharField(blank=True, max_length=255, null=True)),
                ('avantages_bourse', models.TextField(blank=True, null=True)),
                ('critères_eligibilite', models.TextField(blank=True, null=True)),
                ('comment_postuler', models.TextField(blank=True, null=True)),
                ('page_officielle', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "db_table": "bourse_etude",
                "managed": False,
            },
        ),
    ]