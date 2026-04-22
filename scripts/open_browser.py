"""
Simple Browser Launcher
简单的浏览器启动脚本 - 让用户手动操作
"""
import asyncio
from playwright.async_api import async_playwright

async def open_browser():
    """打开浏览器供手动操作"""
    print("Opening browser for manual testing...")
    print("Please:")
    print("1. Login if needed")
    print("2. Navigate to online consultation")
    print("3. Select a patient")
    print("4. Type in input box")
    print("5. Click send")
    print("\nTell me what you see and what class names the elements have.")

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
        await page.goto("https://doc-online-test.gstyun.cn/webClinic/index.html#/home")

        print(f"\nURL: {page.url}")
        print("Browser ready! Please perform the operations.\n")

        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await browser.close()
            print("Done!")

asyncio.run(open_browser())