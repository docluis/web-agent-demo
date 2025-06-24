from config import Config
from src.interaction_agent.agent import InteractionAgent
from src.llm.api_parser import LLM_ApiParser

# target = "https://demoqa.com/webtables"
target = "http://localhost:3000/"

print()
print("Starting interaction agent demo...")
print()
config = Config(target)
agent = InteractionAgent(cf=config, llm_page_request_parser=LLM_ApiParser(config))

# agent.interact(uri="/login", interaction="Login with admin:password123", limit="1")
# agent.interact(
#     uri="/create-post",
#     interaction="Create a post with title 'Hello World' and content 'This is a test post.'",
#     limit="1",
# )
# agent.interact(uri="/", interaction="Logout", limit="1")


phases = [
    "Login with the credentials admin:password123",
    "Create a post with title 'Hello World' and content 'This is a test post.'",
    "Logout",
]

agent.interact(
    uri="/",
    phases=phases,
)
