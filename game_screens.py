"""
🎮 BATALLA DE HÉROES - GAME SCREENS
Pantallas del juego usando State Pattern
"""

import pygame
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from ui_components import *
from game_core import *

if TYPE_CHECKING:
    from game_main import GameApp


# ============================================================================
# ESTADO BASE (State Pattern)
# ============================================================================

class GameState(ABC):
    """Estado base para las pantallas del juego"""
    
    def __init__(self, app: 'GameApp'):
        self.app = app
        self.theme = Theme()
        self.components: list[Component] = []
    
    @abstractmethod
    def handle_events(self, events: list):
        """Maneja eventos"""
        pass
    
    @abstractmethod
    def update(self):
        """Actualiza el estado"""
        pass
    
    @abstractmethod
    def render(self, surface: pygame.Surface):
        """Renderiza la pantalla"""
        pass
    
    def enter(self):
        """Llamado al entrar al estado"""
        pass
    
    def exit(self):
        """Llamado al salir del estado"""
        pass
    
    def on_resize(self, width: int, height: int):
        """Llamado cuando la ventana cambia de tamaño"""
        # Actualizar escala del tema
        scale = min(width / 1366, height / 768)
        self.theme.set_scale(scale)
        
        # Actualizar escala de todos los componentes
        scale_x = width / 1366
        scale_y = height / 768
        for component in self.components:
            component.set_scale(scale_x, scale_y)


# ============================================================================
# MENÚ PRINCIPAL
# ============================================================================

class MenuState(GameState):
    """Pantalla de menú principal"""
    
    def __init__(self, app: 'GameApp'):
        super().__init__(app)
        self._crear_componentes()
    
    def _crear_componentes(self):
        """Crea los componentes del menú usando coordenadas base (1366x768)"""
        base_width = 1366
        base_height = 768
        
        # Título
        self.title_label = Label(
            base_width // 2 - 300, 150,
            "⚔️ BATALLA DE HÉROES ⚔️",
            self.theme.FONT_XL, self.theme.PRIMARY_LIGHT
        )
        
        # Subtítulo
        self.subtitle_label = Label(
            base_width // 2 - 180, 220,
            "Arena Mágica de Combate",
            self.theme.FONT_S, self.theme.TEXT_DIM
        )
        
        # Botones (usando coordenadas base)
        button_width = 400
        button_height = 70
        button_x = base_width // 2 - button_width // 2
        start_y = 320
        spacing = 90
        
        self.btn_battle = Button(
            button_x, start_y, button_width, button_height,
            "⚔️ Iniciar Batalla",
            self.theme.PRIMARY,
            lambda: self.app.change_state('battle')
        )
        
        self.btn_custom = Button(
            button_x, start_y + spacing, button_width, button_height,
            "🎲 Batalla Personalizada",
            self.theme.SECONDARY,
            lambda: self.app.change_state('custom')
        )
        
        self.btn_test = Button(
            button_x, start_y + spacing * 2, button_width, button_height,
            "🧪 Modo Prueba",
            self.theme.SUCCESS,
            lambda: self.app.change_state('test')
        )
        
        self.btn_exit = Button(
            button_x, start_y + spacing * 3, button_width, button_height,
            "❌ Salir",
            self.theme.DANGER,
            lambda: self.app.quit()
        )
        
        # Info (usando coordenadas base)
        self.info_label = Label(
            base_width // 2 - 200, base_height - 30,
            "Desarrollado con Python + Pygame | v3.0",
            self.theme.FONT_XS, self.theme.TEXT_MUTED
        )
        
        self.components = [
            self.title_label,
            self.subtitle_label,
            self.btn_battle,
            self.btn_custom,
            self.btn_test,
            self.btn_exit,
            self.info_label
        ]
        
        # Aplicar escala inicial si la ventana no es del tamaño base
        self.on_resize(self.app.width, self.app.height)
    
    def handle_events(self, events: list):
        mouse_pos = pygame.mouse.get_pos()
        for component in self.components:
            component.update(events, mouse_pos)
    
    def update(self):
        pass
    
    def render(self, surface: pygame.Surface):
        surface.fill(self.theme.BG)
        for component in self.components:
            component.draw(surface)


