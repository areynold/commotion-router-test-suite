"""Sample automated test suite for commotion router's unprivileged functions.
   These are an inefficient use of selenium, but are included as examples.
"""

import objects.browser as browser
import objects.router.page.page as page


class TestFirefoxUnprivileged(browser.BrowserTestContext):
    """Unittest child class for unprivileged functions"""

    def test_show_correct_version(self):
        """Check the footer for the current Commotion revision"""
        home = page.CRHomePage(self.browser)
        test_rev = "Commotion Router Release 1.1rc2"
        # This should return the footer string instead, then assertEqual
        self.assertTrue(home.show_current_rev(self.browser, test_rev),
                        'Incorrect revision in footer')

    def test_default_no_user_apps(self):
        """
        By default, the router homepage should not allow unprivileged
        users to add applications.
        Calls homepage object.
        """
        home = page.CRHomePage(self.browser)
        self.assertFalse(home.users_can_add_apps(self.browser),
                         'Default app permissions incorrect')
