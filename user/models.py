from django.db import models

from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    openid = models.CharField(verbose_name='唯一识别码',max_length=20,blank=True,null=True)
    phone = models.CharField(verbose_name="电话号码",max_length=11,blank=True,null=True)
    age = models.CharField(verbose_name="年龄",max_length=10,blank=True,null=True)
    gender_choice = ((0,"男"),(1,"女"))
    gender = models.SmallIntegerField(choices=gender_choice,default=0,verbose_name="性别")
    nationality = models.CharField(verbose_name='国籍',max_length=30,default='中国',null=True,blank=True)
    category = models.CharField(verbose_name='类别',max_length=20,null=True,blank=True)
    crunchies = models.CharField(verbose_name='榜单',max_length=20,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="录入时间")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = "用户信息表"


class Score(models.Model):
    user = models.ForeignKey("user.UserInfo",on_delete=models.CASCADE,null=True,blank=True)
    total = models.CharField(max_length=10,null=True,blank=True)
    first = models.CharField(max_length=10,null=True,blank=True)
    second = models.CharField(max_length=10,null=True,blank=True)
    third = models.CharField(max_length=10,null=True,blank=True)
    fourth = models.CharField(max_length=10,null=True,blank=True)
    fifth = models.CharField(max_length=10,null=True,blank=True)
    sixth = models.CharField(max_length=10,null=True,blank=True)
    seventh = models.CharField(max_length=10,null=True,blank=True)
    eighth = models.CharField(max_length=10,null=True,blank=True)
    ninth = models.CharField(max_length=10,null=True,blank=True)
    tenth = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return self.total

    class Meta:
        verbose_name = "积分表"
        verbose_name_plural = "积分表"
