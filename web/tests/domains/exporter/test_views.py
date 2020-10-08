from guardian.shortcuts import assign_perm

from web.domains.exporter.models import Exporter
from web.tests.auth import AuthTestCase
from web.tests.domains.exporter.factory import ExporterFactory

LOGIN_URL = "/"


class ExporterListViewTest(AuthTestCase):
    url = "/exporter/"
    redirect_url = f"{LOGIN_URL}?next={url}"

    def test_anonymous_access_redirects(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

    def test_forbidden_access(self):
        self.login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_superuser_access(self):
        self.login()
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_admin_access(self):
        self.login_with_permissions(["reference_data_access", "exporter_access"])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_title(self):
        self.login_with_permissions(["reference_data_access", "exporter_access"])
        response = self.client.get(self.url)
        assert "Maintain Exporters" in response.content.decode()

    def test_anonymous_post_access_redirects(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_forbidden_post_access(self):
        self.login()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_number_of_pages(self):
        for i in range(52):
            ExporterFactory()

        self.login_with_permissions(["reference_data_access", "exporter_access"])
        response = self.client.get(self.url)
        page = response.context_data["page"]
        self.assertEqual(page.paginator.num_pages, 2)

    def test_page_results(self):
        for i in range(53):
            ExporterFactory(is_active=True)
        self.login_with_permissions(["reference_data_access", "exporter_access"])
        response = self.client.get(self.url + "?page=2")
        page = response.context_data["page"]
        self.assertEqual(len(page.object_list), 3)


class ExporterEditViewTest(AuthTestCase):
    def setUp(self):
        super().setUp()
        self.exporter = ExporterFactory()
        self.url = f"/exporter/{self.exporter.id}/edit/"
        self.redirect_url = f"{LOGIN_URL}?next={self.url}"

    def test_anonymous_access_redirects(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

    def test_forbidden_access(self):
        self.login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_authorized_access(self):
        self.login_with_permissions(["reference_data_access", "exporter_access"])
        assign_perm("web.is_contact_of_exporter", self.user, self.exporter)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_title(self):
        self.login_with_permissions(["reference_data_access", "exporter_access"])
        assign_perm("web.is_contact_of_exporter", self.user, self.exporter)
        response = self.client.get(self.url)
        assert f"Editing exporter {self.exporter}" in response.content.decode()


class ExporterCreateViewTest(AuthTestCase):
    url = "/exporter/create/"
    redirect_url = f"{LOGIN_URL}?next={url}"

    def test_anonymous_access_redirects(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

    def test_forbidden_access(self):
        self.login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_authorized_access(self):
        self.login_with_permissions(["reference_data_access", "exporter_access"])
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_exporter_created(self):
        self.login_with_permissions(["reference_data_access", "exporter_access"])
        self.client.post(self.url, {"name": "test exporter"})
        exporter = Exporter.objects.first()
        self.assertEqual(exporter.name, "test exporter")

    def test_page_title(self):
        self.login_with_permissions(["reference_data_access", "exporter_access"])
        response = self.client.get(self.url)
        assert "Create Exporter" in response.content.decode()
