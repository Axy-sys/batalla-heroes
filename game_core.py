"""
🎮 BATALLA DE HÉROES - CORE LOGIC
Lógica del juego separada de la presentación (Patrón MVC - Model)
"""

import random
from typing import Optional, List, Callable
from dataclasses import dataclass


# ============================================================================
# ENTIDADES DEL DOMINIO
# ============================================================================

@dataclass
class HeroStats:
    """Value Object para estadísticas del héroe"""
    nombre: str
    nivel: int
    pv: int
    pv_max: int
    ataque: int
    defensa: int = 5  # Nueva stat: reduce daño recibido
    critico: float = 0.15  # Probabilidad de golpe crítico (15%)
    esquiva: float = 0.10  # Probabilidad de esquivar (10%)
    energia: int = 0  # Energía para habilidades especiales
    energia_max: int = 100
    
    def esta_vivo(self) -> bool:
        return self.pv > 0
    
    def recibir_dano(self, cantidad: int) -> tuple[int, bool]:
        """Retorna (daño real aplicado, fue_esquivado)"""
        # Probabilidad de esquivar
        if random.random() < self.esquiva:
            return (0, True)
        
        # Aplicar defensa (reduce daño en un porcentaje)
        reduccion = min(0.7, self.defensa * 0.02)  # Max 70% reducción
        dano_reducido = int(cantidad * (1 - reduccion))
        
        dano_real = min(dano_reducido, self.pv)
        self.pv = max(0, self.pv - dano_reducido)
        return (dano_real, False)
    
    def curar(self, cantidad: int) -> int:
        """Retorna la curación real aplicada"""
        curacion_real = min(cantidad, self.pv_max - self.pv)
        self.pv = min(self.pv_max, self.pv + cantidad)
        return curacion_real
    
    def ganar_energia(self, cantidad: int = 20):
        """Gana energía cada turno"""
        self.energia = min(self.energia_max, self.energia + cantidad)
    
    def usar_energia(self, cantidad: int) -> bool:
        """Intenta usar energía. Retorna True si tiene suficiente"""
        if self.energia >= cantidad:
            self.energia -= cantidad
            return True
        return False
    
    def mejorar(self, inc_pv: int = 10, inc_ataque: int = 5):
        """Mejora las estadísticas del héroe"""
        self.nivel += 1
        self.pv_max += inc_pv
        self.pv = min(self.pv + inc_pv, self.pv_max)
        self.ataque += inc_ataque
        self.defensa += 1
        self.critico = min(0.5, self.critico + 0.02)  # Max 50% crítico


class NodoHeroe:
    """Nodo para lista enlazada simple"""
    def __init__(self, stats: HeroStats):
        self.stats = stats
        self.siguiente: Optional['NodoHeroe'] = None
    
    @property
    def nombre(self):
        return self.stats.nombre
    
    @property
    def nivel(self):
        return self.stats.nivel
    
    @property
    def pv(self):
        return self.stats.pv
    
    @property
    def pv_max(self):
        return self.stats.pv_max
    
    @property
    def ataque(self):
        return self.stats.ataque
    
    @property
    def defensa(self):
        return self.stats.defensa
    
    @property
    def energia(self):
        return self.stats.energia
    
    @property
    def energia_max(self):
        return self.stats.energia_max
    
    @property
    def critico(self):
        return self.stats.critico
    
    @property
    def esquiva(self):
        return self.stats.esquiva


class NodoTurno:
    """Nodo para lista circular de turnos"""
    def __init__(self, heroe: NodoHeroe):
        self.heroe = heroe
        self.siguiente: Optional['NodoTurno'] = None


# ============================================================================
# ESTRUCTURAS DE DATOS
# ============================================================================

