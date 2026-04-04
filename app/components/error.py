from __future__ import annotations
from typing import Any


class ApiError(Exception):
    """
    Excepción estándar para errores al consumir la API.
    - message: texto base del error
    - status_code: código HTTP (int). Usa 0 para errores de red/conexión.
    - payload: dict opcional con detalle estructurado devuelto por la API
    """
    def __init__(self, message: str, status_code: int, payload: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload or {}


def api_error_to_text(ex: ApiError) -> str:
    """
    Convierte ApiError a un texto amigable para UI (SnackBar/Toast/Dialog).
    """
    payload = getattr(ex, "payload", None) or {}
    
    # Manejar caso donde el message recibió un string tipo lista (FastAPI error)
    import ast
    ex_msg = str(ex)
    if ex_msg.startswith("[{") or ex_msg.startswith("{"):
        try:
            parsed = ast.literal_eval(ex_msg)
            if isinstance(parsed, list):
                return "\n".join([str(d.get("msg", str(d))) for d in parsed if isinstance(d, dict)])
            elif isinstance(parsed, dict):
                if "detalles" in parsed:
                    det = parsed["detalles"]
                    return "\n".join(str(x) for x in det) if isinstance(det, list) else str(det)
                if "detail" in parsed:
                    return str(parsed["detail"])
        except Exception:
            pass

    if isinstance(payload, dict):
        detalles = getattr(payload, "get", lambda x: None)("detalles")
        if isinstance(detalles, list) and detalles:
            return "\n".join(str(x) for x in detalles)

        if "detail" in payload:
            return str(payload["detail"])
        if "error" in payload:
            return str(payload["error"])

    # Fallback si el payload está vacío
    ex_str = str(ex).replace("ApiError(", "").strip(")'\"")
    return ex_str