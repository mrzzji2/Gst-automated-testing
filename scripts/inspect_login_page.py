"""
Open browser and inspect login page
使用 Playwright 打开浏览器并检查登录页面
"""
import asyncio
from playwright.async_api import async_playwright


async def main():
    """主函数"""
    async with async_playwright() as p:
        # 启动 Chromium 浏览器（ headed 模式）
        browser = await p.chromium.launch(
            headless=False,
            slow_mo=1000  # 慢速模式，方便观察
        )

        # 创建浏览器上下文
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 720},
            locale='zh-CN'
        )

        # 创建新页面
        page = await context.new_page()

        # 导航到登录页面
        print("正在打开登录页面...")
        await page.goto("https://doc-online-test.gstyun.cn/webClinic/index.html#/home")

        # 等待页面加载
        await page.wait_for_load_state("networkidle", timeout=10000)

        print("页面已加载，请手动登录或按回车继续...")
        input("按 Enter 键继续...")

        # 截图保存
        await page.screenshot(path="screenshots/login_page_inspect.png", full_page=True)
        print("截图已保存到: screenshots/login_page_inspect.png")

        # 打印页面标题和URL
        print(f"页面标题: {await page.title()}")
        print(f"当前URL: {page.url}")

        # 尝试查找登录相关的元素
        print("\n正在查找登录页面元素...")

        # 查找所有输入框
        inputs = await page.query_selector_all("input")
        print(f"\n找到 {len(inputs)} 个输入框:")
        for i, input_elem in enumerate(inputs):
            placeholder = await input_elem.get_attribute("placeholder")
            input_type = await input_elem.get_attribute("type")
            input_id = await input_elem.get_attribute("id")
            input_name = await input_elem.get_attribute("name")
            print(f"  输入框 {i+1}: type={input_type}, placeholder={placeholder}, id={input_id}, name={input_name}")

        # 查找所有按钮
        buttons = await page.query_selector_all("button")
        print(f"\n找到 {len(buttons)} 个按钮:")
        for i, btn in enumerate(buttons):
            btn_text = await btn.inner_text()
            btn_type = await btn.get_attribute("type")
            btn_class = await btn.get_attribute("class")
            print(f"  按钮 {i+1}: text={btn_text[:30] if btn_text else 'N/A'}, type={btn_type}, class={btn_class}")

        # 保存页面 HTML
        html_content = await page.content()
        with open("screenshots/login_page.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("\n页面HTML已保存到: screenshots/login_page.html")

        # 保持浏览器打开，方便观察
        print("\n浏览器保持打开状态，按 Ctrl+C 或关闭浏览器窗口退出...")
        try:
            await page.wait_for_event("close", timeout=0)  # 无限等待
        except:
            pass

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