class ListaHeroes:
    """Lista enlazada simple para gestionar héroes"""
    
    def __init__(self):
        self.cabeza: Optional[NodoHeroe] = None
        self.tamano: int = 0
    
    def agregar_heroe(self, nombre: str, nivel: int, pv: int, ataque: int) -> bool:
        """Agrega un héroe al final de la lista"""
        if not self._validar_datos(nombre, nivel, pv, ataque):
            return False
        
        stats = HeroStats(nombre, nivel, pv, pv, ataque)
        nuevo_nodo = NodoHeroe(stats)
        
        if not self.cabeza:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo_nodo
        
        self.tamano += 1
        return True
    
    def eliminar_heroe(self, nombre: str) -> bool:
        """Elimina un héroe por nombre"""
        if not self.cabeza:
            return False
        
        # Caso especial: eliminar cabeza
        if self.cabeza.nombre == nombre:
            self.cabeza = self.cabeza.siguiente
            self.tamano -= 1
            return True
        
        # Buscar en el resto de la lista
        actual = self.cabeza
        while actual.siguiente:
            if actual.siguiente.nombre == nombre:
                actual.siguiente = actual.siguiente.siguiente
                self.tamano -= 1
                return True
            actual = actual.siguiente
        
        return False
    
    def buscar_heroe(self, nombre: str) -> Optional[NodoHeroe]:
        """Busca un héroe por nombre"""
        actual = self.cabeza
        while actual:
            if actual.nombre == nombre:
                return actual
            actual = actual.siguiente
        return None
    
    def mejorar_heroe(self, nombre: str, inc_pv: int = 10, inc_ataque: int = 5) -> bool:
        """Mejora las estadísticas de un héroe"""
        heroe = self.buscar_heroe(nombre)
        if heroe:
            heroe.stats.mejorar(inc_pv, inc_ataque)
            return True
        return False
    
    def obtener_heroes_vivos(self) -> List[NodoHeroe]:
        """Retorna lista de héroes vivos"""
        heroes = []
        actual = self.cabeza
        while actual:
            if actual.stats.esta_vivo():
                heroes.append(actual)
            actual = actual.siguiente
        return heroes
    
    def iterar(self) -> List[NodoHeroe]:
        """Retorna todos los héroes como lista"""
        heroes = []
        actual = self.cabeza
        while actual:
            heroes.append(actual)
            actual = actual.siguiente
        return heroes
    
    def _validar_datos(self, nombre: str, nivel: int, pv: int, ataque: int) -> bool:
        """Valida los datos de entrada"""
        if not nombre or not isinstance(nombre, str):
            return False
        if nivel < 1 or nivel > 10:
            return False
        if pv < 10 or pv > 200:
            return False
        if ataque < 5 or ataque > 50:
            return False
        return True


class ListaCircularTurnos:
    """Lista circular para gestionar turnos de batalla"""
    
    def __init__(self):
        self.actual: Optional[NodoTurno] = None
        self.tamano: int = 0
    
    def agregar_turno(self, heroe: NodoHeroe) -> bool:
        """Agrega un turno a la lista circular"""
        nuevo_nodo = NodoTurno(heroe)
        
        if not self.actual:
            nuevo_nodo.siguiente = nuevo_nodo
            self.actual = nuevo_nodo
        else:
            # Insertar al final
            temp = self.actual
            while temp.siguiente != self.actual:
                temp = temp.siguiente
            temp.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.actual
        
        self.tamano += 1
        return True
    
    def eliminar_turno(self, nombre: str) -> bool:
        """Elimina un turno por nombre del héroe"""
        if not self.actual or self.tamano == 0:
            return False
        
        # Caso especial: un solo nodo
        if self.tamano == 1:
            if self.actual.heroe.nombre == nombre:
                self.actual = None
                self.tamano = 0
                return True
            return False
        
        # Buscar el nodo a eliminar
        temp = self.actual
        anterior = None
        
        # Encontrar el anterior al actual
        while temp.siguiente != self.actual:
            temp = temp.siguiente
        anterior = temp
        
        # Buscar en toda la lista circular
        temp = self.actual
        for _ in range(self.tamano):
            if temp.heroe.nombre == nombre:
                if temp == self.actual:
                    # Eliminar el actual
                    anterior.siguiente = temp.siguiente
                    self.actual = temp.siguiente
                else:
                    anterior.siguiente = temp.siguiente
                
                self.tamano -= 1
                return True
            
            anterior = temp
            temp = temp.siguiente
        
        return False
    
    def siguiente_turno(self) -> Optional[NodoHeroe]:
        """Avanza al siguiente turno"""
        if not self.actual:
            return None
        
        self.actual = self.actual.siguiente
        return self.actual.heroe
    
    def obtener_turno_actual(self) -> Optional[NodoHeroe]:
        """Retorna el héroe del turno actual"""
        return self.actual.heroe if self.actual else None
    
    def ordenar_por_pv(self):
        """Ordena la lista circular por PV (descendente)"""
        if self.tamano <= 1:
            return
        
        # Convertir a lista
        heroes = []
        temp = self.actual
        for _ in range(self.tamano):
            heroes.append(temp.heroe)
            temp = temp.siguiente
        
        # Ordenar por PV (burbuja)
        for i in range(len(heroes)):
            for j in range(len(heroes) - 1 - i):
                if heroes[j].pv < heroes[j + 1].pv:
                    heroes[j], heroes[j + 1] = heroes[j + 1], heroes[j]
        
        # Reconstruir lista circular
        self.actual = None
        self.tamano = 0
        for heroe in heroes:
            self.agregar_turno(heroe)


