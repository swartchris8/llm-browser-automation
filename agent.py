from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
from datetime import datetime
import json
import os
load_dotenv()

import asyncio

llm = ChatOpenAI(model="gpt-4o")

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
    )
    result = await agent.run()
    
    # Create history data dictionary
    history_data = {
        "task": agent.task,
        "timestamp": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "urls": agent.history.urls(),
        "screenshots": agent.history.screenshots(),
        "action_names": agent.history.action_names(),
        "extracted_content": agent.history.extracted_content(),
        "errors": agent.history.errors(),
        "model_actions": agent.history.model_actions(),
        "final_result": agent.history.final_result()
    }
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Save to file
    filename = f"results/task_{history_data['timestamp']}.json"
    with open(filename, 'w') as f:
        json.dump(history_data, f, indent=2)
    
    print(f"Results saved to {filename}")
    print(result)

asyncio.run(main())
