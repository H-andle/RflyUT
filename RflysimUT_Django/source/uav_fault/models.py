from django.db import models
from source.uav.models import Drones
from source.proposal.models import Proposals
# Create your models here.

class FaultPlans(models.Model):
    proposal = models.ForeignKey(to=Proposals,on_delete=models.CASCADE,verbose_name="所属方案", blank=False, null=False)
    name = models.CharField(max_length=100, verbose_name="无人机名称", blank=True, null=True, default="")
    type = models.IntegerField(verbose_name="注入故障类型", blank=False, null=False, help_text="")
    drone = models.ForeignKey(to=Drones,verbose_name="故障无人机",on_delete=models.CASCADE, blank=True, null=False,help_text="故障注入为单机故障")
    para = models.TextField(verbose_name="故障参数",blank = True,null=False,help_text= "JSON格式，包含该故障类型所需参数")
    start_time = models.TimeField(verbose_name="故障开始时间",auto_now=True, blank=True, null=False)
    end_time = models.TimeField(verbose_name="故障结束时间", blank=True, null=False)
    duration = models.IntegerField(verbose_name="故障时长", blank=True, null=False, help_text="单位：s")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "故障注入"
        verbose_name_plural = verbose_name
