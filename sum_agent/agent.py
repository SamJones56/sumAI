from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import os
from datetime import datetime
from subprocess import run
import json
from pathlib import Path

model = LiteLlm(
    model="openrouter/deepseek/deepseek-chat-v3.1:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)


def get_current_date():
    """
    This tool returns the current date when the tool is ran.
    """
    today = datetime.today().strftime("%Y.%m.%d")
    return today


# https://www.elastic.co/docs/solutions/search/the-search-api
def pull_data():
    """
    This tool takes todays date, pulls all elastic JSON data, and writes it to a file in "./log_data/{today}.json"
    """
    today = get_current_date()
    file_path = f"./log_data/{today}.json"
    print(f"Pulling data from {today}\nSaving to {file_path}")
    cmd = [
        "curl",
        "-X",
        "GET",
        f"http://127.0.0.1:64298/logstash-{today}/_search?pretty",
        "-H",
        "Content-Type: application/json",
        "-d",
        '{ "query": { "match_all": {} }, "size": 10000}',
    ]
    result = run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    print(f"Writing to {file_path}")
    with open(f"{file_path}", "w") as f:
        json.dump(data, f)
    print(f"File write completed")


def get_data(file_path: Path):
    """ """
    allowed_dir = "./log_data"
    today = get_current_date()
    data = []
    if file_path.parent == allowed_dir:
        for line in open(f"file_path", "r"):
            data.append(line.strip())
    return data


sum_agent = Agent(
    name="sum_agent",
    model=model,
    description="Takes in log data from T-Pot honey pots and summarises them, emailing summaries",
    instruction="""
    You are a data summarisation agent.
    
    When you receive log data you will parse through the files and generate a summarisation of the data,
    
    You can use the following tools:
    - get_current_date (use this tool returns the current date when the tool is ran.)
    - pull_data (use this to read the elastic log data into a file)
    - get_data (use this tool to return all the data saved to a file_path, file_path must be within the "./log_data/" folder)
    """,
    tools=[get_current_date, pull_data, get_data],
)
