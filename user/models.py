from django.db import models
from django.contrib.auth.models import AbstractUser

class UserInfo(AbstractUser):
    avatar = models.CharField(max_length=200, null=True, blank=True, verbose_name="头像")
    openid = models.CharField(max_length=64,null=True,blank=True,verbose_name='openid')
    phone = models.CharField(verbose_name="电话号码",max_length=11,blank=True,null=True)
    age = models.CharField(verbose_name="年龄",max_length=10,blank=True,null=True)
    gender = models.CharField(max_length=5,verbose_name="性别",blank=True,null=True)
    nationality = models.CharField(verbose_name='国籍',max_length=30,default='中国',null=True,blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息表"
        verbose_name_plural = "用户信息表"

class ScoreRecord(models.Model):
    user = models.ForeignKey("user.UserInfo",on_delete=models.CASCADE,null=True,blank=True)
    total = models.CharField(max_length=10,null=True,blank=True,verbose_name="总分")
    first = models.CharField(max_length=10,null=True,blank=True,verbose_name="第1环")
    second = models.CharField(max_length=10,null=True,blank=True,verbose_name="第2环")
    third = models.CharField(max_length=10,null=True,blank=True,verbose_name="第3环")
    fourth = models.CharField(max_length=10,null=True,blank=True,verbose_name="第4环")
    fifth = models.CharField(max_length=10,null=True,blank=True,verbose_name="第5环")
    sixth = models.CharField(max_length=10,null=True,blank=True,verbose_name="第6环")
    seventh = models.CharField(max_length=10,null=True,blank=True,verbose_name="第7环")
    eighth = models.CharField(max_length=10,null=True,blank=True,verbose_name="第8环")
    ninth = models.CharField(max_length=10,null=True,blank=True,verbose_name="第9环")
    tenth = models.CharField(max_length=10,null=True,blank=True,verbose_name="第10环")
    category_choice = (
        (0, "竞技"),
        (1, "娱乐"),
    )
    category = models.SmallIntegerField(choices=category_choice, default=0, verbose_name='类别')
    crunchies_choice = (
        (0, "新手榜"),
        (1, "勇士榜"),
        (2, "宗师榜"),
        (3, "王者榜"),
    )
    crunchies = models.SmallIntegerField(choices=crunchies_choice, default=1, verbose_name='榜单')
    created = models.DateTimeField(auto_now_add=True, verbose_name="录入时间")
    rank = models.IntegerField(verbose_name="当前排名",null=True,blank=True)

    def __str__(self):
        return self.total

    class Meta:
        verbose_name = "积分表"
        verbose_name_plural = "积分表"
