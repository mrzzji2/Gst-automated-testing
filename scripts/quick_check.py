"""
Quick Element Checker
快速检查页面元素
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def check_elements():
    STORAGE_STATE_FILE = Path(__file__).parent.parent / "tests" / "storage_state.json"
    BASE_URL = "https://doc-online-test.gstyun.cn/webClinic"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="chrome")
        context = await browser.new_context(storage_state=str(STORAGE_STATE_FILE))
        page = await context.new_page()

        await page.goto(f"{BASE_URL}/index.html#/home")
        await asyncio.sleep(3)

        print(f"Current URL: {page.url}")
        print("\n=== Patient List ===")
        print("Trying selectors:")
        for sel in [".patient-item", "[class*='patient']", "tr[class*='table']"]:
            cnt = await page.locator(sel).count()
            print(f"  {sel}: {cnt} elements")

        print("\n=== Input Box ===")
        for sel in ["textarea", "input[type='text']", "[contenteditable='true']"]:
            cnt = await page.locator(sel).count()
            print(f"  {sel}: {cnt} elements")

        print("\n=== Send Button ===")
        for sel in ["button:has-text('发送')", "[class*='send']"]:
            cnt = await page.locator(sel).count()
            print(f"  {sel}: {cnt} elements")

        print("\nPress Ctrl+C to exit...")
        try:
            while True:
                await asyncio.sleep(1)
        except:
            pass
        await browser.close()

asyncio.run(check_elements())
