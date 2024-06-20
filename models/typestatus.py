from enum import Enum

class TypeStatus(Enum):
    BUENO = 'BUENO'
    CADUCADO = 'CADUCADO'
    POR_CADUCAR = 'POR_CADUCAR'
    @property
    def serialize(self):
        return {
            'name': self.name
        }