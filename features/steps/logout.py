from behave import when
from selenium.webdriver.common.by import By

from features.steps import utils


@when("the user clicks on logout button")
def click_on_logout(context):
    utils.go_to_page(context, "home")
    context.browser.find_element(By.ID, "btnLogout").click()
