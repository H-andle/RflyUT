from django.db import models
from source.proposal.models import Proposals


# Create your models here.
class Permissions(models.Model):
    name = models.CharField(max_length=100, verbose_name="权限名称", blank=False, null=False, default="", help_text="权限名称")
    level = models.IntegerField(verbose_name="权限等级", blank=False, null=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "通行权限"
        verbose_name_plural = verbose_name


class Layers(models.Model):
    name = models.CharField(max_length=100, verbose_name="航路网层级名称", blank=False, null=False, default="")
    level = models.IntegerField(verbose_name="权限等级", blank=False, null=False)
    height = models.FloatField(verbose_name="所在高度", blank=False, null=False, default=120.0)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name
    
    class Meta:
        verbose_name = "航路网层级"
        verbose_name_plural = verbose_name


class Nodes(models.Model):
    proposal = models.ForeignKey(to=Proposals, on_delete=models.CASCADE, verbose_name="所属方案", blank=False, null=False)
    name = models.CharField(max_length=100, verbose_name="节点名称", blank=True, null=False, default="", help_text="节点名称，可以编号命名")
    permission = models.ForeignKey(to=Permissions, on_delete=models.PROTECT, blank=True, null=True, verbose_name="通行权限")
    type = models.CharField(max_length=100,verbose_name="节点类型", blank=True, null=True, help_text="包括Junction,EntranceVirtual等")
    connections = models.TextField(verbose_name="联接关系", blank=True, null=True, help_text="当节点类型为Junction时，Edges间联接关系,Json格式，\
                                   Connection(incomingEdge,connectingEdge,contactPoint(start/end),lanelinks(from,to)")
    max_cross = models.IntegerField(verbose_name="最大通行量", blank=True, null=True)
    max_speed = models.FloatField(verbose_name="最大通行速度", blank=True, null=True, help_text="单位：m/s")
    gps = models.CharField(max_length=100, verbose_name="节点位置", blank=False, null=False, help_text="地图上的坐标点，格式为...(待定)")
    radius = models.FloatField(verbose_name="节点半径", blank=False, null=False, default=5.0, help_text="单位：m")
    layer = models.ForeignKey(to=Layers, on_delete=models.CASCADE, verbose_name="所属层级", blank=True, null=True)
    tag = models.CharField(max_length=100, verbose_name="标签", blank=True, null=True)

    class Meta:
        verbose_name = "节点"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name


class Edges(models.Model):
    proposal = models.ForeignKey(to=Proposals, on_delete=models.CASCADE, verbose_name="所属方案", blank=False, null=False)
    name = models.CharField(max_length=100, verbose_name="航路名称", blank=True, null=False, default="", help_text="航路名称，可以编号命名")
    start_node = models.ForeignKey(to=Nodes, on_delete=models.PROTECT, related_name='start', blank=False, null=False, verbose_name="起点节点")
    end_node = models.ForeignKey(to=Nodes, on_delete=models.PROTECT, related_name='end', blank=False, null=False, verbose_name="终点节点")
    nodes = models.TextField(verbose_name="航路管道中心线坐标列表", blank=True, null=False, help_text="格式为...（待定）")
    length = models.FloatField(verbose_name="管道长度", blank=True, null=False, help_text="单位：m")
    height = models.FloatField(verbose_name="管道高度", blank=True, null=False, help_text="单位：m")
    width = models.FloatField(verbose_name="管道宽度", blank=True, null=False, help_text="单位：m")
    permission = models.ForeignKey(to=Permissions, on_delete=models.PROTECT, blank=True, null=True, verbose_name="通行权限")
    max_cross = models.IntegerField(verbose_name="最大通行量", blank=True, null=True)
    max_speed = models.FloatField(verbose_name="最大通行速度", blank=True, null=True, help_text="单位：m/s")
    gps = models.CharField(max_length=100, verbose_name="航路位置", blank=True, null=True, help_text="地图上的坐标点，格式为...(待定)")
    volume = models.FloatField(verbose_name="航路管道体积容量", blank=True, null=False, help_text="单位：m^3")
    lanes = models.TextField(verbose_name="航道", blank=True, null=True, help_text="描述航路内的航道结构，Json格式，\
                              Lane(id,link(predecessor,successor),width,height,speed,type)")
    junction = models.IntegerField(verbose_name="为交叉口", blank=True, null=False, default=-1, help_text="航路作为节点内联接道路所属交叉口id，非则使用-1")
    rule = models.IntegerField(verbose_name="行驶规则", blank=True, null=False, default=1, help_text="航路行驶规则，1=靠左行，-1=靠右行，默认为1")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "航路"
        verbose_name_plural = verbose_name


class Airports(models.Model):
    proposal = models.ForeignKey(to=Proposals, on_delete=models.PROTECT,verbose_name="所属方案", blank=False, null=False)
    name = models.CharField(max_length=100, verbose_name="机场名称", blank=True, null=True, default="", help_text="可以编号命名")
    gps = models.CharField(max_length=100, verbose_name="机场位置", blank=False, null=False, help_text="地图上的坐标点，格式为...(待定)")
    radius = models.FloatField(verbose_name="机场半径", blank=False, null=False, default=5.0, help_text="单位：m")
    entrance_node = models.ForeignKey(to=Nodes, related_name='entrance', on_delete=models.PROTECT, blank=False, null=False, verbose_name="入口节点")
    exit_node = models.ForeignKey(to=Nodes, related_name='exit', on_delete=models.PROTECT, blank=False, null=False, verbose_name="出口节点")
    permission = models.ForeignKey(to=Permissions, on_delete=models.PROTECT, blank=True, null=True, verbose_name="通行权限")
    max_speed = models.FloatField(verbose_name="最大通行速度", blank=True, null=True, help_text="单位：m/s")
    capacity = models.IntegerField(verbose_name="机场容量", blank=True, null=False, default=1, help_text="单位：架")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "起降点"
        verbose_name_plural = verbose_name



