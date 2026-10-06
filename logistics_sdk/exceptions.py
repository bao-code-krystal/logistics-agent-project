class DifyAPIError(Exception):
    """Dify API 调用异常基类"""
    pass

class DifyAuthError(DifyAPIError):
    """API Key 认证失败"""
    pass

class DifyTimeoutError(DifyAPIError):
    """API 调用超时"""
    pass