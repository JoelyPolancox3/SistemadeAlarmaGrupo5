from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass 
class Usuario:
    nombre: str
    email: str
    contrasena: str
    id: Optional[int] = None
    rol: str = "usuario"

    def __repr__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')"

@dataclass
class Incidencia:  
    id: Optional[int] = None
    usuario_id: int = 0
    Titulo: str = ""
    Descripcion: str = ""
    Estado: str = "Pendiente"
    Fecha_Creacion: datetime = datetime.now()
    prioridad: str = "media"

    def __repr__(self):
        return f"Incidencia(id={self.id}, titulo='{self.Titulo}', estado='{self.Estado}')"

@dataclass
class Cliente:
    id: Optional[int] = None
    nombre: str = ""
    email: str = ""
    telefono: str = ""
    empresa: str = ""
    sector: str = "otros"

    def __repr__(self):
        return f"Cliente(id={self.id}, nombre='{self.nombre}', email='{self.email}')"