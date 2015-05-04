"""Sample automated test suite for commotion router's unprivileged functions.
   These are an inefficient use of selenium, but are included as examples.
"""

import objects.browser as cbo
import objects.router.page.page as cpo


class TestFirefoxUnprivileged(cbo.BrowserTestContext):
    """Unittest child class for unprivileged functions"""

    def test_show_correct_version(self):
        """Check the footer for the current Commotion revision"""
        home = cpo.CRHomePage(self.browser)
        test_rev = "Commotion Router Release 1.1rc2"
        # This should return the footer string instead, then assertEqual
        self.assertTrue(home.show_current_rev(test_rev),
                        'Incorrect revision in footer')

    def test_default_no_user_apps(self):
        """
        By default, the router homepage should not allow unprivileged
        users to add applications.
        Calls homepage object.
        """
        home = cpo.CRHomePage(self.browser)
        self.assertFalse(home.users_can_add_apps(),
                         'Default app permissions incorrect')
