from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        #user checks out app's homepage
        self.browser.get(self.live_server_url)

        #user sees "to-do list" in the title and header
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #user is invited to enter an item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        #user types "buy peacock feathers" into a text box
        inputbox.send_keys('Buy peacock feathers')
        #when user hits enter,
        #taken to a new URL which says
        #"1: buy peacock feathers" as an item on a todo list table
        inputbox.send_keys(Keys.ENTER)
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        #the blank text box for new entries is stil there ...
        #user types "use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        #page updates again now with both items
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        #new user comes to site

        #use a new browser session to make sure no info is shared
        self.browser.quit()
        self.browser = webdriver.Firefox()

        #user2 visits home page ... with no sign of user1's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        #user2 starts a new list by entering an item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        #user2 gets unique URL
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url,user1_list_url)

        #still no trace of user1's list
        page_text - self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

if __name__ == '__main__':
    unittest.main(warnings='ignore')
