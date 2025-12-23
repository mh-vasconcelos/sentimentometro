import unicodedata
import pandas as pd
import numpy as np
# --- Helper Function (Função Auxiliar) ---
def remover_acentos(texto: str) -> str:
    """Remove acentos de uma string."""
    if not isinstance(texto, str):
        return texto
    nfkd_form = unicodedata.normalize('NFKD', texto)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

