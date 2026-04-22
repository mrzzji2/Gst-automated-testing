"""
Debug Page Elements
Script to inspect and record page elements
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

STORAGE_STATE_FILE = Path(__file__).parent.parent / "tests" / "storage_state.json"
BASE_URL = "https://doc-online-test.gstyun.cn/webClinic"


async def inspect_elements():
    """Inspect page elements and print selectors"""
    print("=" * 60)
    print("Page Elements Inspector")
    print("=" * 60)

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--start-maximized"]
        )

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            storage_state=str(STORAGE_STATE_FILE)
        )

        page = await context.new_page()
        page.set_default_timeout(30000)

        # Navigate to home
        await page.goto(f"{BASE_URL}/index.html#/home")
        print(f"\n[INFO] Navigated to: {page.url}")

        await asyncio.sleep(3)

        if "#/login" in page.url:
            print("[ERROR] Not logged in!")
            await browser.close()
            return

        print("[OK] Logged in successfully!")

        # Inspect patient list
        print("\n" + "=" * 60)
        print("INSPECTING PATIENT LIST")
        print("=" * 60)

        # Try different selectors for patient list
        selectors_to_try = [
            ".patient-item",
            "[class*='patient']",
            "[class*='Patient']",
            ".el-table__row",
            "tr[class*='el-table']",
            "[role='row']",
        ]

        for selector in selectors_to_try:
            try:
                count = await page.locator(selector).count()
                if count > 0:
                    print(f"\n✓ Found {count} elements with: {selector}")

                    # Get first element details
                    first = page.locator(selector).first
                    text = await first.text_content()
                    print(f"  First element text: {text[:100] if text else 'N/A'}")

                    # Get HTML
                    html = await first.inner_html()
                    print(f"  HTML snippet: {html[:200] if html else 'N/A'}...")
            except:
                pass

        # Inspect input box
        print("\n" + "=" * 60)
        print("INSPECTING INPUT BOX")
        print("=" * 60)

        input_selectors = [
            "textarea",
            "input[type='text']",
            "[contenteditable='true']",
            "[class*='input']",
            "[placeholder*='输入']",
            "[placeholder*='消息']",
        ]

        for selector in input_selectors:
            try:
                count = await page.locator(selector).count()
                if count > 0:
                    print(f"\n✓ Found {count} elements with: {selector}")
            except:
                pass

        # Inspect send button
        print("\n" + "=" * 60)
        print("INSPECTING SEND BUTTON")
        print("=" * 60)

        button_selectors = [
            "button:has-text('发送')",
            "button[class*='send']",
            "button[class*='Send']",
            "[class*='send-btn']",
            "i[class*='send']",
            "svg[class*='send']",
        ]

        for selector in button_selectors:
            try:
                count = await page.locator(selector).count()
                if count > 0:
                    print(f"\n✓ Found {count} elements with: {selector}")
            except:
                pass

        print("\n" + "=" * 60)
        print("Please now manually:")
        print("1. Select a patient")
        print("2. Type in the input box")
        print("3. Click send")
        print("4. Tell me what happened")
        print("=" * 60)

        # Keep browser open
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await browser.close()
            print("\n[OK] Done!")


if __name__ == "__main__":
    asyncio.run(inspect_elements())
