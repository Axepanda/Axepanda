# Generated by Django 2.2.2 on 2019-09-29 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scorerecord',
            name='rank',
            field=models.IntegerField(blank=True, null=True, verbose_name='当前排名'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='头像'),
        ),
    ]