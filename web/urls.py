from django.urls import include, path, register_converter

from web.views.views_healthcheck import health_check

from . import converters
from .views import home

register_converter(converters.NegativeIntConverter, "negint")
register_converter(converters.CaseTypeConverter, "casetype")
register_converter(converters.ExportApplicationTypeConverter, "exportapplicationtype")
register_converter(converters.SILSectionTypeConverter, "silsectiontype")

urlpatterns = [
    path("", include("web.auth.urls")),
    path("health-check/", health_check, name="health-check"),
    path("home/", home, name="home"),
    path("workbasket/", include("web.domains.workbasket.urls")),
    path("user/", include("web.domains.user.urls")),
    path("template/", include("web.domains.template.urls")),
    path("constabulary/", include("web.domains.constabulary.urls")),
    path("sanction-emails/", include("web.domains.sanction_email.urls")),
    path("commodity/", include("web.domains.commodity.urls")),
    path("country/", include("web.domains.country.urls")),
    path("product-legislation/", include("web.domains.legislation.urls")),
    path("firearms/", include("web.domains.firearms.urls")),
    path("section5/", include("web.domains.section5.urls")),
    path("importer/", include("web.domains.importer.urls")),
    path("exporter/", include("web.domains.exporter.urls")),
    path("case/", include("web.domains.case.urls")),
    path("access/", include("web.domains.case.access.urls", namespace="access")),
    path("import/", include("web.domains.case._import.urls")),
    path("export/", include("web.domains.case.export.urls", namespace="export")),
    path("mailshot/", include("web.domains.mailshot.urls")),
    path("select2/", include("django_select2.urls")),
]
