import asyncio
from playwright.async_api import async_playwright

async def main():
    """Launch Chrome with specific profile and navigate to a URL."""
    # Hardcoded values
    chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    profile_path = '/Users/chris/Library/Application Support/Google/Chrome/Profile 4'
    url = 'https://example.com'
    
    print(f"Launching Chrome from: {chrome_path}")
    print(f"Using profile from: {profile_path}")
    print("Note: Please ensure Chrome is closed before running this script")
    
    async with async_playwright() as p:
        # Launch browser with specific profile using launchPersistentContext
        browser_context = await p.chromium.launch_persistent_context(
            user_data_dir=profile_path,
            headless=False,
            channel="chrome",
            executable_path=chrome_path,
            # Add arguments to disable automation detection
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-default-browser-check"
            ],
            # Ignore default arguments that might trigger security warnings
            ignore_default_args=["--enable-automation", "--use-mock-keychain", "--password-store=basic", "--no-sandbox"]
        )
        
        # Get the first page from browser_context.pages()
        pages = browser_context.pages
        if pages and len(pages) > 0:
            page = pages[0]
        else:
            page = await browser_context.new_page()
            
        print(f"Navigating to: {url}")
        await page.goto(url)
        content = await page.content()
        print(content)
        
        # Keep the browser open until user decides to close it
        print("Browser is open. Press Enter to close the browser...")
        input()
        
        # Close the browser when user presses Enter
        await browser_context.close()
        print("Browser closed.")

if __name__ == "__main__":
    asyncio.run(main())