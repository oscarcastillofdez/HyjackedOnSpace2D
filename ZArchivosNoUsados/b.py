from abc import ABC, abstractmethod

class MiClaseAbstracta(ABC):
    @abstractmethod
    def metodo_abstracto(self):
        pass

    @abstractmethod
    def otro_metodo_abstrato(self):
        pass

class MiSubclase(MiClaseAbstracta):
    def metodo_abstracto(self):
        # Implementación del método abstracto
        print("Implementación del método abstracto")

    def otro_metodo_abstrato(self):
        # Implementación del otro método abstracto
        print("Implementación del otro método abstracto")

# Intentar crear una instancia de la clase abstracta dará un error
# mi_objeto = MiClaseAbstracta()

# Pero podemos crear una instancia de la subclase sin problemas
mi_objeto = MiSubclase()
mi_objeto.metodo_abstracto()
mi_objeto.otro_metodo_abstrato("a")
