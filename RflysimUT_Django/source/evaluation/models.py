from django.db import models
from source.experiment.models import Experiments

# Create your models here.
class Index(models.Model):
    type = models.IntegerField(verbose_name="评估类型", blank=False, null=False, help_text="")
    name = models.CharField(max_length=100, verbose_name="评估指标名称说明", blank=True, null=True, default="")
    level = models.IntegerField(verbose_name="指标等级", blank=False, null=False, help_text="1表示一级指标，2表示二级指标，以此类推")
    para = models.TextField(verbose_name="默认指标参数", blank=True, null=False, help_text="JSON格式，包含各个评价指标所需阈值参数")
    superior = models.ForeignKey(to='self', verbose_name="上级指标", on_delete=models.SET_NULL, blank=True, null=True, default=0, help_text="一级指标无上级指标")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "指标"
        verbose_name_plural = verbose_name


class Values(models.Model):
    experiment = models.ForeignKey(to=Experiments, on_delete=models.CASCADE, verbose_name="所属实验", blank=False, null=False)
    index = models.ForeignKey(to=Index, on_delete=models.CASCADE, verbose_name="指标", blank=False, null=False)
    para = models.TextField(verbose_name="自定义指标参数", blank=True, null=True, help_text="JSON格式，包含各个评价指标所需阈值参数，为空时，使用默认指标参数计算")
    value = models.FloatField(verbose_name="指标数值", blank=True, null=False, default=0)

    def __str__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    def __repr__(self):
        return str(self.id)

    class Meta:
        verbose_name = "评估数值"
        verbose_name_plural = verbose_name
