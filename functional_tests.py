from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        
    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        #user checks out app's homepage
        self.browser.get('http://localhost:8000')

        #user sees "to-do list" in the title and header
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        #user is invited to enter an item straight away

        #user types "buy peacock feathers" into a text box

        #when user hits enter, page updates and now says
        #"1: buy peacock feathers" as an item on a todo list

        #the blank text box for new entries is stil there ...
        #user types "use peacock feathers to make a fly"

        #page updates again now with both items

        #how remember the list? user notices unique URL with explanatory text

        #user visits direct URL and sees todo list

        #user ends session

if __name__ == '__main__':
    unittest.main(warnings='ignore')