# ============================================================================
# LÓGICA DE COMBATE (Patrón Strategy)
# ============================================================================

class AccionCombate:
    """Clase base para acciones de combate (Strategy Pattern)"""
    
    def ejecutar(self, atacante: NodoHeroe, objetivo: Optional[NodoHeroe] = None) -> dict:
        """Ejecuta la acción y retorna resultado"""
        raise NotImplementedError


class AccionAtacar(AccionCombate):
    """Estrategia de ataque"""
    
    def ejecutar(self, atacante: NodoHeroe, objetivo: Optional[NodoHeroe] = None) -> dict:
        if not objetivo or not objetivo.stats.esta_vivo():
            return {"tipo": "ataque_fallido", "atacante": atacante.nombre}
        
        # Calcular daño base
        dano_base = atacante.ataque
        dano_aleatorio = random.randint(-5, 15)
        dano_total = dano_base + dano_aleatorio
        
        # Verificar crítico
        es_critico = random.random() < atacante.critico
        if es_critico:
            dano_total = int(dano_total * 1.5)  # 50% más de daño
        
        # Aplicar daño (considera defensa y esquiva)
        dano_real, fue_esquivado = objetivo.stats.recibir_dano(dano_total)
        
        # Ganar energía por atacar
        atacante.stats.ganar_energia(15)
        
        return {
            "tipo": "ataque",
            "atacante": atacante.nombre,
            "objetivo": objetivo.nombre,
            "dano": dano_real,
            "es_critico": es_critico,
            "fue_esquivado": fue_esquivado,
            "objetivo_murio": not objetivo.stats.esta_vivo()
        }


class AccionCurar(AccionCombate):
    """Estrategia de curación"""
    
    def ejecutar(self, atacante: NodoHeroe, objetivo: Optional[NodoHeroe] = None) -> dict:
        curacion_base = 15 + (atacante.nivel * 5)
        curacion_aleatoria = random.randint(5, 20)
        curacion = curacion_base + curacion_aleatoria
        
        curacion_real = atacante.stats.curar(curacion)
        
        # Ganar energía por curar
        atacante.stats.ganar_energia(10)
        
        return {
            "tipo": "curacion",
            "heroe": atacante.nombre,
            "cantidad": curacion_real
        }


class AccionHabilidadEspecial(AccionCombate):
    """Estrategia de habilidad especial (cuesta energía)"""
    
    def __init__(self, costo_energia: int = 50):
        self.costo_energia = costo_energia
    
    def ejecutar(self, atacante: NodoHeroe, objetivo: Optional[NodoHeroe] = None) -> dict:
        # Verificar si tiene energía suficiente
        if not atacante.stats.usar_energia(self.costo_energia):
            return {
                "tipo": "habilidad_fallida",
                "atacante": atacante.nombre,
                "razon": "energia_insuficiente"
            }
        
        if not objetivo or not objetivo.stats.esta_vivo():
            return {"tipo": "habilidad_fallida", "atacante": atacante.nombre, "razon": "sin_objetivo"}
        
        # Habilidad especial: Daño masivo ignorando defensa
        dano_base = int(atacante.ataque * 2.5)
        dano_aleatorio = random.randint(20, 40)
        dano_total = dano_base + dano_aleatorio
        
        # Ignorar defensa pero no esquiva
        if random.random() < objetivo.esquiva:
            return {
                "tipo": "habilidad",
                "atacante": atacante.nombre,
                "objetivo": objetivo.nombre,
                "dano": 0,
                "fue_esquivado": True,
                "objetivo_murio": False
            }
        
        # Aplicar daño directo
        dano_real = min(dano_total, objetivo.pv)
        objetivo.stats.pv = max(0, objetivo.stats.pv - dano_total)
        
        return {
            "tipo": "habilidad",
            "atacante": atacante.nombre,
            "objetivo": objetivo.nombre,
            "dano": dano_real,
            "fue_esquivado": False,
            "objetivo_murio": not objetivo.stats.esta_vivo()
        }


