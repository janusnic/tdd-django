from django.test import TestCase
from collections import namedtuple
from django.test import LiveServerTestCase
from selenium import webdriver
# we need the special ``Keys``class to send a carriage return to the password field.
from selenium.webdriver.common.keys import Keys

import time
PollInfo = namedtuple('PollInfo', ['question', 'choices'])
POLL1 = PollInfo(
    question="How awesome is Test-Driven Development?",
    choices=[
        'Very awesome',
        'Quite awesome',
        'Moderately awesome',
    ],
)
POLL2 = PollInfo(
    question="Which workshop treat do you prefer?",
    choices=[
        'Beer',
        'Pizza',
        'The Acquisition of Knowledge',
    ],
)

class PollsTest(LiveServerTestCase):

    fixtures = ['admin_user.json']

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_poll_via_admin_site(self):
        # Nerd opens her web browser, and goes to the admin page
        self.browser.get(self.live_server_url + '/admin/')

        # He sees the familiar 'Janus CMS' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Janus CMS', body.text)

        # Nerd types in his username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('janus')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('ghbdtnjanus')
        password_field.send_keys(Keys.RETURN)

        # his username and password are accepted, and he is taken to
        # the Site Administration page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # He now sees a couple of hyperlink that says "Polls"
        polls_links = self.browser.find_elements_by_link_text('Polls')
        self.assertEquals(len(polls_links), 1)

        # The second one looks more exciting, so he clicks it
        polls_links[0].click()

        # he is taken to the polls listing page, which shows he has
        # no polls yet
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('0 total', body.text)

        # he sees a link to 'add' a new poll, so he clicks it
        new_poll_link = self.browser.find_element_by_link_text('Add poll')
        new_poll_link.click()

        # he sees some input fields for "Question" and "Date published"
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Question', body.text)
        # self.assertIn('Pub date', body.text)
        self.assertIn('Date published', body.text)

        # he types in an interesting question for the Poll
        question_field = self.browser.find_element_by_name('question')
        question_field.send_keys("How awesome is Test-Driven Development?")

        # he sets the date and time of publication - it'll be a new year's
        # poll!
        date_field = self.browser.find_element_by_name('pub_date_0')
        date_field.send_keys('05/05/16')
        time_field = self.browser.find_element_by_name('pub_date_1')
        time_field.send_keys('00:00')

        # he sees he can enter choices for the Poll.  he adds three
        self.browser.find_element_by_id('choice_set0').click()
        time.sleep(2)
        choice_1 = self.browser.find_element_by_name('choice_set-0-choice')
        #time.sleep(10)
        #flag = choice_1.is_displayed() # flag = True - если элемент видим, flag = False - если нет
        #self.assertEquals(flag, True)
        
        choice_1.send_keys('Very awesome')
        self.browser.find_element_by_id('choice_set1').click()
        time.sleep(2)
        choice_2 = self.browser.find_element_by_name('choice_set-1-choice')
        choice_2.send_keys('Quite awesome')
        self.browser.find_element_by_id('choice_set2').click()
        time.sleep(2)
        choice_3 = self.browser.find_element_by_name('choice_set-2-choice')
        choice_3.send_keys('Moderately awesome')

        

        # Gertrude clicks the save button
        save_button = self.browser.find_element_by_css_selector("input[value='Save']")
        save_button.click()

        # She is returned to the "Polls" listing, where she can see her
        # new poll, listed as a clickable link
        new_poll_links = self.browser.find_elements_by_link_text(
                "How awesome is Test-Driven Development?"
        )
        self.assertEquals(len(new_poll_links), 1)


        # TODO: use the admin site to create a Poll
        self.fail('finish this test for Janus CMS')

    def _setup_polls_via_admin(self):
        # Gertrude logs into the admin site
        self.browser.get(self.live_server_url + '/admin/')
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('janus')
        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('ghbdtnjanus')
        password_field.send_keys(Keys.RETURN)

        # She has a number of polls to enter.  For each one, she:
        for poll_info in [POLL1, POLL2]:
            # Follows the link to the Polls app, and adds a new Poll
            self.browser.find_elements_by_link_text('Polls')[0].click()
            self.browser.find_element_by_link_text('Add poll').click()

            # Enters its name, and uses the 'today' and 'now' buttons to set
            # the publish date
            question_field = self.browser.find_element_by_name('question')
            question_field.send_keys(poll_info.question)
            date_field = self.browser.find_element_by_name('pub_date_0')
            date_field.send_keys('05/05/16')
            time_field = self.browser.find_element_by_name('pub_date_1')
            time_field.send_keys('00:00')
            #self.browser.find_element_by_link_text('Today').click()
            #self.browser.find_element_by_link_text('Now').click()

            # Sees she can enter choices for the Poll on this same page,
            # so she does
            for i, choice_text in enumerate(poll_info.choices):
                self.browser.find_element_by_id('choice_set%d' % i).click()
                time.sleep(2)
                choice_field = self.browser.find_element_by_name('choice_set-%d-choice' % i)
                choice_field.send_keys(choice_text)

            # Saves her new poll
            save_button = self.browser.find_element_by_css_selector("input[value='Save']")
            save_button.click()

            # Is returned to the "Polls" listing, where she can see her
            # new poll, listed as a clickable link by its name
            new_poll_links = self.browser.find_elements_by_link_text(
                    poll_info.question
            )
            self.assertEquals(len(new_poll_links), 1)

            # She goes back to the root of the admin site
            self.browser.get(self.live_server_url + '/admin/')

        # She logs out of the admin site
        self.browser.find_element_by_link_text('Log out').click()


    def test_voting_on_a_new_poll(self):
        # First, Gertrude the administrator logs into the admin site and
        # creates a couple of new Polls, and their response choices
        self._setup_polls_via_admin()

        # Now, Herbert the regular user goes to the homepage of the site. He
        # sees a list of polls.
        self.browser.get(self.live_server_url)
        heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(heading.text, 'Polls')

        # He clicks on the link to the first Poll, which is called
        # 'How awesome is test-driven development?'
        first_poll_title = 'How awesome is Test-Driven Development?'
        self.browser.find_element_by_link_text(first_poll_title).click()

        # He is taken to a poll 'results' page, which says
        # "no-one has voted on this poll yet"
        main_heading = self.browser.find_element_by_tag_name('h1')
        self.assertEquals(main_heading.text, 'Poll Results')
        sub_heading = self.browser.find_element_by_tag_name('h2')
        self.assertEquals(sub_heading.text, first_poll_title)
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('No-one has voted on this poll yet', body.text)

        # He also sees a form, which offers him several choices.
        # There are three options with radio buttons
        choice_inputs = self.browser.find_elements_by_css_selector(
                "input[type='radio']"
        )
        self.assertEquals(len(choice_inputs), 3)

        # The buttons have labels to explain them
        choice_labels = self.browser.find_elements_by_tag_name('label')
        choices_text = [c.text for c in choice_labels]
        self.assertEquals(choices_text, [
            'Vote:', # this label is auto-generated for the whole form
            'Very awesome',
            'Quite awesome',
            'Moderately awesome',
        ])
        # He decided to select "very awesome", which is answer #1
        chosen = self.browser.find_element_by_css_selector(
                "input[value='1']"
        )
        chosen.click()

        # Herbert clicks 'submit'
        self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

        # The page refreshes, and he sees that his choice
        # has updated the results.  they now say
        # "100 %: very awesome".
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('100 %: Very awesome', body_text)

        # The page also says "1 vote"
        self.assertIn('1 vote', body_text)

        # But not "1 votes" -- Herbert is impressed at the attention to detail
        self.assertNotIn('1 votes', body_text)

        # Herbert suspects that the website isn't very well protected
        # against people submitting multiple votes yet, so he tries
        # to do a little astroturfing
        self.browser.find_element_by_css_selector("input[value='1']").click()
        self.browser.find_element_by_css_selector("input[type='submit']").click()

        # The page refreshes, and he sees that his choice has updated the
        # results.  it still says # "100 %: very awesome".
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('100 %: Very awesome', body_text)

        # But the page now says "2 votes"
        self.assertIn('2 votes', body_text)

        # Cackling manically over his l33t haxx0ring skills, he tries
        # voting for a different choice
        self.browser.find_element_by_css_selector("input[value='2']").click()
        self.browser.find_element_by_css_selector("input[type='submit']").click()

        # Now, the percentages update, as well as the votes
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('67 %: Very awesome', body_text)
        self.assertIn('33 %: Quite awesome', body_text)
        self.assertIn('3 votes', body_text)

        # Satisfied, he goes back to sleep