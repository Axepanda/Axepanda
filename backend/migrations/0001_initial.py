# Generated by Django 2.2.2 on 2019-09-20 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, max_length=20, null=True, verbose_name='文件名')),
                ('path', models.CharField(blank=True, max_length=108, null=True, verbose_name='文件路径')),
                ('size', models.CharField(blank=True, max_length=64, null=True, verbose_name='第1环')),
            ],
            options={
                'verbose_name': '文件表',
                'verbose_name_plural': '文件表',
            },
        ),
    ]