# ============================================================================
# BATALLA
# ============================================================================

class BattleState(GameState):
    """Pantalla de batalla"""
    
    def __init__(self, app: 'GameApp', num_rondas: int = 5, 
                 lista_heroes: Optional[ListaHeroes] = None):
        super().__init__(app)
        
        # Inicializar motor de juego
        if lista_heroes is None:
            lista_heroes = HeroFactory.crear_lista_inicial()
        
        self.motor = MotorCombate(lista_heroes, num_rondas)
        self.motor.agregar_observer(self._on_combat_event)
        
        # Estado de la batalla
        self.auto_play = True
        self.auto_timer = 0
        self.auto_delay = 90  # frames entre turnos
        self.paused = False
        self.game_over = False
        self.ganador = None
        
        # Log de batalla
        self.battle_log: list[str] = []
        self.max_log_entries = 8
        
        self._crear_componentes()
    
    def _crear_componentes(self):
        """Crea componentes de la UI usando coordenadas base (1366x768)"""
        base_height = 768
        
        # Panel de héroes
        self.hero_cards: list[HeroCard] = []
        card_width = 300
        card_height = 140
        start_x = 30
        start_y = 120
        spacing = 150
        
        for i, heroe in enumerate(self.motor.lista_heroes.iterar()):
            card = HeroCard(start_x, start_y + i * spacing, card_width, card_height)
            card.set_hero(heroe.nombre, heroe.nivel, heroe.ataque, heroe.pv, heroe.pv_max,
                         heroe.defensa, heroe.energia, heroe.energia_max)
            self.hero_cards.append(card)
        
        # Panel de log
        self.log_panel = Panel(700, 100, 630, 400, border_color=self.theme.PRIMARY)
        
        # Panel de stats
        self.stats_panel = Panel(700, 520, 630, 180, border_color=self.theme.SECONDARY)
        
        # Botones de control (usando coordenadas base)
        self.btn_next = Button(
            30, base_height - 80, 150, 60,
            "▶ Siguiente",
            self.theme.SUCCESS,
            self._next_turn
        )
        
        self.btn_pause = Button(
            200, base_height - 80, 150, 60,
            "⏸️ Pausa",
            self.theme.WARNING,
            self._toggle_pause
        )
        
        self.btn_menu = Button(
            370, base_height - 80, 150, 60,
            "🏠 Menú",
            self.theme.PRIMARY,
            lambda: self.app.change_state('menu')
        )
        
        self.components = [
            self.log_panel,
            self.stats_panel,
            self.btn_next,
            self.btn_pause,
            self.btn_menu
        ] + self.hero_cards
        
        # Aplicar escala inicial
        self.on_resize(self.app.width, self.app.height)
    
    def _on_combat_event(self, evento: dict):
        """Observador de eventos de combate con eventos mejorados"""
        tipo = evento.get("tipo")
        
        if tipo == "ataque":
            # Mensajes mejorados con íconos
            critico_icon = "💥" if evento.get("es_critico") else "⚔️"
            esquiva_msg = ""
            
            if evento.get("fue_esquivado"):
                msg = f"💨 {evento['objetivo']} ESQUIVÓ el ataque de {evento['atacante']}!"
            elif evento.get("es_critico"):
                msg = f"{critico_icon} ¡CRÍTICO! {evento['atacante']} → {evento['objetivo']}: -{evento['dano']} PV"
            else:
                msg = f"{critico_icon} {evento['atacante']} → {evento['objetivo']}: -{evento['dano']} PV"
            
            self.battle_log.append(msg)
            
            if evento.get("objetivo_murio"):
                self.battle_log.append(f"💀 {evento['objetivo']} HA SIDO DERROTADO!")
        
        elif tipo == "habilidad":
            if evento.get("fue_esquivado"):
                msg = f"💨 {evento['objetivo']} ESQUIVÓ la habilidad especial de {evento['atacante']}!"
            else:
                msg = f"✨ ¡HABILIDAD ESPECIAL! {evento['atacante']} → {evento['objetivo']}: -{evento['dano']} PV"
            self.battle_log.append(msg)
            
            if evento.get("objetivo_murio"):
                self.battle_log.append(f"💀 {evento['objetivo']} HA SIDO DERROTADO!")
        
        elif tipo == "habilidad_fallida":
            razon = evento.get("razon", "")
            if razon == "energia_insuficiente":
                msg = f"⚠️ {evento['atacante']} no tiene suficiente energía"
            else:
                msg = f"⚠️ Habilidad de {evento['atacante']} falló"
            self.battle_log.append(msg)
        
        elif tipo == "curacion":
            msg = f"💚 {evento['heroe']} se cura +{evento['cantidad']} PV"
            self.battle_log.append(msg)
        
        elif tipo == "pasar":
            curacion = evento.get("curacion_pasiva", 0)
            if curacion > 0:
                msg = f"⏭️ {evento['heroe']} recupera energía (+{curacion} PV)"
            else:
                msg = f"⏭️ {evento['heroe']} recupera energía"
            self.battle_log.append(msg)
        
        elif tipo == "fin_ronda":
            self.battle_log.append(f"═══ FIN RONDA {evento['ronda']} ═══")
        
        # Limitar log
        if len(self.battle_log) > self.max_log_entries:
            self.battle_log = self.battle_log[-self.max_log_entries:]
        
        # Actualizar tarjetas
        self._actualizar_hero_cards()
    
    def _actualizar_hero_cards(self):
        """Actualiza las tarjetas de héroes con todas las stats"""
        heroes = self.motor.lista_heroes.iterar()
        heroe_actual = self.motor.turnos.obtener_turno_actual()
        
        for i, heroe in enumerate(heroes):
            if i < len(self.hero_cards):
                card = self.hero_cards[i]
                card.set_hero(heroe.nombre, heroe.nivel, heroe.ataque, heroe.pv, heroe.pv_max,
                             heroe.defensa, heroe.energia, heroe.energia_max)
                card.set_active(heroe_actual and heroe.nombre == heroe_actual.nombre)
    
    def _next_turn(self):
        """Ejecuta el siguiente turno"""
        if self.game_over:
            self.app.change_state('results', ganador=self.ganador, 
                                 stats=self.motor.estadisticas)
            return
        
        resultado = self.motor.ejecutar_turno()
        
        if resultado.get("fin_juego"):
            self.game_over = True
            self.ganador = resultado.get("ganador")
    
    def _toggle_pause(self):
        """Alterna pausa"""
        self.paused = not self.paused
        self.btn_pause.text = "▶ Reanudar" if self.paused else "⏸️ Pausa"
    
    def handle_events(self, events: list):
        mouse_pos = pygame.mouse.get_pos()
        for component in self.components:
            component.update(events, mouse_pos)
        
        # Tecla ESC para volver
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.app.change_state('menu')
                elif event.key == pygame.K_SPACE:
                    self._toggle_pause()
    
    def update(self):
        # Auto-avance si no está pausado
        if self.auto_play and not self.paused and not self.game_over:
            self.auto_timer += 1
            if self.auto_timer >= self.auto_delay:
                self._next_turn()
                self.auto_timer = 0
    
    def render(self, surface: pygame.Surface):
        surface.fill(self.theme.BG)
        
        # Título con ronda
        title_text = f"RONDA {self.motor.ronda_actual + 1}/{self.motor.num_rondas}"
        title_surf = self.theme.FONT_M.render(title_text, True, self.theme.PRIMARY_LIGHT)
        title_rect = title_surf.get_rect(center=(self.app.width // 2, 40))
        surface.blit(title_surf, title_rect)
        
        # Componentes
        for component in self.components:
            component.draw(surface)
        
        # Log de batalla
        log_y = 140
        for i, log_entry in enumerate(self.battle_log):
            log_surf = self.theme.FONT_XS.render(log_entry, True, self.theme.TEXT_DIM)
            surface.blit(log_surf, (720, log_y + i * 30))
        
        # Estadísticas mejoradas
        stats_y = 560
        stats = [
            f"⚔️ Ataques: {self.motor.estadisticas['ataques_totales']} | 💥 Críticos: {self.motor.estadisticas.get('criticos', 0)}",
            f"💨 Esquivas: {self.motor.estadisticas.get('esquivas', 0)} | ✨ Habilidades: {self.motor.estadisticas.get('habilidades_usadas', 0)}",
            f"🩸 Daño total: {self.motor.estadisticas['dano_total']}",
            f"💚 Curaciones: {self.motor.estadisticas['curaciones_totales']} (+{self.motor.estadisticas['salud_restaurada']} PV)"
        ]
        
        for i, stat in enumerate(stats):
            stat_surf = self.theme.FONT_XS.render(stat, True, self.theme.TEXT_DIM)
            surface.blit(stat_surf, (720, stats_y + i * 30))


# ============================================================================
# RESULTADOS
# ============================================================================

class ResultsState(GameState):
    """Pantalla de resultados"""
    
    def __init__(self, app: 'GameApp', ganador: Optional[NodoHeroe] = None, 
                 stats: dict = None):
        super().__init__(app)
        self.ganador = ganador
        self.stats = stats or {}
        self._crear_componentes()
    
    def _crear_componentes(self):
        """Crea componentes de resultados usando coordenadas base (1366x768)"""
        base_width = 1366
        base_height = 768
        
        self.btn_menu = Button(
            base_width // 2 - 150, base_height - 100, 300, 70,
            "🏠 Volver al Menú",
            self.theme.PRIMARY,
            lambda: self.app.change_state('menu')
        )
        
        self.components = [self.btn_menu]
        
        # Aplicar escala inicial
        self.on_resize(self.app.width, self.app.height)
    
    def handle_events(self, events: list):
        mouse_pos = pygame.mouse.get_pos()
        for component in self.components:
            component.update(events, mouse_pos)
    
    def update(self):
        pass
    
    def render(self, surface: pygame.Surface):
        surface.fill(self.theme.BG)
        
        # Título
        title_surf = self.theme.FONT_XL.render("🏆 ¡BATALLA FINALIZADA! 🏆", 
                                              True, self.theme.PRIMARY_LIGHT)
        title_rect = title_surf.get_rect(center=(self.app.width // 2, 80))
        surface.blit(title_surf, title_rect)
        
        if self.ganador:
            # Panel del ganador
            panel_rect = pygame.Rect(100, 180, self.app.width - 200, 200)
            pygame.draw.rect(surface, self.theme.BG_LIGHT, panel_rect, border_radius=20)
            pygame.draw.rect(surface, self.theme.SUCCESS, panel_rect, width=4, border_radius=20)
            
            # Nombre del ganador
            winner_title = self.theme.FONT_L.render("👑 GANADOR 👑", True, self.theme.SUCCESS)
            winner_rect = winner_title.get_rect(center=(self.app.width // 2, 240))
            surface.blit(winner_title, winner_rect)
            
            winner_name = self.theme.FONT_M.render(self.ganador.nombre, True, self.theme.TEXT)
            name_rect = winner_name.get_rect(center=(self.app.width // 2, 290))
            surface.blit(winner_name, name_rect)
            
            # Stats del ganador
            stats_text = f"❤️ PV: {self.ganador.pv}/{self.ganador.pv_max}  |  ⚔️ Ataque: {self.ganador.ataque}  |  🏅 Nivel: {self.ganador.nivel}"
            stats_surf = self.theme.FONT_S.render(stats_text, True, self.theme.TEXT_DIM)
            stats_rect = stats_surf.get_rect(center=(self.app.width // 2, 340))
            surface.blit(stats_surf, stats_rect)
        
        # Estadísticas finales mejoradas
        stats_y = 420
        stats_title = self.theme.FONT_L.render("📊 Estadísticas Finales", True, self.theme.PRIMARY_LIGHT)
        stats_title_rect = stats_title.get_rect(center=(self.app.width // 2, stats_y))
        surface.blit(stats_title, stats_title_rect)
        
        stats_list = [
            f"⚔️ Ataques: {self.stats.get('ataques_totales', 0)} | 💥 Críticos: {self.stats.get('criticos', 0)}",
            f"� Esquivas: {self.stats.get('esquivas', 0)} | ✨ Habilidades: {self.stats.get('habilidades_usadas', 0)}",
            f"🩸 Daño total: {self.stats.get('dano_total', 0)}",
            f"💚 Curaciones: {self.stats.get('curaciones_totales', 0)} (+{self.stats.get('salud_restaurada', 0)} PV)"
        ]
        
        for i, stat in enumerate(stats_list):
            stat_surf = self.theme.FONT_S.render(stat, True, self.theme.TEXT_DIM)
            stat_rect = stat_surf.get_rect(center=(self.app.width // 2, stats_y + 60 + i * 40))
            surface.blit(stat_surf, stat_rect)
        
        # Botón
        for component in self.components:
            component.draw(surface)


# ============================================================================
# MODO PRUEBA
# ============================================================================

class TestState(GameState):
    """Pantalla de modo prueba"""
    
    def __init__(self, app: 'GameApp'):
        super().__init__(app)
        self.lista_heroes = HeroFactory.crear_lista_inicial()
        self._crear_componentes()
    
    def _crear_componentes(self):
        """Crea componentes del modo prueba usando coordenadas base (1366x768)"""
        base_width = 1366
        base_height = 768
        
        # Campos de entrada
        input_y = 420
        self.input_nombre = InputField(50, input_y, 250, 40, "Nombre", "text")
        self.input_nivel = InputField(320, input_y, 150, 40, "Nivel", "number")
        self.input_pv = InputField(490, input_y, 150, 40, "PV", "number")
        self.input_ataque = InputField(660, input_y, 150, 40, "Ataque", "number")
        
        # Botones de acción
        button_y = 520
        self.btn_add = Button(50, button_y, 200, 60, "➕ Agregar", 
                             self.theme.SUCCESS, self._agregar_heroe)
        self.btn_delete = Button(270, button_y, 200, 60, "🗑️ Eliminar", 
                                self.theme.DANGER, self._eliminar_heroe)
        self.btn_search = Button(490, button_y, 200, 60, "🔍 Buscar", 
                                self.theme.PRIMARY, self._buscar_heroe)
        self.btn_improve = Button(710, button_y, 200, 60, "⬆️ Mejorar", 
                                 self.theme.WARNING, self._mejorar_heroe)
        self.btn_battle = Button(930, button_y, 200, 60, "⚔️ Batalla", 
                                self.theme.SECONDARY, self._iniciar_batalla)
        
        # Botón volver (usando coordenadas base)
        self.btn_back = Button(
            base_width // 2 - 150, base_height - 80, 300, 60,
            "🏠 Volver al Menú",
            self.theme.PRIMARY,
            lambda: self.app.change_state('menu')
        )
        
        # Mensaje (usando coordenadas base)
        self.message_box = MessageBox(
            base_width // 2 - 300, 600, 600, 60
        )
        
        self.components = [
            self.input_nombre, self.input_nivel, self.input_pv, self.input_ataque,
            self.btn_add, self.btn_delete, self.btn_search, self.btn_improve, self.btn_battle,
            self.btn_back, self.message_box
        ]
        
        # Aplicar escala inicial
        self.on_resize(self.app.width, self.app.height)
    
    def _agregar_heroe(self):
        nombre = self.input_nombre.get_text()
        nivel = int(self.input_nivel.get_text() or "1")
        pv = int(self.input_pv.get_text() or "100")
        ataque = int(self.input_ataque.get_text() or "20")
        
        if self.lista_heroes.agregar_heroe(nombre, nivel, pv, ataque):
            self.message_box.show_message(f"✅ {nombre} agregado!", "success")
            self.input_nombre.clear()
            self.input_nivel.clear()
            self.input_pv.clear()
            self.input_ataque.clear()
        else:
            self.message_box.show_message("❌ Datos inválidos", "error")
    
    def _eliminar_heroe(self):
        nombre = self.input_nombre.get_text()
        if self.lista_heroes.eliminar_heroe(nombre):
            self.message_box.show_message(f"✅ {nombre} eliminado!", "success")
        else:
            self.message_box.show_message(f"❌ {nombre} no encontrado", "error")
    
    def _buscar_heroe(self):
        nombre = self.input_nombre.get_text()
        heroe = self.lista_heroes.buscar_heroe(nombre)
        if heroe:
            msg = f"✅ {heroe.nombre} | Nv.{heroe.nivel} | PV:{heroe.pv} | Atq:{heroe.ataque}"
            self.message_box.show_message(msg, "success", 240)
        else:
            self.message_box.show_message(f"❌ {nombre} no encontrado", "error")
    
    def _mejorar_heroe(self):
        nombre = self.input_nombre.get_text()
        if self.lista_heroes.mejorar_heroe(nombre):
            self.message_box.show_message(f"✅ {nombre} mejorado!", "success")
        else:
            self.message_box.show_message(f"❌ {nombre} no encontrado", "error")
    
    def _iniciar_batalla(self):
        if len(self.lista_heroes.obtener_heroes_vivos()) < 2:
            self.message_box.show_message("❌ Se necesitan al menos 2 héroes vivos", "error")
        else:
            self.app.change_state('battle', lista_heroes=self.lista_heroes)
    
    def handle_events(self, events: list):
        mouse_pos = pygame.mouse.get_pos()
        for component in self.components:
            component.update(events, mouse_pos)
    
    def update(self):
        pass
    
    def render(self, surface: pygame.Surface):
        surface.fill(self.theme.BG)
        
        # Título
        title_surf = self.theme.FONT_L.render("🧪 Modo Prueba", True, self.theme.PRIMARY_LIGHT)
        title_rect = title_surf.get_rect(center=(self.app.width // 2, 40))
        surface.blit(title_surf, title_rect)
        
        # Lista de héroes
        list_y = 120
        for i, heroe in enumerate(self.lista_heroes.iterar()):
            estado = "✅" if heroe.pv > 0 else "💀"
            text = f"{i+1}. {estado} {heroe.nombre} [Nv.{heroe.nivel}] | PV: {heroe.pv}/{heroe.pv_max} | Atq: {heroe.ataque}"
            text_surf = self.theme.FONT_XS.render(text, True, self.theme.TEXT_DIM)
            surface.blit(text_surf, (50, list_y + i * 35))
        
        # Labels de campos
        labels = ["Nombre:", "Nivel:", "PV:", "Ataque:"]
        for i, label in enumerate(labels):
            x = 50 + i * 220 if i < 2 else 50 + (i-2) * 180
            label_surf = self.theme.FONT_XS.render(label, True, self.theme.TEXT)
            surface.blit(label_surf, (x, 395))
        
        # Componentes
        for component in self.components:
            component.draw(surface)
