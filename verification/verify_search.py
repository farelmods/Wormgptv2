import os
from playwright.sync_api import sync_playwright

def verify_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Get absolute path to index.html
        cwd = os.getcwd()
        file_path = f"file://{cwd}/index.html"

        print(f"Navigating to {file_path}")
        page.goto(file_path)

        # Login
        print("Logging in...")
        page.fill('#loginUsername', 'admin')
        page.fill('#loginPassword', 'admin')
        page.click('button.login-btn')

        # Wait for login to complete (toast appears)
        page.wait_for_selector('.toast.show', state='visible')
        print("Logged in.")

        # Inject some chat history for testing
        print("Injecting test data...")
        page.evaluate("""
            state.chatHistory.push({
                id: 12345,
                title: "Optimization Test Chat",
                messages: [{sender: 'user', content: 'This is a unique searchable string'}]
            });
            // We must rebuild index manually because we injected data directly
            buildSearchIndex();
        """)

        # Open Sidebar
        print("Opening sidebar...")
        page.click('.menu-btn')

        # Click Search
        print("Opening search panel...")
        page.click('text=Search chat')

        # Wait for modal
        page.wait_for_selector('#searchModal.active')

        # Type in search box
        print("Typing search query...")
        page.fill('#searchInput', 'unique searchable')

        # Wait for debounce (300ms) + a bit
        page.wait_for_timeout(600)

        # Verify result appears
        # Look for "Optimization Test Chat"
        if page.is_visible('text=Optimization Test Chat'):
            print("SUCCESS: Search result found!")
        else:
            print("FAILURE: Search result NOT found.")

        # Take screenshot
        output_path = "verification/search_result.png"
        page.screenshot(path=output_path)
        print(f"Screenshot saved to {output_path}")

        browser.close()

if __name__ == "__main__":
    verify_search()
