from django.db import models
from source.uav.models import Drones
from source.air_road.models import Airports
from source.proposal.models import Proposals


# Create your models here.
class FlightRequirements(models.Model):
    proposal = models.ForeignKey(to=Proposals, on_delete=models.PROTECT, verbose_name="所属方案", blank=False, null=False)
    name = models.CharField(max_length=100, verbose_name="无人机名称", blank=True, null=True, default="")
    drone = models.ForeignKey(to=Drones, verbose_name="执行无人机", on_delete=models.PROTECT, blank=False, null=False, help_text="飞行计划对应执行的无人机")
    start_time = models.TimeField(verbose_name="计划开始时间", auto_now_add=True, blank=True, null=False)
    end_time = models.TimeField(verbose_name="计划结束时间", blank=True, null=False)
    duration = models.IntegerField(verbose_name="任务时长", blank=True, null=True, help_text="单位：s")
    priority = models.IntegerField(verbose_name="优先级", blank=True, null=True)
    start_airport = models.ForeignKey(to=Airports, verbose_name="起飞机场", related_name='start', on_delete=models.PROTECT, blank=False, null=False)
    end_airport = models.ForeignKey(to=Airports, verbose_name="降落机场", related_name='end', on_delete=models.PROTECT, blank=False, null=False)
    type = models.CharField(max_length=100, verbose_name="任务类型", blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "飞行计划"
        verbose_name_plural = verbose_name
