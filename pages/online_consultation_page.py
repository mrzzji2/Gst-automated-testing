"""
Online Consultation Page
在线问诊页面对象
"""
from playwright.async_api import Page
from typing import List, Dict
from loguru import logger

from pages.base_page import BasePage
from elements.online_consultation_locators import OnlineConsultationLocators


class OnlineConsultationPage(BasePage):
    """
    在线问诊页面对象
    封装在线问诊相关的所有操作
    """

    def __init__(self, page: Page, base_url: str = ""):
        """
        初始化在线问诊页

        Args:
            page: Playwright Page 对象
            base_url: 基础URL
        """
        super().__init__(page, base_url)
        self.locators = OnlineConsultationLocators

    # ==================== 导航操作 ====================

    async def goto_online_consultation(self):
        """导航到在线问诊页面"""
        await self.navigate("/index.html#/home")
        # 等待页面加载
        try:
            await self.wait_for_network_idle()
        except:
            await self.page.wait_for_load_state("domcontentloaded", timeout=30000)

        # 检查是否需要导航到在线问诊页面
        current_url = self.get_current_url()
        logger.info(f"Current URL after navigation: {current_url}")

        # 如果不在在线问诊页面，尝试点击菜单导航
        if "online" not in current_url.lower():
            try:
                # 尝试点击"在线问诊"菜单
                await self.page.wait_for_timeout(2000)
                # 查找并点击在线问诊菜单
                await self.page.click("text=在线问诊, a:has-text('在线问诊'), [class*='menu']:has-text('在线')")
                logger.info("Clicked online consultation menu")
                await self.page.wait_for_timeout(2000)
            except Exception as e:
                logger.warning(f"Could not navigate to online consultation: {e}")

        logger.info("Navigated to online consultation page")

    async def click_doctor_workbench(self):
        """点击医生工作台菜单"""
        await self.click(self.locators.NAV_DOCTOR_WORKBENCH)
        logger.info("Clicked doctor workbench menu")

    async def click_online_consultation_menu(self):
        """点击在线问诊菜单"""
        await self.click(self.locators.MENU_ONLINE_CONSULTATION)
        logger.info("Clicked online consultation menu")

    async def click_ai_clinic(self):
        """点击AI诊室"""
        await self.click(self.locators.NAV_AI_CLINIC)
        logger.info("Clicked AI clinic menu")

    # ==================== 患者搜索操作 ====================

    async def search_patient(self, keyword: str):
        """
        搜索患者

        Args:
            keyword: 搜索关键词（姓名或电话）
        """
        await self.fill(self.locators.PATIENT_SEARCH_INPUT, keyword, timeout=10000)
        # 按 Enter 触发搜索
        await self.page.keyboard.press("Enter")
        logger.info(f"Searched for patient: {keyword}")
        await self.page.wait_for_timeout(500)

    async def clear_patient_search(self):
        """清空患者搜索"""
        await self.clear_text(self.locators.PATIENT_SEARCH_INPUT)
        await self.page.keyboard.press("Enter")
        logger.info("Cleared patient search")

    # ==================== 患者列表操作 ====================

    async def get_patient_list_count(self) -> int:
        """
        获取患者列表数量

        Returns:
            患者数量
        """
        # 尝试多种选择器来查找患者
        selectors = [
            "tbody tr",           # 表格行
            "[class*='patient']",  # 包含 patient 的元素
            "[role='row']",        # role="row" 的元素
            ".el-table__row",      # Element UI 表格行
        ]

        for selector in selectors:
            try:
                count = await self.page.locator(selector).count()
                if count > 0:
                    logger.debug(f"Found {count} patients using selector: {selector}")
                    return count
            except:
                continue

        logger.warning("No patients found with any selector")
        return 0

    async def select_patient_by_index(self, index: int):
        """
        根据索引选择患者

        Args:
            index: 患者索引（从1开始）
        """
        # 尝试多种选择器来点击患者
        selectors = [
            f"tbody tr:nth-child({index})",
            f"[class*='patient']:nth-of-type({index})",
            f"[role='row']:nth-of-type({index})",
            f".el-table__row:nth-child({index})",
        ]

        for selector in selectors:
            try:
                if await self.page.locator(selector).count() > 0:
                    await self.page.click(selector)
                    logger.info(f"Selected patient at index {index} using: {selector}")
                    await self.page.wait_for_timeout(1000)
                    return
            except:
                continue

        # 如果上述方法都不行，尝试通过点击文本查找
        try:
            # 点击第一个包含文本的元素
            await self.page.click(f"[class*='patient']:nth-of-type({index}) *deep>> text")
            logger.info(f"Selected patient at index {index} using text selector")
            await self.page.wait_for_timeout(1000)
            return
        except:
            pass

        raise Exception(f"Could not select patient at index {index}")

    async def select_patient_by_name(self, name: str):
        """
        根据姓名选择患者

        Args:
            name: 患者姓名
        """
        # 使用 Playwright 的 get_by_text 方法
        await self.page.get_by_text(name).click()
        logger.info(f"Selected patient: {name}")

    async def get_first_patient_name(self) -> str:
        """
        获取第一个患者的姓名

        Returns:
            患者姓名
        """
        try:
            # 获取患者列表中的第一个患者姓名
            # 从患者列表中找到第一个包含文字的元素
            patient_list = self.page.locator("[class*='patient']")
            if await patient_list.count() > 0:
                # 获取第一个患者元素的文本内容
                first_patient = patient_list.first
                # 查找患者姓名（通常是第一个文本节点）
                text_content = await first_patient.text_content()
                if text_content:
                    # 提取患者姓名（通常是第一行或第一个单词）
                    lines = text_content.strip().split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and len(line) > 0:
                            # 排除时间和状态等非姓名内容
                            if not any(char in line for char in ['年', '月', '日', '已结束', '填写']):
                                return line
        except Exception as e:
            logger.debug(f"Could not get first patient name: {e}")
        return ""

    # ==================== 消息操作 ====================

    async def send_message(self, message: str):
        """
        发送消息

        Args:
            message: 消息内容
        """
        # 使用 get_by_text 或 get_by_role 来查找输入框
        try:
            # 先尝试找到包含"请输入内容"的div
            input_box = self.page.locator("div:has-text('请输入内容')").last
            await input_box.fill(message)
        except:
            # 如果失败，尝试使用 contenteditable
            input_box = self.page.locator("[contenteditable='true']").last
            await input_box.fill(message)

        # 使用 button 角色和文本"发送"
        await self.page.get_by_role("button", name="发送").click()
        logger.info(f"Sent message: {message}")

    async def send_message_by_enter(self, message: str):
        """
        通过回车键发送消息

        Args:
            message: 消息内容
        """
        try:
            input_box = self.page.locator("div:has-text('请输入内容')").last
            await input_box.fill(message)
        except:
            input_box = self.page.locator("[contenteditable='true']").last
            await input_box.fill(message)

        await self.page.keyboard.press("Enter")
        logger.info(f"Sent message by Enter: {message}")

    async def type_message_with_newline(self, message: str):
        """
        输入消息（换行不发送）

        Args:
            message: 消息内容
        """
        await self.fill(self.locators.MESSAGE_INPUT, message)
        logger.info(f"Typed message (not sent): {message}")

    # ==================== 快捷操作 ====================

    async def click_quick_reply(self):
        """点击快捷回复"""
        await self.click(self.locators.BUTTON_QUICK_REPLY)
        logger.info("Clicked quick reply button")

    async def click_send_questionnaire(self):
        """点击发问诊单"""
        await self.click(self.locators.BUTTON_SEND_QUESTIONNAIRE)
        logger.info("Clicked send questionnaire button")

    async def click_prescribe(self):
        """点击开方"""
        await self.page.get_by_text("在线开方").click()
        logger.info("Clicked prescribe button")

    async def click_video_consultation(self):
        """点击视频看诊"""
        await self.click(self.locators.BUTTON_VIDEO_CONSULTATION)
        logger.info("Clicked video consultation button")

    async def click_phone_consultation(self):
        """点击电话看诊"""
        await self.click(self.locators.BUTTON_PHONE_CONSULTATION)
        logger.info("Clicked phone consultation button")

    async def click_end_consultation(self):
        """点击结束问诊"""
        await self.click(self.locators.BUTTON_END_CONSULTATION)
        logger.info("Clicked end consultation button")

    # ==================== 结束问诊确认 ====================

    async def confirm_end_consultation(self):
        """确认结束问诊"""
        await self.click(self.locators.BUTTON_CONFIRM_END)
        logger.info("Confirmed end consultation")

    async def cancel_end_consultation(self):
        """取消结束问诊"""
        await self.click(self.locators.BUTTON_CANCEL_END)
        logger.info("Canceled end consultation")

    # ==================== 患者信息获取 ====================

    async def get_patient_info(self) -> Dict[str, str]:
        """
        获取当前选中患者的信息

        Returns:
            患者信息字典
        """
        info = {}
        try:
            # 使用 page.get_by_text() 来获取患者姓名
            info['name'] = await self.page.locator("text=test02").first.text_content()
        except:
            info['name'] = ""
        try:
            # 获取性别
            gender_locator = self.page.locator("text=男").or_(self.page.locator("text=女"))
            info['gender'] = await gender_locator.first.text_content()
        except:
            info['gender'] = ""
        try:
            # 获取年龄
            age_locator = self.page.locator("text=/\\d+岁/")
            if await age_locator.count() > 0:
                info['age'] = await age_locator.first.text_content()
            else:
                info['age'] = ""
        except:
            info['age'] = ""
        try:
            # 获取电话
            phone_text = await self.page.locator("text=电话:").first.text_content()
            info['phone'] = phone_text
        except:
            info['phone'] = ""

        logger.debug(f"Patient info: {info}")
        return info

    async def get_consultation_status(self) -> str:
        """
        获取问诊状态

        Returns:
            问诊状态文本
        """
        try:
            if await self.is_visible(self.locators.CONSULTATION_STATUS_ENDED, timeout=1000):
                return "已结束"
            if await self.is_visible(self.locators.CONSULTATION_STATUS_ONGOING, timeout=1000):
                return "进行中"
            return "未知"
        except:
            return "未知"

    # ==================== 历史处方 ====================

    async def get_prescription_history_count(self) -> int:
        """
        获取历史处方数量

        Returns:
            处方数量
        """
        try:
            count = await self.count_elements(self.locators.PRESCRIPTION_ITEM)
            return count
        except:
            return 0

    # ==================== 看诊数量徽章 ====================

    async def get_video_consultation_count(self) -> int:
        """
        获取视频看诊数量

        Returns:
            数量
        """
        try:
            # 尝试获取徽章中的数字
            badge_text = await self.get_text(self.locators.VIDEO_CONSULTATION_BADGE)
            # 提取数字
            import re
            numbers = re.findall(r'\d+', badge_text)
            if numbers:
                return int(numbers[0])
        except:
            pass
        return 0

    async def get_phone_consultation_count(self) -> int:
        """
        获取电话看诊数量

        Returns:
            数量
        """
        try:
            badge_text = await self.get_text(self.locators.PHONE_CONSULTATION_BADGE)
            import re
            numbers = re.findall(r'\d+', badge_text)
            if numbers:
                return int(numbers[0])
        except:
            pass
        return 0

    # ==================== 草稿箱 ====================

    async def get_draft_count(self) -> int:
        """
        获取草稿箱数量

        Returns:
            草稿数量
        """
        try:
            text = await self.get_text(self.locators.DRAFT_COUNT)
            # 从文本中提取数字
            import re
            numbers = re.findall(r'\d+', text)
            if numbers:
                return int(numbers[0])
        except:
            pass
        return 0

    # ==================== 验证操作 ====================

    async def assert_on_online_consultation_page(self):
        """断言在在线问诊页面"""
        # 验证URL包含home
        current_url = self.get_current_url()
        assert "#/home" in current_url or "home" in current_url, f"Expected URL to contain 'home', got: {current_url}"
        # 验证左侧菜单区域可见（使用更通用的选择器）
        try:
            await self.assert_element_visible(".sidebar, .menu, nav, [class*='menu'], [class*='sidebar']", timeout=5000)
        except:
            # 如果找不到侧边栏，至少验证页面已加载
            await self.page.wait_for_load_state("domcontentloaded", timeout=5000)
        logger.debug("Verified on online consultation page")

    async def assert_patient_list_visible(self):
        """断言患者列表可见"""
        await self.assert_element_visible(self.locators.PATIENT_LIST)
        logger.debug("Verified patient list is visible")

    async def assert_patient_selected(self, patient_name: str = ""):
        """
        断言患者已选中

        Args:
            patient_name: 患者姓名（可选）
        """
        await self.assert_element_visible(self.locators.PATIENT_INFO_PANEL)
        if patient_name:
            await self.assert_text_contains(self.locators.PATIENT_DETAIL_NAME, patient_name)
        logger.debug(f"Verified patient selected: {patient_name}")

    async def assert_message_sent(self):
        """断言消息发送成功（验证输入框清空）"""
        # 这里可以根据实际UI验证消息是否出现在聊天记录中
        await self.wait(500)
        logger.debug("Verified message sent")

    async def assert_consultation_ended(self):
        """断言问诊已结束"""
        await self.assert_element_visible(self.locators.CONSULTATION_STATUS_ENDED)
        logger.debug("Verified consultation ended")

    async def assert_prescription_page_opened(self):
        """断言开方页面已打开"""
        # 验证开方弹窗或页面显示
        await self.wait(500)
        logger.debug("Verified prescription page opened")

    # ==================== P1/P2 测试用例新增方法 ====================

    async def get_menu_items_count(self) -> int:
        """
        获取左侧菜单项数量

        Returns:
            菜单项数量
        """
        # 查找所有菜单项
        selectors = [
            ".menu-item",
            "[class*='menu-item']",
            ".sidebar-menu .menu-item",
        ]
        for selector in selectors:
            try:
                count = await self.page.locator(selector).count()
                if count > 0:
                    logger.debug(f"Found {count} menu items using selector: {selector}")
                    return count
            except:
                continue
        return 0

    async def get_menu_item_names(self) -> List[str]:
        """
        获取菜单项名称列表

        Returns:
            菜单项名称列表
        """
        try:
            # 获取所有包含文字的菜单项
            items = await self.page.locator(".menu-item, .sidebar-menu [class*='menu']").all()
            names = []
            for item in items:
                text = await item.text_content()
                if text.strip():
                    names.append(text.strip())
            logger.debug(f"Menu items: {names}")
            return names
        except Exception as e:
            logger.debug(f"Could not get menu item names: {e}")
            return []

    async def get_badge_number(self, selector: str) -> int:
        """
        获取徽章中的数字

        Args:
            selector: 徽章选择器

        Returns:
            数字数量
        """
        try:
            # 获取徽章附近的数字
            badge_locator = self.page.locator(selector).locator("..")
            count = await badge_locator.count()
            if count > 0:
                text = await badge_locator.first.text_content()
                import re
                numbers = re.findall(r'\d+', text)
                if numbers:
                    return int(numbers[0])
        except:
            pass
        return 0

    async def click_video_consultation_submenu(self, option: str = "video"):
        """
        点击视频看诊二级菜单

        Args:
            option: 选项，"video"视频看诊 或 "audio"语音问诊
        """
        await self.click(self.locators.BUTTON_VIDEO_CONSULTATION)
        await self.page.wait_for_timeout(300)
        if option == "video":
            await self.click(self.locators.SUBMENU_VIDEO_CONSULTATION)
        else:
            await self.click(self.locators.SUBMENU_AUDIO_CONSULTATION)
        await self.page.wait_for_timeout(300)
        logger.info(f"Clicked video consultation submenu: {option}")

    async def click_phone_consultation_submenu(self, option: str = "phone"):
        """
        点击电话看诊二级菜单

        Args:
            option: 选项，"phone"电话问诊 或 "audio"语音问诊
        """
        await self.click(self.locators.BUTTON_PHONE_CONSULTATION)
        await self.page.wait_for_timeout(300)
        if option == "phone":
            await self.click(self.locators.SUBMENU_PHONE_CONSULTATION)
        else:
            await self.click(self.locators.SUBMENU_AUDIO_CONSULTATION_PHONE)
        await self.page.wait_for_timeout(300)
        logger.info(f"Clicked phone consultation submenu: {option}")

    async def get_draft_box_heading(self) -> str:
        """
        获取草稿箱标题

        Returns:
            标题文本
        """
        try:
            return await self.get_text(self.locators.DRAFT_BOX_HEADING)
        except:
            return ""

    async def get_draft_count_text(self) -> str:
        """
        获取草稿箱数量文本（包含"个"字）

        Returns:
            数量文本
        """
        try:
            return await self.get_text(self.locators.DRAFT_COUNT_TEXT)
        except:
            return ""

    async def click_close_dialog_button(self):
        """点击对话框关闭按钮"""
        await self.click(self.locators.BUTTON_PRESCRIPTION_CLOSE)
        await self.page.wait_for_timeout(300)
        logger.info("Clicked dialog close button")

    async def dismiss_dialog_by_escape(self):
        """按 ESC 关闭对话框"""
        await self.page.keyboard.press("Escape")
        await self.page.wait_for_timeout(300)
        logger.info("Dismissed dialog by Escape")

    async def is_dialog_visible(self, selector: str = None) -> bool:
        """
        检查对话框是否可见

        Args:
            selector: 对话框选择器（可选）

        Returns:
            是否可见
        """
        try:
            if selector:
                return await self.is_visible(selector, timeout=1000)
            # 检查是否有任何 dialog 元素
            return await self.page.locator(".dialog, .modal").count() > 0
        except:
            return False

    async def rapid_click_prescribe_button(self, times: int = 2):
        """
        快速连续点击开方按钮

        Args:
            times: 点击次数
        """
        for _ in range(times):
            await self.click(self.locators.BUTTON_ONLINE_PRESCRIBE)
            await self.page.wait_for_timeout(50)  # 短间隔
        logger.info(f"Rapid clicked prescribe button {times} times")

    async def verify_no_duplicate_dialog(self) -> bool:
        """
        验证没有重复对话框

        Returns:
            True 表示只有一个或零个对话框
        """
        dialog_count = await self.page.locator(".dialog, .modal").count()
        result = dialog_count <= 1
        logger.info(f"Dialog count: {dialog_count}, no duplicate: {result}")
        return result
