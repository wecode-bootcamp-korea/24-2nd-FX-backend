# Generated by Django 3.2.7 on 2021-09-14 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('signup_type', models.CharField(max_length=100)),
                ('kakao_id', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watching_time', models.TimeField(null=True)),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_details', to='contents.detail')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_details', to='users.user')),
            ],
            options={
                'db_table': 'user_detail_relations',
            },
        ),
    ]