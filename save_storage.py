"""Save storage state for login"""
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to login page
        await page.goto('https://doc-online-test.gstyun.cn/webClinic/index.html#/login')

        # Login
        await page.fill('input[placeholder*="手机号"]', '18500629847')
        await page.fill('input[placeholder*="验证码"]', '123456')
        await page.click('button:has-text("登录")')

        # Wait for doctor selection dialog
        await page.wait_for_timeout(3000)

        # Check current URL
        print(f"Current URL: {page.url}")

        # Check if doctor selection dialog appears
        try:
            # Look for radio buttons
            radios = page.locator('input[type="radio"], [role="radio"]')
            radio_count = await radios.count()
            print(f"Found {radio_count} radio buttons")

            if radio_count > 0:
                # Try to click the first radio button
                await radios.first.click(force=True)
                await page.wait_for_timeout(500)

                # Click confirm button
                await page.click('button:has-text("确认"), button:has-text("确认切换")')
            else:
                print("No radio buttons found, dialog might not have appeared")
        except Exception as e:
            print(f"Doctor selection error: {e}")
            print("Continuing...")

        # Wait for page load
        await page.wait_for_timeout(3000)

        # Save storage state
        await context.storage_state(path='d:/work/gst/tests/storage_state.json')

        print('Storage state saved successfully')
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())