from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
import asyncio
from datetime import datetime
import json
import os

# Configure the browser to connect to your Chrome instance
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # For Linux, typically: '/usr/bin/google-chrome'
    )
)

llm=ChatOpenAI(model='gpt-4o-mini')

async def main():
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
        browser=browser
    )
    history = await agent.run()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Save to file
    filename = f"results/task_history_{timestamp}.json"
    with open(filename, 'w') as f:
        f.write(history.model_dump_json())
    
    print(f"Result history saved to {filename}")
    
    filename = f"results/task_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump({"task": agent.task, "final_result": history.final_result()}, f)

    print(f"Task saved to {filename}")
    
    print(history)

if __name__ == '__main__':
    asyncio.run(main())
