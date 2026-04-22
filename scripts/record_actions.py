"""
Record User Actions
记录用户操作的脚本，用于获取正确的元素选择器
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def record_actions():
    """打开浏览器让用户手动操作，然后记录选择器"""
    print("=" * 60)
    print("Patient Selection Element Recorder")
    print("=" * 60)
    print("\nPlease perform these steps:")
    print("1. Login if needed")
    print("2. Navigate to online consultation page")
    print("3. Select a patient")
    print("4. Tell me when done, and I'll inspect the page")
    print("\nScript is now in observation mode...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--start-maximized"]
        )

        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN"
        )

        page = await context.new_page()
        page.set_default_timeout(30000)

        # Start at login page
        await page.goto("https://doc-online-test.gstyun.cn/webClinic/index.html#/home")

        print("\n[OK] Browser ready!")
        print("URL:", page.url)
        print("\n" + "=" * 60)
        print("Please perform the operations manually.")
        print("When you have selected a patient,")
        print("I will automatically inspect the page elements.")
        print("=" * 60)

        # Wait for user to complete operations
        try:
            # Monitor page for activity
            last_url = page.url
            print("\n[INFO] Monitoring page...")

            for i in range(300):  # 5 minutes max
                await asyncio.sleep(1)

                # Check for URL changes
                current_url = page.url
                if current_url != last_url:
                    print(f"[INFO] URL changed: {current_url}")
                    last_url = current_url

                # Every 10 seconds, show current status
                if i > 0 and i % 10 == 0:
                    print(f"[INFO] Running... ({i}s)")

        except KeyboardInterrupt:
            print("\n[INFO] User interrupted, inspecting page...")

        # Inspect page after user operations
        print("\n" + "=" * 60)
        print("PAGE INSPECTION")
        print("=" * 60)

        print(f"\nFinal URL: {page.url}")

        # Get page title
        title = await page.title()
        print(f"Page Title: {title}")

        # Look for common patient list patterns
        print("\n=== Looking for patient elements ===")

        # Try various selectors
        selectors = [
            # Table rows
            "tr.el-table__row",
            ".el-table__body tr",
            "table tbody tr",

            # Card items
            ".patient-card",
            ".card-item",
            "[class*='patient']",

            # List items
            "li",
            ".list-item",
            "[role='listitem']",

            # Any clickable element that might be a patient
            "[class*='clickable']",
            "[role='button']",
        ]

        found_selectors = []
        for selector in selectors:
            try:
                count = await page.locator(selector).count()
                if count > 0:
                    found_selectors.append((selector, count))
                    print(f"\n  {selector}: {count} elements")

                    # Get details for first few elements
                    for idx in range(min(3, count)):
                        elem = page.locator(selector).nth(idx)
                        try:
                            text = await elem.text_content()
                            if text and text.strip():
                                print(f"    [{idx}] {text.strip()[:100]}")
                        except:
                            pass
            except:
                pass

        # Look for input elements
        print("\n=== Looking for input elements ===")
        input_selectors = [
            "textarea",
            "input[type='text']",
            "[contenteditable='true']",
            "input:not([type])",
        ]

        for selector in input_selectors:
            try:
                count = await page.locator(selector).count()
                if count > 0:
                    print(f"\n  {selector}: {count} elements")
            except:
                pass

        # Look for send button
        print("\n=== Looking for send button ===")
        send_selectors = [
            "button:has-text('发送')",
            "button[class*='send']",
            "[class*='send-btn']",
            "i[class*='send']",
        ]

        for selector in send_selectors:
            try:
                count = await page.locator(selector).count()
                if count > 0:
                    print(f"\n  {selector}: {count} elements")
            except:
                pass

        # Save findings to file
        output_file = Path(__file__).parent.parent / "tests" / "page_inspection.txt"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("Page Inspection Results\n")
            f.write("=" * 60 + "\n")
            f.write(f"Final URL: {page.url}\n")
            f.write(f"Page Title: {title}\n\n")
            f.write("Patient Elements:\n")
            for selector, count in found_selectors:
                f.write(f"  {selector}: {count} elements\n")

        print(f"\n[OK] Inspection saved to: {output_file}")

        print("\n" + "=" * 60)
        print("Close the browser to exit...")
        print("=" * 60)

        # Wait until browser closed
        await browser.wait_for_event("close")

        print("[OK] Done!")


if __name__ == "__main__":
    asyncio.run(record_actions())