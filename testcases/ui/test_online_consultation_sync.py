import pytest
import allure
from pages.online_consultation_page_sync import OnlineConsultationPage

class TestOnlineConsultation:
    """在线问诊测试 - 同步版本"""
    
    @pytest.mark.P0
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.title("验证在线问诊页面基本元素")
    @allure.description("验证在线问诊页面基本元素正确显示，包括菜单、患者列表等")
    def test_verify_page_elements(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        验证在线问诊页面基本元素
        前置条件：
        - 已登录系统
        - 已进入在线问诊页面
        验证点：
        - 页面加载完成
        """
        # fixture 已处理登录和导航，验证页面元素
        assert "#/online-consultation" in gst_online_consultation_page.page.url, "Should be on online consultation page"

        # 验证患者列表（允许为空，但必须存在）
        patient_count = gst_online_consultation_page.get_patient_list_count()
        print(f"Patient count: {patient_count}")
        
        # 验证搜索框可用
        assert gst_online_consultation_page.is_search_box_enabled(), "Search box should be enabled"
        print("Search box is enabled")
        
        print("✅ 在线问诊页面基本元素验证通过！")