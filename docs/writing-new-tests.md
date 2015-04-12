#Writing New UI Tests

##Write Page Model
* Identify unique page functions and elements
    * Testable common elements (e.g., header, footer elements) should go in a model of the template
    * Answer basic question - what functions must this page perform
* Identify page landmarks
    * Add to LOCATORS
    * LOCATORS is dict
    * Uses page class as primary key
    * Uses human-readable identifier as secondary key
    * Uses selenium-compatible locator (css class, link text, xpath, etc)
        as secondary value
    * Comment identifies type of locator for use in wait_for_element_of_type()
* Implement page as child class of CRCommonPage
    * Each unique function or element should be written as a method of the page
    * Each method should return true or false

##Write Unit Test
* All tests derive from browser context class, which derives from unittest
* Tests are written as methods for particular browser/permission class (e.g., admin privileges in firefox)
* Tests should be relatively simple assertions. Test logic should be contained in page methods.

##Run py.test
Py.test automatically discovers and runs all tests
that use the standard pytest naming conventions.

