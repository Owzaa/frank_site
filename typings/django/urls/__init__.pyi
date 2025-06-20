from typing import Any, Callable, List, Optional, Pattern, Sequence, Tuple, Union, overload

# Type definitions for django.urls
# These are stub type definitions to help with type checking

class ResolverMatch:
    func: Callable
    args: Tuple
    kwargs: dict
    url_name: Optional[str]
    app_names: List[str]
    app_name: str
    namespace: str
    namespaces: List[str]
    view_name: str

def resolve(path: str, urlconf: Any = None) -> ResolverMatch: ...

def reverse(
    viewname: str,
    urlconf: Any = None,
    args: Any = None,
    kwargs: Any = None,
    current_app: Any = None,
) -> str: ...

def reverse_lazy(
    viewname: str,
    urlconf: Any = None,
    args: Any = None,
    kwargs: Any = None,
    current_app: Any = None,
) -> str: ...

def clear_url_caches() -> None: ...

def set_script_prefix(prefix: str) -> None: ...

def get_script_prefix() -> str: ...

def clear_script_prefix() -> None: ...

def set_urlconf(urlconf_name: Any) -> None: ...

def get_urlconf(default: Any = None) -> Any: ...

def is_valid_path(path: str, urlconf: Any = None) -> bool: ...

def translate_url(url: str, lang_code: str) -> str: ...

# path and re_path functions
def path(
    route: str,
    view: Union[Callable, str],
    kwargs: dict = None,
    name: str = None,
) -> Any: ...

def re_path(
    route: Union[str, Pattern],
    view: Union[Callable, str],
    kwargs: dict = None,
    name: str = None,
) -> Any: ...

# URL resolver and pattern functions
def include(
    arg: Any,
    namespace: str = None,
    app_name: str = None,
) -> Tuple[Any, Optional[str], Optional[str]]: ...

# URL converters
class URLPattern:
    pattern: Any
    callback: Any
    default_args: dict
    name: str

class URLResolver:
    urlconf_name: Any
    app_name: Optional[str]
    namespace: Optional[str]
    pattern: Any
