from django.db import models

from web.domains.country.models import Country
from web.models.mixins import Archivable

COMMODITY_TYPES = {
    **dict.fromkeys(
        ["28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39"], "Chemicals"
    ),
    **dict.fromkeys(["72", "73", "76"], "Iron, Steel and Aluminium"),
    **dict.fromkeys(
        [
            "2707",
            "2709",
            "2710",
            "2711",
            "2712",
            "2713",
            "2714",
            "2715",
            "2812",
            "2814",
            "2901",
            "2902",
            "2903",
            "2905",
            "2907",
            "2909",
            "2910",
            "2914",
            "2917",
            "2926",
            "2929",
            "3901",
        ],
        "Oil and Petrochemicals",
    ),
    **dict.fromkeys(
        [
            "50",
            "51",
            "52",
            "53",
            "54",
            "55",
            "56",
            "57",
            "58",
            "59",
            "60",
            "61",
            "62",
            "63",
            "9619",
        ],
        "Textiles",
    ),
    "93": "Firearms and Ammunition",
    "97": "Firearms and Ammunition",
    "87": "Vehicles",
    "71": "Precious Metals and Stones",
    "4403": "Wood",
    "4402": "Wood Charcoal",
}


class Unit(models.Model):
    unit_type = models.CharField(max_length=20, blank=False, null=False)
    description = models.CharField(max_length=100, blank=False, null=False)
    short_description = models.CharField(max_length=30, blank=False, null=False)
    hmrc_code = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.description


class CommodityType(models.Model):
    type_code = models.CharField(max_length=20)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Commodity(Archivable, models.Model):
    LABEL = "Commodity"

    is_active = models.BooleanField(blank=False, null=False, default=True)
    start_datetime = models.DateTimeField(auto_now_add=True, blank=False, null=False)
    end_datetime = models.DateTimeField(blank=True, null=True)
    commodity_code = models.CharField(max_length=10, blank=False, null=False)
    validity_start_date = models.DateField(blank=False, null=True)
    validity_end_date = models.DateField(blank=True, null=True)
    quantity_threshold = models.IntegerField(blank=True, null=True)
    sigl_product_type = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        if self.id:
            return f"{self.LABEL} - {self.commodity_code}"
        else:
            return self.LABEL

    class Meta:
        ordering = (
            "-is_active",
            "commodity_code",
        )

    @property
    def commodity_type(self):
        if self.commodity_code:
            prefix_two_digits = self.commodity_code[:2]
            prefix_four_digits = self.commodity_code[:4]
            ct = COMMODITY_TYPES.get(prefix_two_digits)
            if ct is None:
                ct = COMMODITY_TYPES.get(prefix_four_digits, "N/A")
            return ct
        else:
            return "N/A"


class CommodityGroup(Archivable, models.Model):
    LABEL = "Commodity Group"

    AUTO = "AUTO"
    CATEGORY = "CATEGORY"

    TYPES = [(AUTO, "Auto"), (CATEGORY, ("Category"))]

    is_active = models.BooleanField(blank=False, null=False, default=True)
    start_datetime = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    end_datetime = models.DateTimeField(blank=True, null=True)
    group_type = models.CharField(
        max_length=20, choices=TYPES, blank=False, null=False, default=AUTO
    )
    group_code = models.CharField(max_length=25, blank=False, null=False)
    group_name = models.CharField(max_length=100, blank=True, null=True)
    group_description = models.CharField(max_length=4000, blank=True, null=True)
    commodity_type = models.ForeignKey(
        CommodityType, on_delete=models.PROTECT, blank=True, null=True
    )
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, blank=True, null=True)
    commodities = models.ManyToManyField(Commodity, blank=True)

    @property
    def group_type_verbose(self):
        return self.get_group_type_display()

    @property
    def commodity_type_verbose(self):
        return self.commodity_type.type

    def __str__(self):
        if self.pk and self.group_name:
            return f"{self.group_code} - {self.group_name}"
        elif self.pk:
            return self.group_code
        else:
            return self.LABEL

    class Meta:
        ordering = (
            "-is_active",
            "group_code",
        )


class Usage(models.Model):
    application_type = models.ForeignKey("web.ImportApplicationType", on_delete=models.PROTECT)
    application_subtype = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=False, null=False)
    commodity_group = models.ForeignKey(
        CommodityGroup, on_delete=models.PROTECT, related_name="usages"
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    maximum_allocation = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ("-start_datetime",)
