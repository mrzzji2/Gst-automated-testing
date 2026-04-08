"""
API Utilities
API请求工具（可选）
"""
import requests
from typing import Optional, Dict, Any, Union
from loguru import logger


class APIUtils:
    """
    API请求工具类
    支持 RESTful API 调用
    """

    def __init__(
        self,
        base_url: str = "",
        headers: Optional[Dict[str, str]] = None,
        timeout: int = 30000,
        verify_ssl: bool = True
    ):
        """
        初始化API工具

        Args:
            base_url: API基础URL
            headers: 默认请求头
            timeout: 超时时间（毫秒）
            verify_ssl: 是否验证SSL
        """
        self.base_url = base_url.rstrip("/")
        self.headers = headers or {}
        self.timeout = timeout / 1000  # 转换为秒
        self.verify_ssl = verify_ssl
        self.session = requests.Session()

    def _full_url(self, endpoint: str) -> str:
        """获取完整URL"""
        endpoint = endpoint.lstrip("/")
        return f"{self.base_url}/{endpoint}" if self.base_url else endpoint

    def _log_response(self, response: requests.Response, method: str, url: str):
        """记录响应信息"""
        logger.debug(f"{method} {url} - Status: {response.status_code}")

    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        GET 请求

        Args:
            endpoint: 接口端点
            params: 查询参数
            headers: 请求头

        Returns:
            响应对象
        """
        url = self._full_url(endpoint)
        req_headers = {**self.headers, **(headers or {})}

        try:
            response = self.session.get(
                url,
                params=params,
                headers=req_headers,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            self._log_response(response, "GET", url)
            return response
        except Exception as e:
            logger.error(f"GET request failed: {url} - {e}")
            raise

    def post(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        POST 请求

        Args:
            endpoint: 接口端点
            data: 表单数据
            json: JSON数据
            headers: 请求头

        Returns:
            响应对象
        """
        url = self._full_url(endpoint)
        req_headers = {**self.headers, **(headers or {})}

        try:
            response = self.session.post(
                url,
                data=data,
                json=json,
                headers=req_headers,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            self._log_response(response, "POST", url)
            return response
        except Exception as e:
            logger.error(f"POST request failed: {url} - {e}")
            raise

    def put(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        PUT 请求

        Args:
            endpoint: 接口端点
            data: 表单数据
            json: JSON数据
            headers: 请求头

        Returns:
            响应对象
        """
        url = self._full_url(endpoint)
        req_headers = {**self.headers, **(headers or {})}

        try:
            response = self.session.put(
                url,
                data=data,
                json=json,
                headers=req_headers,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            self._log_response(response, "PUT", url)
            return response
        except Exception as e:
            logger.error(f"PUT request failed: {url} - {e}")
            raise

    def delete(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        DELETE 请求

        Args:
            endpoint: 接口端点
            params: 查询参数
            headers: 请求头

        Returns:
            响应对象
        """
        url = self._full_url(endpoint)
        req_headers = {**self.headers, **(headers or {})}

        try:
            response = self.session.delete(
                url,
                params=params,
                headers=req_headers,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            self._log_response(response, "DELETE", url)
            return response
        except Exception as e:
            logger.error(f"DELETE request failed: {url} - {e}")
            raise

    def patch(
        self,
        endpoint: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> requests.Response:
        """
        PATCH 请求

        Args:
            endpoint: 接口端点
            data: 表单数据
            json: JSON数据
            headers: 请求头

        Returns:
            响应对象
        """
        url = self._full_url(endpoint)
        req_headers = {**self.headers, **(headers or {})}

        try:
            response = self.session.patch(
                url,
                data=data,
                json=json,
                headers=req_headers,
                timeout=self.timeout,
                verify=self.verify_ssl
            )
            self._log_response(response, "PATCH", url)
            return response
        except Exception as e:
            logger.error(f"PATCH request failed: {url} - {e}")
            raise

    def set_auth(self, auth_type: str, **kwargs):
        """
        设置认证

        Args:
            auth_type: 认证类型 (bearer, basic, api_key)
            **kwargs: 认证参数
        """
        if auth_type == "bearer":
            token = kwargs.get("token")
            self.headers["Authorization"] = f"Bearer {token}"
        elif auth_type == "basic":
            username = kwargs.get("username")
            password = kwargs.get("password")
            self.session.auth = (username, password)
        elif auth_type == "api_key":
            key = kwargs.get("key")
            header_name = kwargs.get("header", "X-API-Key")
            self.headers[header_name] = key

    def set_header(self, key: str, value: str):
        """设置请求头"""
        self.headers[key] = value

    def close(self):
        """关闭会话"""
        self.session.close()


# 全局实例
api_utils = None

def get_api_utils(config: Dict[str, Any]) -> APIUtils:
    """
    获取API工具实例

    Args:
        config: API配置

    Returns:
        APIUtils 实例
    """
    global api_utils
    if api_utils is None:
        api_utils = APIUtils(
            base_url=config.get("base_url", ""),
            headers=config.get("headers", {}),
            timeout=config.get("timeout", 30000),
            verify_ssl=config.get("verify_ssl", True)
        )
    return api_utils


__all__ = ["APIUtils", "get_api_utils"]
