"""
Collected page objects for Commotion Router web UI.
The page design pattern allows web pages and UI elements to be modeled with as much detail as needed,
while protecting test logic from under-the-hood changes.

Each page is represented by a class, and each page class should contain methods representing
functions unique to that page. Page-specific landmarks (logos, form fields, etc.) should be added
to the LOCATORS dictionary.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import objects.router.router as router
import objects.exceptions as exceptions

# Dictionary of core identifiers for each page.
#
# Summary: Each page has a number of landmark elements (logos, headings, etc.)
# that help us navigate and interact with the page. The LOCATORS variable is a
# dictionary of pages and their elements that can be called from tests.
#
# Structure:
# { name_of_page_class : {
# human_readable_element_title : selenium_compatible_element_identifier
# # inline comment containing identifier type
#       }
# }
#
# Use:
# Most often used with wait_for_element_of_type() or selenium's built-in locator functions.
# e.g., LOCATORS["common"]["commotion_logo"] would return the html ID ("device") of the template's
# Commotion logo, which can be used to check that the page has finished loading before attempting
# to run test functions.
LOCATORS = {
    "common": {
        "commotion_logo": "device",  # ID
        "version": "credits",  # Class - requires add'l filtering
    },
    "login": {
        "username_field": "username",  # Name
        "password_field": "focus_password",  # ID
        "error": "error",  # Class
        "submit": "cbi-button-apply",  # Class
        "reset": "cbi-button-reset",  # Class
    },
    "home": {
        "apps-header": "appsH2",  # Class
        "user-add-app": "add_app",  # ID
    },
    "admin": {
        "url-stok": False,
        "logout": "Logout",  # Link_Text
    },
}


class RouterTemplate(object):
    """Page objects common to all Commotion Router pages"""

    def __init__(self):
        """Set page within context of router."""
        page_url = None
        __sb = None
        commotion_node_ip = None

    # This is dumb and duplicative. We only need node_ip.
    # Try this http://pydanny.com/attaching-custom-exceptions-to-functions-and-classes.html
    _, commotion_client_ip = router.get_commotion_client_ip()
    try:
        commotion_node_ip = router.get_commotion_node_ip(commotion_client_ip)
    except TypeError:
        raise exceptions.CommotionIPError(
            'No valid Commotion IP address found'
        )
    except exceptions.CommotionIPError as args:
        print(args)

    def _verify_correct_page(self, __sb, page_url):
        """Sanity check defined page url against url in browser"""
        __sb.get(page_url)

        # Wait for known-good page element
        self.wait_for_page_load(__sb)

        try:
            # this assert may not work as expected
            assert (__sb.current_url == page_url) is True
            print(__sb.current_url + " matches " + page_url)
        except AssertionError:
            print("Rendered url %s does not match expected url %s" % (
                __sb.current_url, page_url
            ))

    @staticmethod
    def wait_for_page_load(__sb):
        """Tell selenium to wait for locator before proceeding"""
        print("Waiting for presence of known-good page element")
        try:
            WebDriverWait(__sb, 10).until(
                expected.presence_of_element_located((By.ID, "device")))
        except NoSuchElementException:
            message = "Page element 'device' not found!"
            print(message)
            raise Exception(message)
        else:
            print("%s loaded successfully" % __sb.current_url)

    @staticmethod
    def wait_for_element_of_type(__sb, etype, element):
        """
        Tell selenium to wait for a specific locator of specific type
        before proceeding.

        Valid types: ID, CLASS_NAME, CSS_SELECTOR, LINK_TEXT, NAME,
            PARTIAL_LINK_TEXT, TAG_NAME, XPATH
        """
        print("Waiting for %s, type %s" % (element, etype))
        try:
            WebDriverWait(__sb, 10).until(
                expected.presence_of_element_located((
                    (
                        getattr(By, etype)), element
                )))
        except NoSuchElementException:
            print("Page element %s of type %s not found!" % (
                element, etype
            ))
        else:
            print("Page element %s found." % element)
            return True


            # thisnode url
            # Header
            # Footer
            # Body


class CRHomePage(RouterTemplate):
    """Objects found on Commotion Router's default landing page"""

    def __init__(self, browser):
        super(CRHomePage, self).__init__()
        __sb = browser
        self.page_url = (
            'https://' + RouterTemplate.commotion_node_ip + '/cgi-bin/luci'
        )
        self._verify_correct_page(__sb, self.page_url)

    def show_current_rev(self, __sb, test_rev):
        """Check page footer for commotion version number.
        This is actually a common object but common class
        isn't written to accept tests."""
        print("Checking footer for correct Commotion Revision")
        RouterTemplate.wait_for_element_of_type(
            __sb, "CLASS_NAME", LOCATORS["common"]["version"]
        )
        print("Comparing versions")
        page_rev = __sb.find_element_by_class_name(LOCATORS["common"]
        ["version"])
        # Could also use page_rev.text.endswith(test_rev)
        if test_rev not in page_rev.text:
            print("Footer version %s does not match test version %s", (
                page_rev.text, test_rev))
            return False
        else:
            return True

    @staticmethod
    def users_can_add_apps(self, __sb):
        """When enabled, unprivileged users can add apps from the homepage"""
        print("Checking for app add button...")
        try:
            __sb.find_element_by_id(LOCATORS["home"]["user-add-app"])
        except NoSuchElementException:
            return False
        else:
            print("Users can add applications from the homepage")
            return True


