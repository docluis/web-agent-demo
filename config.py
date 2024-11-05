from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

class Config:
    def __init__(self):
        load_dotenv()

        # Selenium
        self.chromedriver_path = "/usr/bin/chromedriver"
        self.service = ChromeService(executable_path=self.chromedriver_path)
        self.options = ChromeOptions()
        self.options.add_argument("--lang=en")
        self.driver = webdriver.Chrome(service=self.service, options=self.options)

        # LLM
        self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)