import traceback
from typing import Optional


class AppException(Exception):
    def __init__(
        self,
        message: str,
        *,
        error_code: str = "APP_ERROR",
        module: Optional[str] = None,
        function: Optional[str] = None,
        file_name: Optional[str] = None,
        line_number: Optional[int] = None,
        original_error: Optional[Exception] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.module = module
        self.function = function
        self.file_name = file_name
        self.line_number = line_number
        self.original_error = original_error
        self.traceback_details = traceback.format_exc()

        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "error_code": self.error_code,
            "message": self.message,
            "module": self.module,
            "function": self.function,
            "file_name": self.file_name,
            "line_number": self.line_number,
            "original_error": str(self.original_error) if self.original_error else None,
            "traceback": self.traceback_details,
        }

    def __str__(self) -> str:
        return (
            f"{self.error_code}: {self.message} "
            f"[module={self.module}, function={self.function}, "
            f"file={self.file_name}, line={self.line_number}] "
            f"| original_error={self.original_error}"
        )


class ConfigurationException(AppException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="CONFIG_ERROR", **kwargs)


class IngestionException(AppException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="INGESTION_ERROR", **kwargs)


class RetrieverException(AppException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="RETRIEVER_ERROR", **kwargs)


class LLMException(AppException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="LLM_ERROR", **kwargs)


class RAGException(AppException):
    def __init__(self, message: str, **kwargs):
        super().__init__(message, error_code="RAG_ERROR", **kwargs)