class AccionPasar(AccionCombate):
    """Estrategia de pasar turno"""
    
    def ejecutar(self, atacante: NodoHeroe, objetivo: Optional[NodoHeroe] = None) -> dict:
        # Recuperar energía y vida al pasar turno
        atacante.stats.ganar_energia(25)
        curacion = int(atacante.pv_max * 0.05)  # 5% de vida máxima
        curacion_real = atacante.stats.curar(curacion)
        
        return {
            "tipo": "pasar",
            "heroe": atacante.nombre,
            "curacion_pasiva": curacion_real
        }


# ============================================================================
# MOTOR DE JUEGO (Patrón Facade)
# ============================================================================

class MotorCombate:
    """Facade para la lógica de combate"""
    
    def __init__(self, lista_heroes: ListaHeroes, num_rondas: int = 5):
        self.lista_heroes = lista_heroes
        self.turnos = ListaCircularTurnos()
        self.num_rondas = num_rondas
        self.ronda_actual = 0
        self.estadisticas = {
            "ataques_totales": 0,
            "dano_total": 0,
            "curaciones_totales": 0,
            "salud_restaurada": 0,
            "criticos": 0,
            "esquivas": 0,
            "habilidades_usadas": 0
        }
        self.observers: List[Callable] = []
        
        # Inicializar turnos
        self._inicializar_turnos()
    
    def _inicializar_turnos(self):
        """Inicializa la lista circular de turnos"""
        for heroe in self.lista_heroes.obtener_heroes_vivos():
            self.turnos.agregar_turno(heroe)
    
    def agregar_observer(self, callback: Callable):
        """Patrón Observer para notificar eventos"""
        self.observers.append(callback)
    
    def notificar(self, evento: dict):
        """Notifica a los observers"""
        for observer in self.observers:
            observer(evento)
    
    def ejecutar_turno(self) -> dict:
        """Ejecuta un turno de combate"""
        heroe_actual = self.turnos.obtener_turno_actual()
        if not heroe_actual:
            return {"tipo": "fin_juego"}
        
        # Seleccionar acción con IA
        accion = self._seleccionar_accion(heroe_actual)
        
        # Ejecutar acción
        if isinstance(accion, (AccionAtacar, AccionHabilidadEspecial)):
            objetivo = self._seleccionar_objetivo(heroe_actual)
            resultado = accion.ejecutar(heroe_actual, objetivo)
            
            if resultado["tipo"] in ["ataque", "habilidad"]:
                self.estadisticas["ataques_totales"] += 1
                self.estadisticas["dano_total"] += resultado.get("dano", 0)
                
                # Trackear críticos y esquivas
                if resultado.get("es_critico"):
                    self.estadisticas["criticos"] += 1
                if resultado.get("fue_esquivado"):
                    self.estadisticas["esquivas"] += 1
                if resultado["tipo"] == "habilidad":
                    self.estadisticas["habilidades_usadas"] += 1
                
                # Si murió, eliminar de turnos
                if resultado.get("objetivo_murio", False):
                    self.turnos.eliminar_turno(resultado["objetivo"])
        else:
            resultado = accion.ejecutar(heroe_actual)
            
            if resultado["tipo"] == "curacion":
                self.estadisticas["curaciones_totales"] += 1
                self.estadisticas["salud_restaurada"] += resultado["cantidad"]
        
        # Notificar evento
        self.notificar(resultado)
        
        # Avanzar turno
        self.turnos.siguiente_turno()
        
        # Verificar fin de juego
        heroes_vivos = self.lista_heroes.obtener_heroes_vivos()
        if len(heroes_vivos) <= 1:
            resultado["fin_juego"] = True
            resultado["ganador"] = heroes_vivos[0] if heroes_vivos else None
        
        return resultado
    
    def finalizar_ronda(self):
        """Finaliza una ronda y ordena por PV"""
        self.ronda_actual += 1
        self.turnos.ordenar_por_pv()
        self.notificar({
            "tipo": "fin_ronda",
            "ronda": self.ronda_actual
        })
    
    def obtener_ganador(self) -> Optional[NodoHeroe]:
        """Retorna el héroe ganador"""
        heroes = self.lista_heroes.obtener_heroes_vivos()
        if not heroes:
            return None
        
        ganador = heroes[0]
        for heroe in heroes[1:]:
            if heroe.pv > ganador.pv:
                ganador = heroe
        
        return ganador
    
    def _seleccionar_accion(self, heroe: NodoHeroe) -> AccionCombate:
        """Selecciona acción con IA básica"""
        # Si tiene energía suficiente y poca vida del enemigo, usar habilidad
        if heroe.energia >= 50:
            posibles_objetivos = [h for h in self.lista_heroes.obtener_heroes_vivos() 
                                  if h.nombre != heroe.nombre]
            if posibles_objetivos:
                objetivo_debil = min(posibles_objetivos, key=lambda h: h.pv)
                if objetivo_debil.pv < 60 and random.random() < 0.4:  # 40% chance si está débil
                    return AccionHabilidadEspecial()
        
        # Curar si está por debajo del 40% de vida
        if heroe.pv < heroe.pv_max * 0.4 and random.random() < 0.6:  # 60% chance
            return AccionCurar()
        
        # Decisión normal con ponderación
        rand = random.random()
        if rand < 0.55:  # 55% atacar
            return AccionAtacar()
        elif rand < 0.80:  # 25% curar
            return AccionCurar()
        else:  # 20% pasar (regenerar energía)
            return AccionPasar()
    
    def _seleccionar_objetivo(self, atacante: NodoHeroe) -> Optional[NodoHeroe]:
        """Selecciona objetivo aleatorio"""
        posibles_objetivos = [h for h in self.lista_heroes.obtener_heroes_vivos() 
                              if h.nombre != atacante.nombre]
        return random.choice(posibles_objetivos) if posibles_objetivos else None


