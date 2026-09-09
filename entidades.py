from dataclasses import dataclass
from datetime import datetime

@dataclass
class Usuario:
    id: int
    nombre: str
    email: str
    contrasena: str
    rol: str  
    telefono: str = ""
    empresa: str = ""
    sector: str = "otros" 

    def __repr__(self):
        return f"Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}', rol='{self.rol}')"

@dataclass
class Incidencia:
    id: int
    usuario_id: int
    titulo: str
    descripcion: str
    estado: str = "pendiente"  
    prioridad: str = "media"  
    fecha_creacion: datetime = datetime.now()

    def __repr__(self):
        return f"Incidencia(id={self.id}, titulo='{self.titulo}', estado='{self.estado}')"