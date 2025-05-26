# exceptions.py

class AppBaseException(Exception):
    """应用内通用业务异常基类"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message

class UserNotFoundError(AppBaseException):
    """用户未找到"""
    pass

class InvalidPasswordError(AppBaseException):
    """密码错误"""
    pass

class UserAlreadyExistsError(AppBaseException):
    """用户名已存在"""
    pass

class MissingParameterError(AppBaseException):
    """缺少必要参数"""
    pass

class UserAlreadyDeactiveError(AppBaseException):
    """用户已退出活跃状态"""
    pass
