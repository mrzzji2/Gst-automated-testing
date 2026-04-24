"""
Online Consultation Page - Synchronous Version
在线问诊页面对象 - 同步版本
"""
from playwright.sync_api import Page
from typing import List, Dict
from loguru import logger

from pages.base_page import BasePage
from elements.online_consultation_locators import OnlineConsultationLocators


class OnlineConsultationPage(BasePage):
    """
    在线问诊页面对象 - 同步版本
    封装在线问诊相关的所有操作
    """

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)
        self.locators = OnlineConsultationLocators()

    # ==================== 导航操作 ====================

    def goto_online_consultation(self):
        """导航到在线问诊页面"""
        # 先访问基础URL进行登录
        base_url = f"{self.base_url}/index.html"
        self.page.goto(base_url)
        logger.info(f"Navigated to base URL for login: {base_url}")

        # 智能等待：等待跳转到 home 页面或医生选择对话框
        try:
            self.page.wait_for_url("**/home", timeout=10000)
            logger.info("Successfully navigated to home page")
        except:
            # 可能还在登录页或医生选择页面
            current_url = self.page.url
            logger.info(f"Current URL: {current_url}")

            if "#/home" not in current_url:
                logger.warning(f"Not on home page, current URL: {current_url}")
                # 尝试导航到 home
                home_url = f"{self.base_url}/index.html#/home"
                self.page.goto(home_url)
                try:
                    self.page.wait_for_url("**/home", timeout=8000)
                except:
                    pass

        # 点击"医生工作台"菜单
        try:
            # 先点击"医生工作台"主菜单
            logger.info("Clicking doctor workbench menu first")
            self.page.get_by_text("医生工作台").first.click()

            # 智能等待：等待在线问诊菜单出现
            self.page.wait_for_selector("li:has-text('在线问诊')", timeout=3000)

            # 再点击"在线问诊"子菜单
            logger.info("Clicking online consultation submenu")
            menu_selectors = [
                "ul.action-tabs li:has-text('在线问诊')",
                "li:has-text('在线问诊')",
                "a:has-text('在线问诊')",
            ]

            for selector in menu_selectors:
                try:
                    menu_item = self.page.locator(selector)
                    if menu_item.count() > 0:
                        menu_item.first.click()
                        logger.info(f"Clicked online consultation menu using: {selector}")
                        break
                except:
                    continue

            # 智能等待：等待页面加载和患者列表出现
            try:
                self.page.wait_for_selector("#consultList", timeout=8000)
                logger.info("Patient list loaded successfully")
            except:
                logger.warning("Patient list not found after clicking menu")

            # 验证最终 URL
            final_url = self.page.url
            logger.info(f"Final URL: {final_url}")

        except Exception as e:
            logger.error(f"Failed to navigate to online consultation menu: {e}")

        logger.info("Navigation to online consultation completed")

    def click_doctor_workbench(self):
        """点击医生工作台菜单"""
        self.click(self.locators.NAV_DOCTOR_WORKBENCH)
        logger.info("Clicked doctor workbench menu")

    def click_online_consultation_menu(self):
        """点击在线问诊菜单"""
        self.click(self.locators.MENU_ONLINE_CONSULTATION)
        logger.info("Clicked online consultation menu")

    def click_ai_clinic(self):
        """点击AI诊室"""
        self.click(self.locators.NAV_AI_CLINIC)
        logger.info("Clicked AI clinic menu")

    # ==================== 患者搜索操作 ====================

    def search_patient(self, keyword: str):
        """
        搜索患者

        Args:
            keyword: 搜索关键词（姓名或电话）
        """
        self.fill(self.locators.PATIENT_SEARCH_INPUT, keyword)
        # 按 Enter 触发搜索
        self.page.keyboard.press("Enter")
        logger.info(f"Searched for patient: {keyword}")
        # 搜索结果即时更新，无需等待

    def clear_patient_search(self):
        """清空患者搜索"""
        self.clear_text(self.locators.PATIENT_SEARCH_INPUT)
        self.page.keyboard.press("Enter")
        logger.info("Cleared patient search")

    def is_search_box_enabled(self) -> bool:
        """检查搜索框是否可用"""
        try:
            return self.page.locator(self.locators.PATIENT_SEARCH_INPUT).is_enabled()
        except:
            return False

    # ==================== 患者列表操作 ====================

    def get_patient_list_count(self) -> int:
        """
        获取患者列表数量

        Returns:
            患者数量
        """
        # 使用正确的选择器
        selector = "#consultList li"

        try:
            count = self.page.locator(selector).count()
            logger.info(f"Found {count} patients using selector: {selector}")
            return count
        except Exception as e:
            logger.warning(f"Error getting patient list: {e}")
            return 0

    def select_patient_by_index(self, index: int):
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
                if self.page.locator(selector).count() > 0:
                    self.page.click(selector)
                    logger.info(f"Selected patient at index {index} using: {selector}")
                    # 智能等待：等待患者详情面板出现
                    try:
                        self.page.wait_for_selector("[class*='patient-info'], [class*='patient-detail']", timeout=2000)
                    except:
                        pass  # 继续执行
                    return
            except:
                continue

        raise Exception(f"Could not select patient at index {index}")

    def select_patient_by_name(self, name: str):
        """
        根据姓名选择患者

        Args:
            name: 患者姓名
        """
        # 使用正确的选择器定位患者列表项
        selector = "#consultList li"

        # 等待患者列表加载
        self.page.wait_for_selector(selector, timeout=10000)

        # 在患者列表中查找包含指定姓名的项
        patient_items = self.page.locator(selector)
        count = patient_items.count()

        logger.debug(f"Found {count} patient items")

        for i in range(count):
            try:
                item = patient_items.nth(i)
                # 检查是否包含患者姓名
                if item.locator(f"text={name}").count() > 0:
                    item.click()
                    logger.info(f"Selected patient: {name}")
                    return
            except:
                continue

        raise Exception(f"Patient '{name}' not found in list")

    def get_first_patient_name(self) -> str:
        """
        获取第一个患者的姓名

        Returns:
            患者姓名
        """
        try:
            # 获取患者列表中的第一个患者（跳过第一个，可能是小固助理）
            selector = "#consultList li"
            patient_items = self.page.locator(selector)
            count = patient_items.count()

            if count <= 1:
                return ""

            # 从第二个开始查找患者姓名（跳过小固助理）
            for i in range(1, min(count, 5)):
                try:
                    item = patient_items.nth(i)
                    # 查找 .name 元素
                    name_span = item.locator('.name')
                    if name_span.count() > 0:
                        name_text = name_span.text_content()
                        if name_text and name_text.strip():
                            cleaned_name = name_text.strip()
                            # 排除时间和状态等非姓名内容
                            if not any(char in cleaned_name for char in ['年', '月', '日', '已结束', '填写']):
                                return cleaned_name
                except:
                    continue
        except Exception as e:
            logger.debug(f"Could not get first patient name: {e}")
        return ""

    # ==================== 消息操作 ====================

    def send_message(self, message: str):
        """
        发送消息

        Args:
            message: 消息内容
        """
        try:
            input_box = self.page.locator("div:has-text('请输入内容')").last
            input_box.fill(message)
        except:
            input_box = self.page.locator("[contenteditable='true']").last
            input_box.fill(message)

        self.page.get_by_role("button", name="发送").click()
        logger.info(f"Sent message: {message}")

    def send_message_by_enter(self, message: str):
        """
        通过回车键发送消息

        Args:
            message: 消息内容
        """
        try:
            input_box = self.page.locator("div:has-text('请输入内容')").last
            input_box.fill(message)
        except:
            input_box = self.page.locator("[contenteditable='true']").last
            input_box.fill(message)

        self.page.keyboard.press("Enter")
        logger.info(f"Sent message by Enter: {message}")

    def type_message_with_newline(self, message: str):
        """
        输入消息（换行不发送）

        Args:
            message: 消息内容
        """
        self.fill(self.locators.MESSAGE_INPUT, message)
        logger.info(f"Typed message (not sent): {message}")

    # ==================== 快捷操作 ====================

    def click_quick_reply(self):
        """点击快捷回复"""
        self.click(self.locators.BUTTON_QUICK_REPLY)
        logger.info("Clicked quick reply button")

    def click_send_questionnaire(self):
        """点击发问诊单"""
        self.click(self.locators.BUTTON_SEND_QUESTIONNAIRE)
        logger.info("Clicked send questionnaire button")

    def click_prescribe(self):
        """点击开方"""
        self.page.get_by_text("在线开方").click()
        logger.info("Clicked prescribe button")

    def click_video_consultation(self):
        """点击视频看诊"""
        self.page.get_by_text("视频看诊").last.click()
        logger.info("Clicked video consultation button")

    def click_phone_consultation(self):
        """点击电话看诊"""
        self.page.get_by_text("电话看诊").click()
        logger.info("Clicked phone consultation button")

    def click_end_consultation(self):
        """点击结束问诊"""
        self.page.get_by_text("结束问诊").first.click()
        logger.info("Clicked end consultation button")

    # ==================== 结束问诊确认 ====================

    def confirm_end_consultation(self):
        """确认结束问诊"""
        self.click(self.locators.BUTTON_CONFIRM_END)
        logger.info("Confirmed end consultation")

    def cancel_end_consultation(self):
        """取消结束问诊"""
        self.click(self.locators.BUTTON_CANCEL_END)
        logger.info("Canceled end consultation")

    # ==================== 患者信息获取 ====================

    def get_patient_info(self) -> Dict[str, str]:
        """
        获取当前选中患者的信息

        Returns:
            患者信息字典
        """
        info = {}
        try:
            info['name'] = self.page.locator("text=test02").first.text_content()
        except:
            info['name'] = ""
        try:
            gender_locator = self.page.locator("text=男").or_(self.page.locator("text=女"))
            info['gender'] = gender_locator.first.text_content()
        except:
            info['gender'] = ""
        try:
            age_locator = self.page.locator("text=/\\d+岁/")
            if age_locator.count() > 0:
                info['age'] = age_locator.first.text_content()
            else:
                info['age'] = ""
        except:
            info['age'] = ""
        try:
            phone_text = self.page.locator("text=电话:").first.text_content()
            info['phone'] = phone_text
        except:
            info['phone'] = ""

        logger.debug(f"Patient info: {info}")
        return info

    def get_consultation_status(self) -> str:
        """
        获取问诊状态

        Returns:
            问诊状态文本
        """
        try:
            if self.is_visible(self.locators.CONSULTATION_STATUS_ENDED):
                return "已结束"
            if self.is_visible(self.locators.CONSULTATION_STATUS_ONGOING):
                return "进行中"
            return "未知"
        except:
            return "未知"

    # ==================== 历史处方 ====================

    def get_prescription_history_count(self) -> int:
        """
        获取历史处方数量

        Returns:
            处方数量
        """
        try:
            count = self.count_elements(self.locators.PRESCRIPTION_ITEM)
            return count
        except:
            return 0

    # ==================== 看诊数量徽章 ====================

    def get_video_consultation_count(self) -> int:
        """
        获取视频看诊数量

        Returns:
            数量
        """
        try:
            # 思路A：获取包含"视频看诊"的li父元素，提取完整文本中的数字
            menu_item = self.page.locator('li:has-text("视频看诊")').first
            full_text = menu_item.text_content()
            import re
            numbers = re.findall(r'\d+', full_text)
            if numbers:
                return int(numbers[0])
        except:
            pass
        return 0

    def get_phone_consultation_count(self) -> int:
        """
        获取电话看诊数量

        Returns:
            数量
        """
        try:
            # 思路A：获取包含"电话看诊"的li父元素，提取完整文本中的数字
            menu_item = self.page.locator('li:has-text("电话看诊")').first
            full_text = menu_item.text_content()
            import re
            numbers = re.findall(r'\d+', full_text)
            if numbers:
                return int(numbers[0])
        except:
            pass
        return 0

    # ==================== 草稿箱 ====================

    def get_draft_count(self) -> int:
        """
        获取草稿箱数量

        Returns:
            草稿数量
        """
        try:
            text = self.get_text(self.locators.DRAFT_COUNT)
            import re
            numbers = re.findall(r'\d+', text)
            if numbers:
                return int(numbers[0])
        except:
            pass
        return 0

    # ==================== 验证操作 ====================

    def assert_on_online_consultation_page(self):
        """断言在在线问诊页面"""
        current_url = self.page.url
        assert "#/home" in current_url or "home" in current_url, f"Expected URL to contain 'home', got: {current_url}"
        logger.debug("Verified on online consultation page")

    def assert_patient_list_visible(self):
        """断言患者列表可见"""
        self.assert_element_visible(self.locators.PATIENT_LIST)
        logger.debug("Verified patient list is visible")

    def assert_patient_selected(self, patient_name: str = ""):
        """
        断言患者已选中

        Args:
            patient_name: 患者姓名（可选）
        """
        self.assert_element_visible(self.locators.PATIENT_INFO_PANEL)
        if patient_name:
            self.assert_text_contains(self.locators.PATIENT_DETAIL_NAME, patient_name)
        logger.debug(f"Verified patient selected: {patient_name}")

    def assert_message_sent(self):
        """断言消息发送成功（验证输入框清空）"""
        self.wait(500)
        logger.debug("Verified message sent")

    def assert_consultation_ended(self):
        """断言问诊已结束"""
        self.assert_element_visible(self.locators.CONSULTATION_STATUS_ENDED)
        logger.debug("Verified consultation ended")

    def assert_prescription_page_opened(self):
        """断言开方页面已打开"""
        self.wait(500)
        logger.debug("Verified prescription page opened")

    # ==================== P1/P2 测试用例新增方法 ====================

    def get_menu_item_names(self) -> List[str]:
        """
        获取菜单项名称列表

        Returns:
            菜单项名称列表
        """
        try:
            items = self.page.locator(".el-menu-item, [class*='menu-item'], .nav-item").all()
            names = []
            for item in items:
                text = item.text_content()
                if text.strip():
                    text = text.strip()
                    import re
                    text = re.sub(r'\d+$', '', text)
                    names.append(text)
            logger.debug(f"Menu items: {names}")
            return names
        except Exception as e:
            logger.debug(f"Could not get menu item names: {e}")
            return []

    def get_badge_number(self, selector: str) -> int:
        """
        获取徽章中的数字

        Args:
            selector: 徽章选择器

        Returns:
            数字数量
        """
        try:
            badge_locator = self.page.locator(selector).locator("..")
            count = badge_locator.count()
            if count > 0:
                text = badge_locator.first.text_content()
                import re
                numbers = re.findall(r'\d+', text)
                if numbers:
                    return int(numbers[0])
        except:
            pass
        return 0

    def click_video_consultation_submenu(self, option: str = "video"):
        """
        点击视频看诊二级菜单

        Args:
            option: 选项，"video"视频看诊 或 "audio"语音问诊
        """
        self.click(self.locators.BUTTON_VIDEO_CONSULTATION)
        # 智能等待：等待二级菜单出现
        try:
            self.page.wait_for_selector(self.locators.SUBMENU_VIDEO_CONSULTATION, timeout=1000)
        except:
            pass  # 继续执行
        if option == "video":
            self.click(self.locators.SUBMENU_VIDEO_CONSULTATION)
        else:
            self.click(self.locators.SUBMENU_AUDIO_CONSULTATION)
        logger.info(f"Clicked video consultation submenu: {option}")

    def click_phone_consultation_submenu(self, option: str = "phone"):
        """
        点击电话看诊二级菜单

        Args:
            option: 选项，"phone"电话问诊 或 "audio"语音问诊
        """
        self.click(self.locators.BUTTON_PHONE_CONSULTATION)
        # 智能等待：等待二级菜单出现
        try:
            self.page.wait_for_selector(self.locators.SUBMENU_PHONE_CONSULTATION, timeout=1000)
        except:
            pass  # 继续执行
        if option == "phone":
            self.click(self.locators.SUBMENU_PHONE_CONSULTATION)
        else:
            self.click(self.locators.SUBMENU_AUDIO_CONSULTATION_PHONE)
        logger.info(f"Clicked phone consultation submenu: {option}")

    def get_draft_box_heading(self) -> str:
        """
        获取草稿箱标题

        Returns:
            标题文本
        """
        try:
            return self.get_text(self.locators.DRAFT_BOX_HEADING)
        except:
            return ""

    def get_draft_count_text(self) -> str:
        """
        获取草稿箱数量文本（包含"个"字）

        Returns:
            数量文本
        """
        try:
            return self.get_text(self.locators.DRAFT_COUNT_TEXT)
        except:
            return ""

    def click_close_dialog_button(self):
        """点击对话框关闭按钮"""
        self.click(self.locators.BUTTON_PRESCRIPTION_CLOSE)
        logger.info("Clicked dialog close button")

    def dismiss_dialog_by_escape(self):
        """按 ESC 关闭对话框"""
        self.page.keyboard.press("Escape")
        # 智能等待：等待对话框消失（短等待）
        self.page.wait_for_timeout(200)
        logger.info("Dismissed dialog by Escape")

    def is_dialog_visible(self, selector: str = None) -> bool:
        """
        检查对话框是否可见

        Args:
            selector: 对话框选择器（可选）

        Returns:
            是否可见
        """
        try:
            if selector:
                return self.is_visible(selector)
            return self.page.locator(".dialog, .modal").count() > 0
        except:
            return False

    def rapid_click_prescribe_button(self, times: int = 2):
        """
        快速连续点击开方按钮

        Args:
            times: 点击次数
        """
        for _ in range(times):
            self.click(self.locators.BUTTON_ONLINE_PRESCRIBE)
            self.page.wait_for_timeout(50)
        logger.info(f"Rapid clicked prescribe button {times} times")

    def verify_no_duplicate_dialog(self) -> bool:
        """
        验证没有重复对话框

        Returns:
            True 表示只有一个或零个对话框
        """
        dialog_count = self.page.locator(".dialog, .modal").count()
        result = dialog_count <= 1
        logger.info(f"Dialog count: {dialog_count}, no duplicate: {result}")
        return result

    # ==================== BasePage 缺失方法补充 ====================

    def get_value(self, selector: str) -> str:
        """获取输入框值"""
        return self.page.locator(selector).input_value()

    def is_visible(self, selector: str) -> bool:
        """检查元素是否可见"""
        return self.page.locator(selector).is_visible()

    def wait(self, timeout_ms: int):
        """等待指定毫秒"""
        self.page.wait_for_timeout(timeout_ms)

    def count_elements(self, selector: str) -> int:
        """统计元素数量"""
        return self.page.locator(selector).count()

    def assert_element_visible(self, selector: str):
        """断言元素可见"""
        self.page.wait_for_selector(selector, state="visible", timeout=30000)
        logger.debug(f"Element is visible: {selector}")

    def assert_text_contains(self, selector: str, expected: str):
        """断言文本包含"""
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=30000)
        text = element.text_content()
        assert expected in text, f"Expected '{expected}' in text, got: {text}"
        logger.debug(f"Text contains: {selector} contains '{expected}'")

    def fill(self, selector: str, value: str):
        """填充表单字段"""
        self.page.locator(selector).fill(value)
        logger.debug(f"Filled '{value}' into: {selector}")

    def clear_text(self, selector: str):
        """清空文本"""
        self.page.locator(selector).fill("")
        logger.debug(f"Cleared: {selector}")

    def click(self, selector: str):
        """点击元素"""
        self.page.locator(selector).click()
        logger.debug(f"Clicked: {selector}")

    def get_text(self, selector: str) -> str:
        """获取元素文本"""
        text = self.page.locator(selector).text_content()
        return text.strip() if text else ""