# ============================================================================
# FACTORY PARA HÉROES
# ============================================================================

class HeroFactory:
    """Factory pattern para crear héroes predefinidos"""
    
    HEROES_PREDEF = {
        "Artemis": {"nivel": 5, "pv": 100, "ataque": 25, "defensa": 8, "critico": 0.25, "esquiva": 0.15},
        "Merlín": {"nivel": 6, "pv": 85, "ataque": 30, "defensa": 5, "critico": 0.20, "esquiva": 0.12},
        "Thor": {"nivel": 7, "pv": 120, "ataque": 20, "defensa": 12, "critico": 0.15, "esquiva": 0.08},
        "Shadow": {"nivel": 5, "pv": 80, "ataque": 35, "defensa": 6, "critico": 0.30, "esquiva": 0.20},
    }
    
    @staticmethod
    def crear_heroe(nombre: str) -> Optional[HeroStats]:
        """Crea un héroe predefinido"""
        if nombre not in HeroFactory.HEROES_PREDEF:
            return None
        
        datos = HeroFactory.HEROES_PREDEF[nombre]
        return HeroStats(
            nombre=nombre,
            nivel=datos["nivel"],
            pv=datos["pv"],
            pv_max=datos["pv"],
            ataque=datos["ataque"],
            defensa=datos["defensa"],
            critico=datos["critico"],
            esquiva=datos["esquiva"]
        )
    
    @staticmethod
    def crear_lista_inicial() -> ListaHeroes:
        """Crea lista con héroes iniciales"""
        lista = ListaHeroes()
        for nombre in ["Artemis", "Merlín", "Thor", "Shadow"]:
            hero_stats = HeroFactory.crear_heroe(nombre)
            if hero_stats:
                lista.agregar_heroe(
                    hero_stats.nombre,
                    hero_stats.nivel,
                    hero_stats.pv,
                    hero_stats.ataque
                )
        return lista
