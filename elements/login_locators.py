"""
Login Page Locators
登录页元素定位器
"""


class LoginLocators:
    """登录页元素定位器"""

    # 页面标题
    PAGE_TITLE = "h1:has-text('Login'), h1:has-text('Sign In')"

    # 表单容器
    LOGIN_FORM = "#login-form, form[action*='login']"

    # 输入框
    USERNAME_INPUT = "#username, input[name='username'], input[type='email']"
    PASSWORD_INPUT = "#password, input[name='password'], input[type='password']"

    # 按钮
    LOGIN_BUTTON = "button[type='submit'], #login-button, button:has-text('Login'), button:has-text('Sign In')"
    REMEMBER_ME_CHECKBOX = "#remember-me, input[name='remember']"
    FORGOT_PASSWORD_LINK = "a[href*='forgot'], a:has-text('Forgot')"

    # 第三方登录
    GOOGLE_LOGIN_BUTTON = "button:has-text('Google'), .google-login"
    GITHUB_LOGIN_BUTTON = "button:has-text('GitHub'), .github-login"

    # 注册链接
    REGISTER_LINK = "a[href*='register'], a[href*='signup'], a:has-text('Sign Up')"

    # 错误消息
    ERROR_MESSAGE = ".error-message, .alert-danger, [role='alert']"

    # Logo
    LOGO = ".logo, img[alt*='logo' i]"

    # 页脚链接
    TERMS_OF_SERVICE = "a[href*='terms']"
    PRIVACY_POLICY = "a[href*='privacy']"

    # 返回首页
    BACK_TO_HOME = "a[href='/'], a:has-text('Home')"
