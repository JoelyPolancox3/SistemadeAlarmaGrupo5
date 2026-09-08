#definicion de la entidad Usuario usando dataclass

from dataclasses import dataclass

from typing import Optional
from datetime import datetime

#Entidad Usuario
@dataclass 
class Usuario:
    nombre: str
    email: str
    contrasena:str

    id: Optional[int] = None
    rol: str = "usuario"

    def __repr__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')"




