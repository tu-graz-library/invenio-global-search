# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 Graz University of Technology.
#
# invenio-global-search is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Global Search wrappers and stubs."""

from functools import wraps
from typing import Callable
from warnings import warn

from flask_resources import MarshmallowSerializer


class BaseGlobalSearchSerializer(MarshmallowSerializer):
    """Extend MarshmallowSerializer with a no_op flag.

    Used for correctly handling missing imports.
    """

    def __init__(self, *, no_op: bool = False, **kwargs: dict) -> None:
        """Construct."""
        self._no_op = no_op
        super().__init__(**kwargs)

    @property
    def no_op(self) -> bool:
        """No op."""
        return self._no_op


class NoOpSchema:
    """Stub schema for dealing with missing imports."""

    def __init__(self) -> None:
        """Construct."""


def require_package[T](serializer_cls: type[BaseGlobalSearchSerializer]) -> Callable:
    """Require package."""

    def decorator(func: Callable[..., T]) -> Callable:
        """Decorate."""

        @wraps(func)
        def wrapper() -> T | None:
            if serializer_cls().no_op:
                msg = f"the global search serializers are misconfigured, the package for the serializer: {serializer_cls} hasn't been installed"
                warn(msg, stacklevel=2)
                return None
            return func()

        return wrapper

    return decorator
