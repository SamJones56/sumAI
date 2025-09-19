# https://github.com/bhancockio/agent-development-kit-crash-course/blob/main/5-sessions-and-state/basic_stateful_session.py
import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from sum_agent import sum_agent
from datetime import datetime

load_dotenv()


def get_current_date():
    """
    This tool returns the current date when the tool is ran.
    """
    today = datetime.today().strftime("%Y.%m.%d")
    return today


session_service_stateful = InMemorySessionService()
initial_state = {"todays_date": get_current_date()}
APP_NAME = "Sum Bot"
USER_ID = "001"
SESSION_ID = str(uuid.uuid4())


stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)

print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")

runner = Runner(
    agent=sum_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)

new_message = types.Content(role="user", parts=[types.Part(text="What happened today")])

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

print("==== Session Event Exploration ====")
session = session_service_stateful.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

# Log final Session state
print("=== Final Session State ===")
for key, value in session.state.items():
    print(f"{key}: {value}")
