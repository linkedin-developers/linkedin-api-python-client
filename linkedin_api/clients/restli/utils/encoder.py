from typing import Optional, List, Dict, Any, Union
from urllib.parse import quote

def param_encode(raw_query_params_map: Optional[Dict[str,Any]]) -> str:
  if raw_query_params_map is None:
    return ''

  query_params_map = _encode_query_param_map(raw_query_params_map)
  return '&'.join([f'{key}={query_params_map[key]}' for key in sorted(query_params_map.keys())])

def _encode_query_param_map(raw_query_params_map: Dict[str,Any]) -> dict:
  return { _encode_string(k): encode(v) for (k,v) in raw_query_params_map.items()}

def _encode_string(value: str) -> str:
  return quote(value, safe='')

def _encode_list(value: List[Any]) -> str:
  return f"List({','.join(encode(el) for el in value)})"

def _encode_dict(value: Dict[str, Any]) -> str:
  key_values = ",".join(f"{encode(k)}:{encode(v)}" for (k, v) in sorted(value.items()))

  return f'({key_values})'

def encode(value: Union[bool, str, int, List, Dict]) -> str:
  if value is None:
    return ""
  elif isinstance(value, bool):
    return "true" if value else "false"
  elif isinstance(value, str):
    return _encode_string(value)
  elif isinstance(value, list):
    return _encode_list(value)
  elif isinstance(value, dict):
    return _encode_dict(value)
  else:
    return str(value)
