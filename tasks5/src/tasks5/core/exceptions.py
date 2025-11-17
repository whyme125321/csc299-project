class TaskManagerError(Exception):
    """Base exception for the task manager domain."""
    pass


class InvalidDescriptionError(TaskManagerError):
    """Raised when a task description is invalid."""
    pass


class TaskNotFoundError(TaskManagerError):
    """Raised when a requested task cannot be found."""
    pass


class FileWriteError(TaskManagerError):
    """Raised when writing to storage fails."""
    pass


class FileReadError(TaskManagerError):
    """Raised when reading from storage fails."""
    pass


class CorruptedDataError(TaskManagerError):
    """Raised when persisted data is corrupted or invalid."""
    pass


class ConfigurationError(TaskManagerError):
    """Raised when configuration (paths, env) is invalid."""
    pass
