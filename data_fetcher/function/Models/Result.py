from typing import TypeVar, Generic
import logging

T = TypeVar('T')
E = TypeVar('E')

class Result(Generic[T, E]):
    """
    A generic class that represents the result of an operation that can either succeed with a value of type T,
    or fail with an error of type E.

    Attributes:
        value (T): The value of the result if it's ok.
        error (E): The error of the result if it's an error.
    """

    value: T | None
    error: E | None
    __create_key = object()     # quick clever way to ensure we're only creating result objects using the Ok or Err methods

    @classmethod
    def Ok(cls, value: T) -> 'Result':
        """
        Creates a new Result object that represents a successful result.

        Args:
            value (T): The value of the result.

        Returns:
            Result: A new Result object that represents a successful result. 
        """
        return cls(
            cls.__create_key, value = value
           )


    @classmethod
    def Err(cls, error: E) -> 'Result':
        """
        Creates a new Result object that represents an error.

        Args:
            error (E): The error of the result.
        
        Returns:
            Result: A new Result object that represents an error.
        """
        return cls(
            cls.__create_key, error = error
           )


    def __init__(self, create_key, value=None, error=None) -> None:
        assert(create_key == Result.__create_key, "Result objects must be created using the Result.ok() or Result.errmethod.")

        if value is not None:
            self.value = value
            self.error = None
        else:   
            self.value = None
            self.error = error


    def is_ok(self) -> bool:
        """
        Returns True if the result is ok, False otherwise.
        """
        return self.error is None


    def is_err(self) -> bool:
        """
        Returns True if the result is an error, False otherwise.
        """
        return self.error is not None


    def unwrap(self) -> T:
        """
        Returns the value of the result if it's ok, or raises an exception with the error if it's an error.
        """
        if self.is_ok():
            return self.value
        else:
            raise Exception(self.error)


    def unwrap_or(self, default: T) -> T:
        """
        Returns the value of the result if it's ok, or returns the default value if it's an error.

        Args:
            default (T): The default value to return if the result is an error.

        Returns:
            T: The value of the result if it's ok, or the default value if it's an error.
        """
        if self.is_ok():
            return self.value
        else:
            return default


    def map(self, func: callable) -> 'Result':
        """
        Applies the given function to the value of the result if it's ok, and returns a new Result object with the
        result of the function. If the result is an error, returns the original result object.

        Args:
            func (callable): The function to apply to the value of the result.

        Returns:
            Result: A new Result object with the result of the function if the result is ok, or the original result
            object if it's an error.
        """
        if self.is_ok():
            try:
                result = func(self.value)
                return result 
            except Exception as e:
                error_msg = e.args[0] if e.args else str(e) 
                return Result.Err(error_msg)
        else:
            return self


    def map_err(self, func: callable) -> 'Result':
        """
        Applies the given function to the error of the result if it's an error, and returns a new Result object with
        the result of the function. If the result is ok, returns the original result object.

        Args:
            func (callable): The function to apply to the error of the result.

        Returns:
            Result: A new Result object with the result of the function if the result is an error, or the original
            result object if it's ok.
        """
        if self.is_err():
            return Result(error=func(self.error))
        else:
            return self


    def __repr__(self) -> str:
        """
        Returns a string representation of the result object.

        Returns:
            str: A string representation of the result object.
        """
        if self.is_ok():
            return f"Ok({self.value})"
        else:
            return f"Err({self.error})"