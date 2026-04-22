"""
Debug Patient List Structure
调试患者列表结构
"""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def debug_patient_list():
    STORAGE_STATE_FILE = Path(__file__).parent.parent / "tests" / "storage_state.json"
    BASE_URL = "https://doc-online-test.gstyun.cn/webClinic"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="chrome")
        context = await browser.new_context(storage_state=str(STORAGE_STATE_FILE))
        page = await context.new_page()

        await page.goto(f"{BASE_URL}/index.html#/home")
        await asyncio.sleep(3)

        print(f"Current URL: {page.url}")

        # 获取所有可能的患者相关元素
        print("\n=== All elements with 'patient' in class ===")
        patient_elements = await page.locator("[class*='patient']").all()
        for i, elem in enumerate(patient_elements[:20]):  # 只显示前20个
            try:
                class_name = await elem.get_attribute("class")
                text = await elem.text_content()
                tag = await elem.evaluate("el => el.tagName")
                print(f"{i+1}. <{tag}> class='{class_name}' text='{text[:50] if text else ''}'")
            except:
                pass

        print("\n=== All table rows ===")
        rows = await page.locator("tr").all()
        print(f"Found {len(rows)} table rows")

        # 显示前3行的详细信息
        for i, row in enumerate(rows[:3]):
            try:
                text = await row.text_content()
                print(f"\nRow {i+1}: {text[:100]}")
            except:
                pass

        print("\n=== Looking for clickable elements ===")
        # 查找所有可点击的元素
        clickables = await page.locator("[onclick], [class*='click'], [role='button']").all()
        print(f"Found {len(clickables)} clickable elements")

        print("\n=== Page HTML structure (first 2000 chars) ===")
        html = await page.content()
        print(html[:2000])

        print("\nPress Ctrl+C to exit...")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        await browser.close()

asyncio.run(debug_patient_list())
