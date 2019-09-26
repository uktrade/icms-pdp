from web.models.mixins import Archivable
from django.db import models


class ProductLegislation(Archivable, models.Model):
    name = models.CharField(max_length=500, blank=False, null=False)
    is_active = models.BooleanField(blank=False, null=False, default=True)
    is_biocidal = models.BooleanField(blank=False, null=False, default=False)
    is_eu_cosmetics_regulation = models.BooleanField(blank=False,
                                                     null=False,
                                                     default=False)
    is_biocidal_claim = models.BooleanField(blank=False,
                                            null=False,
                                            default=False)

    @property
    def is_biocidal_yes_no(self):
        return 'Yes' if self.is_biocidal else 'No'

    @property
    def is_biocidal_claim_yes_no(self):
        return 'Yes' if self.is_biocidal_claim else 'No'

    @property
    def is_eu_cosmetics_regulation_yes_no(self):
        return 'Yes' if self.is_eu_cosmetics_regulation else 'No'

    class Meta:
        ordering = ('name', )

    class Display:
        display = [
            'name', 'is_biocidal_yes_no', 'is_biocidal_claim_yes_no',
            'is_eu_cosmetics_regulation_yes_no'
        ]
        labels = [
            'legislation Name', 'Is Biocidal', 'Is Biocidal Claim',
            'Is EU Cosmetics Regulation'
        ]