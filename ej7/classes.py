class SistemaArmas:
    def __init__(self, numCanones=0, numMisiles=0, numTorpedos=0):
        self.numCanones = numCanones
        self.numMisiles = numMisiles
        self.numTorpedos = numTorpedos

    def seleccionarObjetivo(self, idObjetivo: int):
        print(f"[SistemaArmas] Objetivo seleccionado: {idObjetivo}")
        return idObjetivo

    def dispararArma(self, tipo: str):
        if tipo.lower() == 'misil' and self.numMisiles > 0:
            self.numMisiles -= 1
            print("[SistemaArmas] Disparado misil. Misiles restantes:", self.numMisiles)
            return True
        if tipo.lower() == 'torpedo' and self.numTorpedos > 0:
            self.numTorpedos -= 1
            print("[SistemaArmas] Disparado torpedo. Torpedos restantes:", self.numTorpedos)
            return True
        if tipo.lower() == 'canon' and self.numCanones > 0:
            print("[SistemaArmas] Disparado cañon.")
            return True
        print("[SistemaArmas] No hay arma del tipo solicitado o munición insuficiente.")
        return False


class SistemaSensores:
    def __init__(self, tieneRadar=True, tieneSonar=False, rangoDeteccionKm=20.0):
        self.tieneRadar = tieneRadar
        self.tieneSonar = tieneSonar
        self.rangoDeteccionKm = rangoDeteccionKm

    def escanearSuperficie(self):
        if self.tieneRadar:
            print(f"[SistemaSensores] Escaneando superficie hasta {self.rangoDeteccionKm} km")
            return True
        print("[SistemaSensores] No dispone de radar para escanear superficie")
        return False

    def escanearSubmarino(self):
        if self.tieneSonar:
            print(f"[SistemaSensores] Escaneando subsuperficie hasta {self.rangoDeteccionKm} km")
            return True
        print("[SistemaSensores] No dispone de sonar para detección submarina")
        return False


class PlataformaNaval:
    def __init__(self, nombre: str, pais: str, eslora: float, desplazamiento: float, velocidadMaxima: float,
                 sistema_armas: SistemaArmas = None, sistema_sensores: SistemaSensores = None):
        self.nombre = nombre
        self.pais = pais
        self.eslora = eslora
        self.desplazamiento = desplazamiento
        self.velocidadMaxima = velocidadMaxima
        # Composición: los sistemas existen dentro de la plataforma
        self.sistema_armas = sistema_armas if sistema_armas is not None else SistemaArmas()
        self.sistema_sensores = sistema_sensores if sistema_sensores is not None else SistemaSensores()
        self._integridad = 100  # 0..100
        # Asociación: capitán puede existir independientemente
        self.capitan = None

    def navegar(self, rumbo: float, velocidad: float):
        velocidad_real = min(velocidad, self.velocidadMaxima)
        print(f"[{self.nombre}] Navegando rumbo {rumbo}° a {velocidad_real} nudos")

    def detenerse(self):
        print(f"[{self.nombre}] Maniobra: detenerse. Velocidad a 0 nudos")

    def recibirDanio(self, puntos: int):
        self._integridad -= puntos
        if self._integridad < 0:
            self._integridad = 0
        print(f"[{self.nombre}] Ha recibido {puntos} puntos de daño. Integridad={self._integridad}")

    def estaOperativa(self):
        op = self._integridad > 0
        print(f"[{self.nombre}] Operativa: {op}")
        return op


class Fragata(PlataformaNaval):
    def __init__(self, *args, misilesAntiaereos=8, helicopterosEmb=1, rolPrincipal='Escolta', **kwargs):
        super().__init__(*args, **kwargs)
        self.misilesAntiaereos = misilesAntiaereos
        self.helicopterosEmb = helicopterosEmb
        self.rolPrincipal = rolPrincipal

    def dispararMisilAA(self):
        if self.misilesAntiaereos > 0 and self.sistema_armas.dispararArma('misil'):
            self.misilesAntiaereos -= 1
            print(f"[{self.nombre}] Disparado misil antiaéreo. Misiles AA restantes: {self.misilesAntiaereos}")
            return True
        print(f"[{self.nombre}] No hay misiles AA disponibles")
        return False

    def despegarHelicoptero(self):
        if self.helicopterosEmb > 0:
            print(f"[{self.nombre}] Despegando helicóptero desde cubierta")
            return True
        print(f"[{self.nombre}] No hay helicópteros embarcados")
        return False


