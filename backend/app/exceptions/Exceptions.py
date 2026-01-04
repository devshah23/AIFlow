# Repository Errors

class RepositoryError(Exception):
    """Base class for all repository-level errors."""
    pass

class NotFoundError(RepositoryError):
    """Raised when the row does not exist."""
    pass

class DatabaseError(RepositoryError):
    """Raised for Postgres / Supabase / SQLAlchemy errors."""
    pass

class ValidationError(RepositoryError):
    """Raised when invalid fields or bad input data was passed."""
    pass




class WorkflowCycleException(Exception):
    """Raised when a cycle is detected in workflow nodes."""
    pass


class NotFoundException(Exception):
    """Raised when a requested resource is not found."""
    pass

class InvalidFileFormatException(Exception):
    """Raised when a file format is invalid or unsupported."""
    pass

class InvalidWorkflowException(Exception):
    """Raised when workflow does not pass the validation rules."""
    pass

class InvalidNodeConfigException(Exception):
    """Raised on running nodes with invalid data for processing."""
    pass