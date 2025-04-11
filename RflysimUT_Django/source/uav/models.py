from django.db import models
from source.proposal.models import Proposals

# Create your models here.
class Drones(models.Model):
    proposal = models.ForeignKey(to=Proposals,on_delete=models.CASCADE,verbose_name="所属方案", blank=False, null=False)
    name = models.CharField(max_length=100, verbose_name="无人机名称", blank=True, null=True, default="", help_text="可以编号命名")
    max_speed = models.FloatField(verbose_name="最大速度", blank=True, null=False, help_text="单位：m/s")
    model = models.CharField(max_length=100, verbose_name="无人机型号", blank=True, null=True, default="")
    serial_number = models.CharField(max_length=100, verbose_name="无人机序列号", blank=True, null=True, default="")
    manufacturer = models.CharField(max_length=100, verbose_name="无人机制造商", blank=True, null=True, default="")
    manufacturer_date = models.DateField(verbose_name="制造日期", blank=True, null=True)
    registration_date = models.DateField(verbose_name="注册日期", blank=True, null=True)
    max_flight_time = models.IntegerField(verbose_name="最大飞行时间", blank=True, null=True, help_text="单位：分钟")
    battery_capacity = models.FloatField(verbose_name="电池容量", blank=True, null=True)
    payload_capacity = models.FloatField(verbose_name="最大载重量", blank=True, null=True)
    weight = models.FloatField(verbose_name="重量", blank=True, null=True, help_text="单位：kg")
    camera_resolution = models.CharField(max_length=100, verbose_name="摄像头分辨率", blank=True, null=True)
    safe_radius = models.FloatField(verbose_name="安全半径", blank=True, null=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "无人机"
        verbose_name_plural = verbose_name
