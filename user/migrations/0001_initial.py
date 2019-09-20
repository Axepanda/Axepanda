# Generated by Django 2.2.2 on 2019-09-20 16:01

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.CharField(blank=True, max_length=50, null=True, verbose_name='头像')),
                ('openid', models.CharField(blank=True, max_length=64, null=True, verbose_name='openid')),
                ('phone', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话号码')),
                ('age', models.CharField(blank=True, max_length=10, null=True, verbose_name='年龄')),
                ('gender', models.CharField(blank=True, max_length=5, null=True, verbose_name='性别')),
                ('nationality', models.CharField(blank=True, default='中国', max_length=30, null=True, verbose_name='国籍')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息表',
                'verbose_name_plural': '用户信息表',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ScoreRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.CharField(blank=True, max_length=10, null=True, verbose_name='总分')),
                ('first', models.CharField(blank=True, max_length=10, null=True, verbose_name='第1环')),
                ('second', models.CharField(blank=True, max_length=10, null=True, verbose_name='第2环')),
                ('third', models.CharField(blank=True, max_length=10, null=True, verbose_name='第3环')),
                ('fourth', models.CharField(blank=True, max_length=10, null=True, verbose_name='第4环')),
                ('fifth', models.CharField(blank=True, max_length=10, null=True, verbose_name='第5环')),
                ('sixth', models.CharField(blank=True, max_length=10, null=True, verbose_name='第6环')),
                ('seventh', models.CharField(blank=True, max_length=10, null=True, verbose_name='第7环')),
                ('eighth', models.CharField(blank=True, max_length=10, null=True, verbose_name='第8环')),
                ('ninth', models.CharField(blank=True, max_length=10, null=True, verbose_name='第9环')),
                ('tenth', models.CharField(blank=True, max_length=10, null=True, verbose_name='第10环')),
                ('category', models.SmallIntegerField(choices=[(0, '竞技'), (1, '娱乐')], default=0, verbose_name='类别')),
                ('crunchies', models.SmallIntegerField(choices=[(0, '新手榜'), (1, '勇士榜'), (2, '宗师榜'), (3, '王者榜')], default=1, verbose_name='榜单')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='录入时间')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '积分表',
                'verbose_name_plural': '积分表',
            },
        ),
    ]
