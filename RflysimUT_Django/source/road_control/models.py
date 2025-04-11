from django.db import models
from source.air_road.models import Edges
from source.proposal.models import Proposals
# Create your models here.
class RoadControl(models.Model):
    proposal = models.ForeignKey(to=Proposals,on_delete=models.CASCADE,verbose_name="所属方案", blank=False, null=False)
    type = models.IntegerField(verbose_name="管控类型", blank=False, null=False, help_text="0按权限通过，1限流，2限速")
    edge = models.ForeignKey(to=Edges,verbose_name="管控航路",on_delete=models.PROTECT, blank=True, null=False,help_text="管控航路")
    min_value = models.FloatField(verbose_name="管控量最大值", blank=True, null=False,help_text="当type=0，表示最大权限；当type=1，表示最大流量；当type=2，表示最大限速")
    max_value = models.FloatField(verbose_name="管控量最小值", blank=True, null=False, default=0)
    start_time = models.TimeField(verbose_name="管控开始时间", auto_now=True, blank=True, null=False)
    end_time = models.TimeField(verbose_name="管控结束时间", blank=True, null=False)
    duration = models.IntegerField(verbose_name="管控时长", blank=True, null=False, help_text="单位：s")

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    class Meta:
        verbose_name = "交通控制"
        verbose_name_plural = verbose_name
