from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import IEDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.james import JamesHelper
from fixture.signup import SignupHelper
from fixture.mail import MailHelper
from fixture.soap import SoapHelper


class Application:
    def __init__(self, browser, config): #base_url, login, password):

        if browser == 'firefox':
            #self.wd = webdriver.Firefox()
            options = Options()
            options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
            self.wd = webdriver.Firefox(executable_path=r'C:\users\nadya\PycharmProjects\python_training_mantis\fixture\geckodriver.exe',
                                        options=options)
        elif browser == 'chrome':
            self.wd = webdriver.Chrome(ChromeDriverManager().install())
        elif browser == 'ie':
            self.wd = webdriver.Ie(IEDriverManager().install())
        else:
            raise ValueError("Unrecognized browser %s", browser)
        self.session = SessionHelper(self)
        self.config = config
        self.base_url = config['web']['baseURL']
        self.login = config['webadmin']['username']
        self.password = config['webadmin']['password']
        self.project = ProjectHelper(self)
        self.james = JamesHelper(self)
        self.signup = SignupHelper(self)
        self.mail = MailHelper(self)
        self.soap = SoapHelper(self, self.login, self.password)

    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

