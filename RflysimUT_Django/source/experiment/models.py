from django.db import models
from source.proposal.models import Proposals
from source.air_road.models import Edges
from source.uav.models import Drones
# Create your models here.
class Experiments(models.Model):
    name = models.CharField(max_length=100, verbose_name="实验名称", blank=False, null=False, default="", help_text="实验名称，默认值取“proposal_name:/{start_time/}”")
    proposal = models.ForeignKey(to=Proposals, on_delete=models.CASCADE, verbose_name="仿真方案设置", blank=False, null=False)    
    start_time = models.TimeField(verbose_name="仿真开始时间", auto_now_add=True, blank=True, null=False)
    end_time = models.TimeField(verbose_name="仿真结束时间", blank=True, null=False)
    exitflag = models.IntegerField(verbose_name="仿真退出原因", blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name
    
    class Meta:
        verbose_name = "仿真实验"
        verbose_name_plural = verbose_name
    

class EdgeLogs(models.Model):
    experiment = models.ForeignKey(to=Experiments, on_delete=models.PROTECT,verbose_name="所属仿真实验", blank=False, null=False)
    edge = models.ForeignKey(to=Edges, on_delete=models.CASCADE, blank=False, null=False, verbose_name="航路", help_text="日志对应航路")
    start_time = models.TimeField(verbose_name="日志开始时间", auto_now_add=True, blank=True, null=False)
    end_time = models.TimeField(verbose_name="日志结束时间", blank=True, null=False)
    duration = models.IntegerField(verbose_name="日志记录时间长度", blank=True, null=True, help_text="单位：s")
    density = models.TextField(verbose_name="飞行器密度记录", blank=True, null=False, help_text="JSON格式，包含各时刻航路内无人机密度")
    flow_rate = models.TextField(verbose_name="评价流速记录", blank=True, null=False, help_text="JSON格式，包含各时刻航路内无人机平均流速")
    type = models.IntegerField(verbose_name="日志类型", blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    class Meta:
        verbose_name = "航路日志"
        verbose_name_plural = verbose_name

class FlightLogs(models.Model):
    experiment = models.ForeignKey(to=Experiments, on_delete=models.PROTECT,verbose_name="所属仿真实验", blank=False, null=False)
    drone = models.ForeignKey(to=Drones, on_delete=models.CASCADE, blank=False, null=False,verbose_name="无人机",help_text="日志对应无人机")
    start_time = models.TimeField(verbose_name="日志开始时间",auto_now=True, blank=True, null=False,help_text="日志/飞行开始时间")
    end_time = models.TimeField(verbose_name="日志结束时间", blank=True, null=False,help_text="日志/飞行结束时间")
    duration = models.IntegerField(verbose_name="日志记录时间长度", blank=True, null=True, help_text="单位：s")
    start_location = models.CharField(max_length=100, verbose_name="起飞位置", blank=False, null=False, help_text="地图上的坐标点，格式为...(待定)")
    flight_path = models.TextField(verbose_name="飞行路径",blank = True,null=False,help_text= "JSON格式，包含各个路径点的经纬度和高度")
    type = models.IntegerField(verbose_name="日志类型", blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)


    class Meta:
        verbose_name = "飞行日志"
        verbose_name_plural = verbose_name
        db_table = 'experiment_FlightLogs'
