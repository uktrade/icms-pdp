from web.domains.importer.models import Importer
from web.tests.auth import AuthTestCase
from web.tests.domains.importer.factory import ImporterFactory

LOGIN_URL = "/"
ADMIN_PERMISSIONS = ["IMP_MAINTAIN_ALL"]
SECTION5_AUTHORITY_PERMISSIONS = ["IMP_EDIT_SECTION5_AUTHORITY"]
FIREARMS_AUTHORITY_PERMISSIONS = ["IMP_EDIT_FIREARMS_AUTHORITY"]


class ImporterListViewTest(AuthTestCase):
    url = "/importer/"
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
        self.login_with_permissions(ADMIN_PERMISSIONS)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_external_user_access(self):
        self.login_with_permissions(SECTION5_AUTHORITY_PERMISSIONS)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_constabulary_access(self):
        self.login_with_permissions(FIREARMS_AUTHORITY_PERMISSIONS)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_title(self):
        self.login_with_permissions(ADMIN_PERMISSIONS)
        response = self.client.get(self.url)
        self.assertEqual(response.context_data["page_title"], "Maintain Importers")

    def test_anonymous_post_access_redirects(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_forbidden_post_access(self):
        self.login()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)

    def test_number_of_pages(self):
        # Create 58 importer as paging lists 50 items per page
        for i in range(58):
            ImporterFactory()

        self.login_with_permissions(ADMIN_PERMISSIONS)
        response = self.client.get(self.url)
        page = response.context_data["page"]
        self.assertEqual(page.paginator.num_pages, 2)

    def test_page_results(self):
        for i in range(53):
            ImporterFactory(is_active=True)
        self.login_with_permissions(ADMIN_PERMISSIONS)
        response = self.client.get(self.url + "?page=2")
        page = response.context_data["page"]
        self.assertEqual(len(page.object_list), 3)


class ImporterEditViewTest(AuthTestCase):
    def setUp(self):
        super().setUp()
        self.importer = ImporterFactory()
        self.url = f"/importer/{self.importer.id}/edit/"
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
        self.login_with_permissions(ADMIN_PERMISSIONS)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_page_title(self):
        self.login_with_permissions(ADMIN_PERMISSIONS)
        response = self.client.get(self.url)
        self.assertTrue(f"Editing {self.importer}", response.content)


class ImporterCreateViewTest(AuthTestCase):
    url = "/importer/new/individual/"
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
        self.login_with_permissions(ADMIN_PERMISSIONS)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_indiviual_importer_created(self):
        self.login_with_permissions(ADMIN_PERMISSIONS)
        expected_address = "3 avenue des arbres, Pommier"
        expected_postcode = "42000"
        data = {
            "user": self.user.pk,
            "eori_number": "GBPR",
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 0,
            "form-0-address": expected_address,
            "form-0-postcode": expected_postcode,
        }

        response = self.client.post(self.url, data)
        self.assertRedirects(response, "/importer/")
        importer = Importer.objects.first()
        self.assertEqual(importer.user.pk, self.user.pk)
        office = importer.offices.first()
        self.assertEqual(office.address, expected_address)
        self.assertEqual(office.postcode, expected_postcode)

    def test_organisation_importer_created(self):
        self.login_with_permissions(ADMIN_PERMISSIONS)
        data = {
            "name": "test importer",
            "eori_number": "GB",
            "form-TOTAL_FORMS": 1,
            "form-INITIAL_FORMS": 0,
            "form-0-address": "3 avenue des arbres, Pommier",
            "form-0-postcode": "42000",
        }

        url = "/importer/new/organisation/"
        response = self.client.post(url, data)
        self.assertRedirects(response, "/importer/")
        importer = Importer.objects.first()
        self.assertEqual(importer.name, "test importer")

    def test_page_title(self):
        self.login_with_permissions(ADMIN_PERMISSIONS)
        response = self.client.get(self.url)
        self.assertEqual(response.context_data["page_title"], "Create Importer for Individual")


class ImporterAgentCreateViewTest(AuthTestCase):
    base_url = "/importer/{pk}/agent/new/{agent_type}/"
    base_redirect_url = "{LOGIN_URL}?next={url}"

    def setUp(self):
        super().setUp()
        self.importer = ImporterFactory()

        self.url = self.base_url.format(pk=self.importer.pk, agent_type="individual")
        self.url_org = self.base_url.format(pk=self.importer.pk, agent_type="organisation")

        self.redirect_url = self.base_redirect_url.format(LOGIN_URL=LOGIN_URL, url=self.url)
        self.redirect_url_org = self.base_redirect_url.format(LOGIN_URL=LOGIN_URL, url=self.url_org)

    def test_individual_anonymous_access_redirects(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url)

    def test_individual_forbidden_access(self):
        self.login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_individual_authorized_access(self):
        self.login_with_permissions(ADMIN_PERMISSIONS)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_indiviual_agent_importer_created(self):
        self.login_with_permissions(ADMIN_PERMISSIONS)
        data = {
            "user": self.user.pk,
            # no office
            "form-TOTAL_FORMS": 0,
            "form-INITIAL_FORMS": 0,
        }

        response = self.client.post(self.url, data)
        self.assertRedirects(response, "/importer/")
        self.assertEqual(self.importer.agents.count(), 1)

    def test_organisation_anonymous_access_redirects(self):
        response = self.client.get(self.url_org)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.redirect_url_org)

    def test_organisation_forbidden_access(self):
        self.login()
        response = self.client.get(self.url_org)
        self.assertEqual(response.status_code, 403)

    def test_organisation_authorized_access(self):
        self.login_with_permissions(ADMIN_PERMISSIONS)
        response = self.client.get(self.url_org)
        self.assertEqual(response.status_code, 200)

    def test_organisation_agent_importer_created(self):
        self.login_with_permissions(ADMIN_PERMISSIONS)
        data = {
            "name": "agent org",
            "registered_number": "GB42",
            # no office
            "form-TOTAL_FORMS": 0,
            "form-INITIAL_FORMS": 0,
        }

        response = self.client.post(self.url, data)
        self.assertRedirects(response, "/importer/")
        self.assertEqual(self.importer.agents.count(), 1)
