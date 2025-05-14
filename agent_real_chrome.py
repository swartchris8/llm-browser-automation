from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
import asyncio
from datetime import datetime
import json
import os

# Configure the browser to connect to your Chrome instance
# Sadly this still does not use my actual chrome profile, the solution is to just login to my Chrome profile this let's me run it
browser = Browser(
    config=BrowserConfig(
        # Specify the path to your Chrome executable
        browser_binary_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS path
        # For Windows, typically: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
        # For Linux, typically: '/usr/bin/google-chrome'
        
        # Use your existing Chrome profile
        # To check existing profile dir visit -- chrome://version/
        user_data_dir='/Users/chris/Library/Application Support/Google/Chrome/Profile 4',  # macOS path
        # For Windows, typically: os.path.join(home_dir, 'AppData/Local/Google/Chrome/User Data/Default')
        # For Linux, typically: os.path.join(home_dir, '.config/google-chrome/Default')
        
        # Additional options to help with profile loading and prevent automation detection
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-default-browser-check'
        ],
        headless=False,  # Set to False to see the browser window
        ignore_default_args=[
            '--enable-automation',
            '--use-mock-keychain',
            '--password-store=basic',
            '--no-sandbox'
        ],  # Disable automation flags and other security warnings
    )
)

llm=ChatOpenAI(model='gpt-4o-mini')

async def main():
    with get_openai_callback() as cb:
        agent = Agent(
            task="Visit gmail.com and print the last email received",
            llm=llm,
            browser=browser
        )
        history = await agent.run()
        
        # Get token usage information
        token_usage = {
            "total_tokens": cb.total_tokens,
            "prompt_tokens": cb.prompt_tokens,
            "completion_tokens": cb.completion_tokens,
            "total_cost_usd": cb.total_cost
        }
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create results directory if it doesn't exist
        os.makedirs("results", exist_ok=True)
        
        # Save history to file
        filename = f"results/task_history_{timestamp}.json"
        with open(filename, 'w') as f:
            f.write(history.model_dump_json())
        
        print(f"Result history saved to {filename}")
        
        # Save task results and token usage
        filename = f"results/task_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump({
                "task": agent.task, 
                "final_result": history.final_result(),
                "token_usage": token_usage
            }, f, indent=2)
        
        print(f"Task saved to {filename}")
        print("\nToken Usage Summary:")
        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")
        
        print("\nHistory:")
        print(history)

if __name__ == '__main__':
    asyncio.run(main())
