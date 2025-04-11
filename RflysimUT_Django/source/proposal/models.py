from django.db import models
import constant

# Create your models here.
class Modes(models.Model):
    name = models.CharField(max_length=100, verbose_name="仿真模式名称", blank=False, null=False, default="", help_text="包括全质点、全状态等")
    detail = models.TextField(verbose_name="说明", blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "仿真模式"
        verbose_name_plural = verbose_name

class ProposalTypes(models.Model):
    name = models.CharField(max_length=100, verbose_name="仿真类型名称", blank=False, null=False, default="", help_text="包括规划、通信、避障等")
    detail = models.TextField(verbose_name="说明", blank=True, null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name
    
    class Meta:
        verbose_name = "仿真类型"
        verbose_name_plural = verbose_name


class Proposals(models.Model):
    name = models.CharField(max_length=100, verbose_name="名称", blank=False, null=False, default="", help_text="方案名称")
    detail = models.TextField(verbose_name="方案描述", blank=True, null=False, default="")
    map = models.CharField(max_length=100, verbose_name="地图场景", blank=False, null=False, default="", help_text="后续添加地图模型表后，修改为外键")
    mode = models.ForeignKey(to=Modes, on_delete=models.CASCADE, verbose_name="模式", blank=False, null=False)
    type = models.ForeignKey(to=ProposalTypes, on_delete=models.CASCADE, verbose_name="类型", blank=False, null=False)
    time = models.IntegerField(verbose_name="仿真时长", blank=False, null=False, default=600)
    create_time = models.DateTimeField(verbose_name="仿真创建时间", auto_now_add=True, blank=False, null=False)
    status = models.CharField(max_length=100, verbose_name="仿真状态", blank=False, null=False, default=constant.PROPOSAL_STATUS_STOP)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name
    
    class Meta:
        verbose_name = "仿真方案"
        verbose_name_plural = verbose_name
