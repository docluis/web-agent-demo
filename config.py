import os

from langchain_anthropic import ChatAnthropic
from src.log import logger
from urllib.parse import urlparse
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.rate_limiters import InMemoryRateLimiter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


class Config:
    def __init__(self, website: str) -> None:
        load_dotenv()

        ####### Selenium #######
        self.chromedriver_path = "/usr/bin/chromedriver"
        self.service = ChromeService(executable_path=self.chromedriver_path)
        self.options = ChromeOptions()
        self.options.add_argument("--lang=en")
        self.options.add_experimental_option("perfLoggingPrefs", {"enableNetwork": True})
        self.options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.selenium_rate = 0.5

        ####### Model #######
        # self.rate_limiter = InMemoryRateLimiter(
        #     requests_per_second=45 / 60,  # 50 requests per minute, TIER 1 Anthropic
        #     # requests_per_second=5000/60, # 5000 requests per minute, TIER 2 OpenAI
        #     check_every_n_seconds=0.1,
        #     max_bucket_size=5000,
        # )
        # self.model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        # self.advanced_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        self.model = ChatAnthropic(model_name="claude-3-5-haiku-latest", temperature=0.2)
        self.advanced_model = ChatAnthropic(
            model_name="claude-3-5-haiku-latest", temperature=0.2
        )
        self.parser = StrOutputParser()

        ####### Target #######

        try:
            parsed_url = urlparse(website)
            self.target = f"{parsed_url.scheme}://{parsed_url.netloc}"
            self.initial_path = parsed_url.path
        except Exception as e:
            logger.error(f"Error parsing target URL: {e}")
            exit(1)
