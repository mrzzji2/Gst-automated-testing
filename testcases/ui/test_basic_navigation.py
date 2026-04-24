import pytest
from pages.online_consultation_page import OnlineConsultationPage

class TestBasicNavigation:
    """基础导航测试"""
    
    def test_basic_navigation(self, gst_online_consultation_page: OnlineConsultationPage):
        """验证能成功导航到在线问诊页面"""
        assert "#/online-consultation" in gst_online_consultation_page.page.url
        print("✅ 基础导航测试通过！")