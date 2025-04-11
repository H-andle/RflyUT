from django.db import models

# Create your models here.
class Maps(models.Model):
    name = models.CharField(max_length=100, verbose_name="地图场景名称", blank=False, null=False)
    detail = models.TextField(verbose_name="说明", blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "地图场景"
        verbose_name_plural = verbose_name

class VehicleModels(models.Model):
    name = models.CharField(max_length=100, verbose_name="飞行器模型名称", blank=False, null=False)
    detail = models.TextField(verbose_name="说明", blank=True, null=True, help_text="字段待补充设计")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "飞行器模型"
        verbose_name_plural = verbose_name


class FaultModels(models.Model):
    name = models.CharField(max_length=100, verbose_name="故障模型名称", blank=False, null=False)
    detail = models.TextField(verbose_name="说明", blank=True, null=True, help_text="字段待补充设计")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "故障模型"
        verbose_name_plural = verbose_name
