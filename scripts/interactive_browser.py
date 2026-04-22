"""
Interactive Browser Script
Opens browser with saved login state for manual testing
"""
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

# Storage state file path
STORAGE_STATE_FILE = Path(__file__).parent.parent / "tests" / "storage_state.json"
BASE_URL = "https://doc-online-test.gstyun.cn/webClinic"


async def interactive_browser():
    """Open browser with saved login state for manual interaction"""
    print("=" * 60)
    print("Interactive Browser - GST Online Consultation")
    print("=" * 60)
    print(f"[INFO] Loading login state from: {STORAGE_STATE_FILE}")

    if not STORAGE_STATE_FILE.exists():
        print("[ERROR] No saved login state found!")
        print("       Run: python scripts/generate_login_state.py")
        return

    async with async_playwright() as p:
        # Launch browser with saved state
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--start-maximized"]
        )

        # Create context with saved state
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            storage_state=str(STORAGE_STATE_FILE)
        )

        # Create page
        page = await context.new_page()
        page.set_default_timeout(30000)

        # Navigate to home page
        await page.goto(f"{BASE_URL}/index.html#/home")
        print(f"[OK] Navigated to: {page.url}")

        # Check if logged in
        await asyncio.sleep(2)
        if "#/login" in page.url:
            print("[WARN] Saved state may be expired. Please login manually.")
        else:
            print("[OK] Already logged in using saved state!")

        print("\n" + "=" * 60)
        print("Browser is ready for manual operation!")
        print("=" * 60)
        print("\nPlease perform the following steps:")
        print("1. Select a patient from the patient list")
        print("2. Click on any buttons/features you want to test")
        print("3. Tell me what you did, and I'll update the code")
        print("\nPress Ctrl+C to close the browser when done.")
        print("=" * 60 + "\n")

        # Wait indefinitely until user closes browser
        try:
            # Keep browser open
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n[INFO] Closing browser...")
            await browser.close()
            print("[OK] Done!")


if __name__ == "__main__":
    asyncio.run(interactive_browser())
