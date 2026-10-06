import requests
from typing import Optional
from .exceptions import DifyAPIError, DifyAuthError, DifyTimeoutError

class LogisticsFreightAgent:
    """
    物流运费智能体 SDK 客户端
    封装对 Dify 官方 API 的调用，支持会话管理、错误处理和超时控制。
    """
    def __init__(self, api_key: str, base_url: str = "http://47.114.35.9/v1", timeout: int = 30):
        if not api_key:
            raise ValueError("API Key 不能为空")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")  # 去除尾部斜杠
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def chat(self, query: str, user_id: str = "sdk_user", conversation_id: Optional[str] = None) -> dict:
        """
        发送用户提问到物流 Agent，返回完整响应。
        :param query: 用户输入
        :param user_id: 用户唯一标识（用于 Dify 会话隔离）
        :param conversation_id: 可选，用于多轮对话续接
        :return: dict 包含 answer, conversation_id, message_id 等
        """
        url = f"{self.base_url}/chat-messages"
        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "user": user_id,
            "conversation_id": conversation_id or ""
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            raise DifyTimeoutError(f"Dify API 调用超时（{self.timeout}秒）")
        except requests.exceptions.RequestException as e:
            raise DifyAPIError(f"Dify API 请求失败: {str(e)}")

        if response.status_code == 401:
            raise DifyAuthError("API Key 无效或已过期")
        elif response.status_code != 200:
            raise DifyAPIError(f"Dify API 返回错误 [{response.status_code}]: {response.text}")

        return response.json()

    def calculate(self, query: str, user_id: str = "sdk_user") -> str:
        """
        便捷方法：直接返回 Agent 的回答文本
        """
        result = self.chat(query=query, user_id=user_id)
        return result.get("answer", "")