class Corbeta(PlataformaNaval):
    def __init__(self, *args, misilesAntibuque=4, autonomiaDias=10, **kwargs):
        super().__init__(*args, **kwargs)
        self.misilesAntibuque = misilesAntibuque
        self.autonomiaDias = autonomiaDias

    def dispararMisilAntibuque(self):
        if self.misilesAntibuque > 0 and self.sistema_armas.dispararArma('misil'):
            self.misilesAntibuque -= 1
            print(f"[{self.nombre}] Disparado misil antibuque. Restan: {self.misilesAntibuque}")
            return True
        print(f"[{self.nombre}] No hay misiles antibuque disponibles")
        return False

    def realizarPatrulla(self, costera: bool):
        t = 'costera' if costera else 'de alta mar'
        print(f"[{self.nombre}] Realizando patrulla {t}")


class Submarino(PlataformaNaval):
    def __init__(self, *args, profundidadMaxima=300, tipoPropulsion='diesel-eléctrico', tubosLanzatorpedos=4, **kwargs):
        super().__init__(*args, **kwargs)
        self.profundidadMaxima = profundidadMaxima
        self.tipoPropulsion = tipoPropulsion
        self.tubosLanzatorpedos = tubosLanzatorpedos
        self.profundido = False

    def sumergirse(self, profundidad: int):
        if profundidad <= self.profundidadMaxima:
            self.profundido = True
            print(f"[{self.nombre}] Sumergiéndose a {profundidad} m")
            return True
        print(f"[{self.nombre}] Profundidad solicitada excede la máxima")
        return False

    def emerger(self):
        if self.profundido:
            self.profundido = False
            print(f"[{self.nombre}] Emergiendo a superficie")
            return True
        print(f"[{self.nombre}] Ya en superficie")
        return False

    def lanzarTorpedo(self):
        if self.tubosLanzatorpedos > 0 and self.sistema_armas.dispararArma('torpedo'):
            self.tubosLanzatorpedos -= 1
            print(f"[{self.nombre}] Torpedo lanzado. Tubos disponibles: {self.tubosLanzatorpedos}")
            return True
        print(f"[{self.nombre}] No hay torpedos disponibles")
        return False


class Flota:
    def __init__(self, nombre: str, zonaOperacion: str):
        self.nombre = nombre
        self.zonaOperacion = zonaOperacion
        # Agregación: la flota mantiene referencias a plataformas
        self.plataformas = []

    def agregarPlataforma(self, p: PlataformaNaval):
        if p not in self.plataformas:
            self.plataformas.append(p)
            print(f"[Flota {self.nombre}] Plataforma {p.nombre} agregada")

    def retirarPlataforma(self, p: PlataformaNaval):
        if p in self.plataformas:
            self.plataformas.remove(p)
            print(f"[Flota {self.nombre}] Plataforma {p.nombre} retirada")

    def ordenarAtaque(self):
        print(f"[Flota {self.nombre}] Orden de ataque en zona {self.zonaOperacion}")
        for p in self.plataformas:
            if p.capitan:
                p.capitan.darOrden('Atacar objetivo designado')
            else:
                print(f"[Flota {self.nombre}] Plataforma {p.nombre} sin capitán; no puede recibir orden directa")


class Capitan:
    def __init__(self, nombre: str, rango: str, aniosExperiencia: int):
        self.nombre = nombre
        self.rango = rango
        self.aniosExperiencia = aniosExperiencia
        self.plataforma = None

    def darOrden(self, orden: str):
        print(f"[Capitán {self.nombre}] Orden: {orden}")

    def asumirMando(self, plataforma: PlataformaNaval):
        # Asociación: el capitán pasa a comandar la plataforma (referencias mutuas)
        if self.plataforma is not None:
            print(f"[Capitán {self.nombre}] Ya comanda {self.plataforma.nombre}; cambiando mando a {plataforma.nombre}")
        self.plataforma = plataforma
        plataforma.capitan = self
        print(f"[Capitán {self.nombre}] Asumido mando de {plataforma.nombre}")
