from django.db import models

class ExcelFile(models.Model):
    filename = models.CharField(max_length=20,null=True,blank=True,verbose_name="文件名")
    path = models.CharField(max_length=108,null=True,blank=True,verbose_name="文件路径")
    size = models.CharField(max_length=64,null=True,blank=True,verbose_name="第1环")

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = "文件表"
        verbose_name_plural = "文件表"

class Notice(models.Model):
    content = models.TextField(null=True,blank=True,verbose_name="公告内容")
    created = models.DateTimeField(auto_now_add=True,verbose_name="更新时间")