class CRLoginPage(RouterTemplate):
    """Page objects specific to Commotion Router login page.
        Note that the login page triggers a DOM-less cert error
    """

    def __init__(self, browser):
        super(CRLoginPage, self).__init__()
        __sb = browser
        self.page_url = (
            'https://' + RouterTemplate.commotion_node_ip + '/cgi-bin/luci/admin'
        )
        self._verify_correct_page(__sb, self.page_url)

    @staticmethod
    def password_required(__sb):
        """
        Admin pages should require a password if stok url token is not present.
        """
        print("Checking for password field...")
        try:
            __sb.find_element_by_id(LOCATORS["login"]["password_field"])
        except NoSuchElementException:
            print("Login page element %s not found" % (
                LOCATORS["login"]["password_field"]
            ))
            return False
        else:
            print("Login page requires a password")
            return True

    def incorrect_pass_returns_error(self, __sb, password):
        """The login form should reject incorrect passwords"""
        print("Testing user-supplied password")
        __sb.find_element_by_id(
            LOCATORS["login"]["password_field"]
        ).send_keys(password)

        if "\n" not in password:
            # Click submit if password doesn't have a newline
            __sb.find_element_by_class_name("cbi-button-apply").click()

        RouterTemplate.wait_for_element_of_type(
            __sb, "CLASS_NAME", LOCATORS["login"]["error"]
        )
        # Rewrite as try/except NoSuchElementException/else
        if __sb.find_element_by_class_name(LOCATORS["login"]["error"]).is_displayed():
            print("Login page displays error message on incorrect password")
            return True
        else:
            print("Login page does not display error message "
                  "on incorrect password")
            return False

    def correct_pass_allows_access(self, __sb, password):
        """
        Correct password in login form should allow access to admin pages
        """
        print("Testing user-supplied password")
        __sb.find_element_by_id(
            LOCATORS["login"]["password_field"]
        ).send_keys(password)

        if "\n" not in password:
            # Click submit if password doesn't have a newline
            __sb.find_element_by_class_name("cbi-button-apply").click()

        RouterTemplate.wait_for_element_of_type(
            __sb, "LINK_TEXT", LOCATORS["admin"]["logout"]
        )

        # Rewrite as try/except NoSuchElementException/else
        if __sb.find_element_by_link_text(LOCATORS["admin"]["logout"]).is_displayed():
            print("Login successful")
            return True
        else:
            print("Login unsuccessful")
            return False


class CRAdminPage(RouterTemplate):
    """Page objects accessible only to authenticated admin users"""
    # Side Nav
    ## Logout
    # URL stok (Note: This also allows csrf vuln)
    #page_url = 'https://' + self.netinfo.commotion_node_ip \
    #+ '/cgi-bin/luci/admin'
    pass
