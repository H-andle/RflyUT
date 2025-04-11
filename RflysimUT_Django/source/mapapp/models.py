from django.db import models

class ClickAirport(models.Model):
    name = models.CharField(max_length=100, verbose_name="地图添加机场名称", blank=True, null=False, default="", help_text="可以编号命名")
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "地图添加机场"
        verbose_name_plural = verbose_name


class ClickNode(models.Model):
    name = models.CharField(max_length=100, verbose_name="地图添加节点名称", blank=True, null=False, default="", help_text="可以编号命名")
    x = models.IntegerField(null=False)
    y = models.IntegerField(null=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "地图添加节点"
        verbose_name_plural = verbose_name


class ClickEdge(models.Model):
    node1 = models.CharField(max_length=100, verbose_name="起始节点名称", blank=True, null=False)
    node2 = models.CharField(max_length=100, verbose_name="终止节点名称", blank=True, null=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    class Meta:
        verbose_name = "地图添加航路"
        verbose_name_plural = verbose_name
