# Generated by Django 3.2.7 on 2021-09-30 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_kakao_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='signup_type',
            field=models.CharField(choices=[(1, 'Flix'), (2, 'Kakao'), (3, 'Google')], default=1, max_length=100),
        ),
    ]
