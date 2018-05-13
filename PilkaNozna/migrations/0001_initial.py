# Generated by Django 2.0.4 on 2018-04-24 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Klub',
            fields=[
                ('id_klubu', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa_klubu', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Klub',
            },
        ),
        migrations.CreateModel(
            name='Liga',
            fields=[
                ('id_ligi', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa_ligi', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Liga',
            },
        ),
        migrations.CreateModel(
            name='Mecz',
            fields=[
                ('id_meczu', models.AutoField(primary_key=True, serialize=False)),
                ('kolejka', models.IntegerField()),
                ('data_meczu', models.DateField()),
                ('id_klubu1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Klub_1', to='PilkaNozna.Klub')),
                ('id_klubu2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Klub_2', to='PilkaNozna.Klub')),
            ],
            options={
                'verbose_name_plural': 'Mecz',
            },
        ),
        migrations.CreateModel(
            name='Pilkarz',
            fields=[
                ('id_pilkarza', models.AutoField(primary_key=True, serialize=False)),
                ('imie', models.TextField()),
                ('nazwisko', models.TextField()),
                ('data_urodzenia', models.DateField()),
                ('id_klubu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PilkaNozna.Klub')),
            ],
            options={
                'verbose_name_plural': 'Piłkarz',
            },
        ),
        migrations.CreateModel(
            name='Pozycja',
            fields=[
                ('id_pozycji', models.AutoField(primary_key=True, serialize=False)),
                ('nazwa_pozycji', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Pozycja',
            },
        ),
        migrations.CreateModel(
            name='Statystyki_gracza',
            fields=[
                ('id_statystyki', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('gole', models.IntegerField(default=0)),
                ('asysty', models.IntegerField(default=0)),
                ('faule', models.IntegerField(default=0)),
                ('zolta', models.IntegerField(default=0)),
                ('czerwona', models.IntegerField(default=0)),
                ('id_meczu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PilkaNozna.Mecz')),
                ('id_pilkarza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PilkaNozna.Pilkarz')),
            ],
            options={
                'verbose_name_plural': 'Statystyki',
            },
        ),
        migrations.AddField(
            model_name='pilkarz',
            name='id_pozycji',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PilkaNozna.Pozycja'),
        ),
        migrations.AddField(
            model_name='klub',
            name='id_ligi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PilkaNozna.Liga'),
        ),
    ]