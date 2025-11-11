"""
🎨 BATALLA DE HÉROES - UI COMPONENTS
Componentes de interfaz reutilizables (Patrón Composite)
"""

import pygame
from typing import Tuple, Optional, Callable
from abc import ABC, abstractmethod


# ============================================================================
# CONFIGURACIÓN DE COLORES Y FUENTES
# ============================================================================

class Theme:
    """Singleton para el tema visual con soporte para escalado responsivo"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._inicializar()
        return cls._instance
    
    def _inicializar(self):
        # Colores
        self.BG = (15, 15, 25)
        self.BG_LIGHT = (25, 25, 40)
        self.PRIMARY = (100, 80, 255)
        self.PRIMARY_LIGHT = (130, 110, 255)
        self.SECONDARY = (255, 100, 150)
        self.SUCCESS = (50, 200, 100)
        self.WARNING = (255, 180, 50)
        self.DANGER = (255, 70, 70)
        self.TEXT = (255, 255, 255)
        self.TEXT_DIM = (180, 180, 200)
        self.TEXT_MUTED = (120, 120, 140)
        
        # Tamaños base para escalado
        self.base_font_xl = 72
        self.base_font_l = 48
        self.base_font_m = 36
        self.base_font_s = 28
        self.base_font_xs = 22
        
        # Escala actual (1.0 = 100%)
        self.scale = 1.0
        
        # Inicializar fuentes con escala base
        self._update_fonts()
    
    def _update_fonts(self):
        """Actualiza las fuentes según la escala actual"""
        # Fuentes con soporte para emojis
        emoji_fonts = ['segoeuisymbol', 'seguiemj', 'arial', 'segoeui', 'calibri']
        font_found = None
        
        for font_name in emoji_fonts:
            try:
                test_font = pygame.font.SysFont(font_name, 36)
                font_found = font_name
                break
            except:
                continue
        
        # Calcular tamaños escalados
        size_xl = int(self.base_font_xl * self.scale)
        size_l = int(self.base_font_l * self.scale)
        size_m = int(self.base_font_m * self.scale)
        size_s = int(self.base_font_s * self.scale)
        size_xs = int(self.base_font_xs * self.scale)
        
        # Si se encontró una fuente del sistema, usarla; si no, usar la predeterminada
        if font_found:
            self.FONT_XL = pygame.font.SysFont(font_found, size_xl)
            self.FONT_L = pygame.font.SysFont(font_found, size_l)
            self.FONT_M = pygame.font.SysFont(font_found, size_m)
            self.FONT_S = pygame.font.SysFont(font_found, size_s)
            self.FONT_XS = pygame.font.SysFont(font_found, size_xs)
        else:
            # Fallback a fuente predeterminada (sin emojis)
            self.FONT_XL = pygame.font.Font(None, size_xl)
            self.FONT_L = pygame.font.Font(None, size_l)
            self.FONT_M = pygame.font.Font(None, size_m)
            self.FONT_S = pygame.font.Font(None, size_s)
            self.FONT_XS = pygame.font.Font(None, size_xs)
    
    def set_scale(self, scale: float):
        """Actualiza la escala del tema y regenera las fuentes"""
        self.scale = max(0.5, min(2.0, scale))  # Limitar entre 50% y 200%
        self._update_fonts()


# ============================================================================
# COMPONENTES BASE
# ============================================================================

class Component(ABC):
    """Componente base (Composite Pattern) con soporte para escalado"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        # Guardar posición y tamaño base (sin escalar)
        self.base_x = x
        self.base_y = y
        self.base_width = width
        self.base_height = height
        
        # Crear rect con valores actuales
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
        
        # Escala actual
        self.scale_x = 1.0
        self.scale_y = 1.0
    
    def set_scale(self, scale_x: float, scale_y: float):
        """Actualiza la escala del componente"""
        self.scale_x = scale_x
        self.scale_y = scale_y
        
        # Actualizar rect con nueva escala
        self.rect.x = int(self.base_x * scale_x)
        self.rect.y = int(self.base_y * scale_y)
        self.rect.width = int(self.base_width * scale_x)
        self.rect.height = int(self.base_height * scale_y)
    
    @abstractmethod
    def update(self, events: list, mouse_pos: Tuple[int, int]):
        pass
    
    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass
    
    def contains_point(self, pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos) if self.visible and self.enabled else False


class Button(Component):
    """Botón interactivo"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, color: Tuple[int, int, int], 
                 callback: Optional[Callable] = None):
        super().__init__(x, y, width, height)
        self.text = text
        self.color = color
        self.callback = callback
        self.hovered = False
        self.pressed = False
        self.theme = Theme()
    
    def update(self, events: list, mouse_pos: Tuple[int, int]):
        if not self.enabled:
            return
        
        self.hovered = self.contains_point(mouse_pos)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.hovered:
                    self.pressed = True
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.pressed and self.hovered and self.callback:
                    self.callback()
                self.pressed = False
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Color según estado
        color = self.color
        if not self.enabled:
            color = tuple(c // 2 for c in color)
        elif self.pressed:
            color = tuple(max(0, c - 30) for c in color)
        elif self.hovered:
            color = tuple(min(255, c + 20) for c in color)
        
        # Dibujar botón
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        
        # Borde
        border_color = tuple(min(255, c + 40) for c in color)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=10)
        
        # Texto
        text_surf = self.theme.FONT_S.render(self.text, True, self.theme.TEXT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class Label(Component):
    """Etiqueta de texto"""
    
    def __init__(self, x: int, y: int, text: str, 
                 font: pygame.font.Font = None, 
                 color: Tuple[int, int, int] = None):
        super().__init__(x, y, 0, 0)
        self.text = text
        self.theme = Theme()
        self.font = font or self.theme.FONT_S
        self.color = color or self.theme.TEXT
        self._update_size()
    
    def _update_size(self):
        surf = self.font.render(self.text, True, self.color)
        self.rect.size = surf.get_size()
    
    def set_text(self, text: str):
        self.text = text
        self._update_size()
    
    def update(self, events: list, mouse_pos: Tuple[int, int]):
        pass
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, self.rect)


class ProgressBar(Component):
    """Barra de progreso animada"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 max_value: int = 100):
        super().__init__(x, y, width, height)
        self.max_value = max_value
        self.current_value = max_value
        self.target_value = max_value
        self.theme = Theme()
    
    def set_value(self, value: int):
        self.target_value = max(0, min(value, self.max_value))
    
    def update(self, events: list, mouse_pos: Tuple[int, int]):
        # Animación suave
        if self.current_value < self.target_value:
            self.current_value = min(self.target_value, self.current_value + 2)
        elif self.current_value > self.target_value:
            self.current_value = max(self.target_value, self.current_value - 2)
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Fondo
        pygame.draw.rect(surface, self.theme.BG, self.rect, border_radius=7)
        
        # Progreso
        if self.current_value > 0:
            fill_width = int((self.current_value / self.max_value) * self.rect.width)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            
            # Color según porcentaje
            ratio = self.current_value / self.max_value
            if ratio > 0.6:
                color = self.theme.SUCCESS
            elif ratio > 0.3:
                color = self.theme.WARNING
            else:
                color = self.theme.DANGER
            
            pygame.draw.rect(surface, color, fill_rect, border_radius=7)
        
        # Borde
        pygame.draw.rect(surface, self.theme.TEXT_MUTED, self.rect, width=2, border_radius=7)


class Panel(Component):
    """Panel contenedor (Composite Pattern)"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 color: Tuple[int, int, int] = None, 
                 border_color: Tuple[int, int, int] = None):
        super().__init__(x, y, width, height)
        self.theme = Theme()
        self.bg_color = color or self.theme.BG_LIGHT
        self.border_color = border_color or self.theme.PRIMARY
        self.children: list[Component] = []
    
    def add_child(self, child: Component):
        """Añade componente hijo"""
        self.children.append(child)
    
    def remove_child(self, child: Component):
        """Elimina componente hijo"""
        if child in self.children:
            self.children.remove(child)
    
    def set_scale(self, scale_x: float, scale_y: float):
        """Escala el panel y todos sus hijos"""
        super().set_scale(scale_x, scale_y)
        for child in self.children:
            child.set_scale(scale_x, scale_y)
    
    def update(self, events: list, mouse_pos: Tuple[int, int]):
        for child in self.children:
            child.update(events, mouse_pos)
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Fondo
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=15)
        
        # Borde
        pygame.draw.rect(surface, self.border_color, self.rect, width=3, border_radius=15)
        
        # Hijos
        for child in self.children:
            child.draw(surface)


class HeroCard(Component):
    """Tarjeta de héroe con stats mejorada"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.theme = Theme()
        self.hero_name = ""
        self.hero_level = 0
        self.hero_attack = 0
        self.hero_defensa = 0
        self.hero_pv = 0
        self.hero_pv_max = 100
        self.hero_energia = 0
        self.hero_energia_max = 100
        self.is_active = False
        self.is_dead = False
        
        # Componentes internos
        self.name_label = Label(x + 10, y + 10, "", self.theme.FONT_S, self.theme.TEXT)
        self.level_label = Label(x + width - 100, y + 10, "", self.theme.FONT_XS, self.theme.TEXT_DIM)
        self.attack_label = Label(x + 10, y + 45, "", self.theme.FONT_XS, self.theme.WARNING)
        self.defense_label = Label(x + 10, y + 68, "", self.theme.FONT_XS, self.theme.PRIMARY_LIGHT)
        
        # Barras de progreso
        self.health_bar = ProgressBar(x + 10, y + height - 55, width - 20, 18)
        self.health_label = Label(x + 10, y + height - 78, "❤️ PV:", self.theme.FONT_XS, self.theme.TEXT_DIM)
        
        self.energy_bar = ProgressBar(x + 10, y + height - 28, width - 20, 15)
        self.energy_label = Label(x + width - 60, y + height - 28, "", self.theme.FONT_XS, self.theme.TEXT_MUTED)
    
    def set_hero(self, nombre: str, nivel: int, ataque: int, pv: int, pv_max: int, 
                 defensa: int = 0, energia: int = 0, energia_max: int = 100):
        """Actualiza datos del héroe con nuevas stats"""
        self.hero_name = nombre
        self.hero_level = nivel
        self.hero_attack = ataque
        self.hero_defensa = defensa
        self.hero_pv = pv
        self.hero_pv_max = pv_max
        self.hero_energia = energia
        self.hero_energia_max = energia_max
        self.is_dead = pv <= 0
        
        # Actualizar labels
        self.name_label.set_text(nombre)
        self.level_label.set_text(f"Nv.{nivel}")
        self.attack_label.set_text(f"⚔️ ATK: {ataque}")
        self.defense_label.set_text(f"🛡️ DEF: {defensa}")
        
        # Barras
        self.health_bar.max_value = pv_max
        self.health_bar.set_value(pv)
        self.energy_bar.max_value = energia_max
        self.energy_bar.set_value(energia)
        self.energy_label.set_text(f"⚡{energia}")
    
    def set_active(self, active: bool):
        """Marca como turno activo"""
        self.is_active = active
    
    def set_scale(self, scale_x: float, scale_y: float):
        """Escala la tarjeta y sus componentes internos"""
        super().set_scale(scale_x, scale_y)
        
        # Escalar componentes internos
        self.name_label.set_scale(scale_x, scale_y)
        self.level_label.set_scale(scale_x, scale_y)
        self.attack_label.set_scale(scale_x, scale_y)
        self.defense_label.set_scale(scale_x, scale_y)
        self.health_bar.set_scale(scale_x, scale_y)
        self.health_label.set_scale(scale_x, scale_y)
        self.energy_bar.set_scale(scale_x, scale_y)
        self.energy_label.set_scale(scale_x, scale_y)
    
    def update(self, events: list, mouse_pos: Tuple[int, int]):
        self.health_bar.update(events, mouse_pos)
        self.energy_bar.update(events, mouse_pos)
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Color de fondo según estado
        if self.is_dead:
            bg_color = (40, 40, 50)
            border_color = self.theme.TEXT_MUTED
        elif self.is_active:
            bg_color = self.theme.BG_LIGHT
            border_color = self.theme.PRIMARY_LIGHT
        else:
            bg_color = self.theme.BG_LIGHT
            border_color = self.theme.TEXT_MUTED
        
        # Fondo
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=12)
        
        # Borde (más grueso si está activo)
        border_width = 3 if self.is_active else 2
        pygame.draw.rect(surface, border_color, self.rect, width=border_width, border_radius=12)
        
        # Componentes internos
        self.name_label.draw(surface)
        self.level_label.draw(surface)
        self.attack_label.draw(surface)
        self.defense_label.draw(surface)
        self.health_label.draw(surface)
        self.health_bar.draw(surface)
        
        # Barra de energía con color especial (azul/cyan)
        if self.hero_energia > 0:
            # Dibujar barra de energía personalizada
            energy_rect = self.energy_bar.rect
            # Fondo
            pygame.draw.rect(surface, self.theme.BG, energy_rect, border_radius=5)
            # Progreso
            fill_width = int((self.hero_energia / self.hero_energia_max) * energy_rect.width)
            if fill_width > 0:
                fill_rect = pygame.Rect(energy_rect.x, energy_rect.y, fill_width, energy_rect.height)
                # Color cyan/azul para energía
                energy_color = (50, 180, 255)
                pygame.draw.rect(surface, energy_color, fill_rect, border_radius=5)
            # Borde
            pygame.draw.rect(surface, self.theme.TEXT_MUTED, energy_rect, width=1, border_radius=5)
        
        self.energy_label.draw(surface)
        
        # Overlay si está muerto
        if self.is_dead:
            overlay = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 0, 0, 150), overlay.get_rect(), border_radius=12)
            surface.blit(overlay, self.rect.topleft)
            
            dead_text = self.theme.FONT_M.render("💀 MUERTO", True, self.theme.DANGER)
            dead_rect = dead_text.get_rect(center=self.rect.center)
            surface.blit(dead_text, dead_rect)


class InputField(Component):
    """Campo de entrada de texto"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 placeholder: str = "", input_type: str = "text"):
        super().__init__(x, y, width, height)
        self.theme = Theme()
        self.text = ""
        self.placeholder = placeholder
        self.input_type = input_type  # "text" o "number"
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0
        self.max_length = 15 if input_type == "text" else 3
    
    def update(self, events: list, mouse_pos: Tuple[int, int]):
        # Cursor parpadeante
        self.cursor_timer += 1
        if self.cursor_timer > 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.active = self.contains_point(mouse_pos)
            
            elif event.type == pygame.KEYDOWN and self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.active = False
                elif len(self.text) < self.max_length:
                    if self.input_type == "number":
                        if event.unicode.isdigit():
                            self.text += event.unicode
                    elif event.unicode.isalnum() or event.unicode == ' ':
                        self.text += event.unicode
    
    def get_text(self) -> str:
        return self.text
    
    def clear(self):
        self.text = ""
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Fondo
        pygame.draw.rect(surface, self.theme.BG, self.rect, border_radius=8)
        
        # Borde (diferente si está activo)
        border_color = self.theme.PRIMARY if self.active else self.theme.TEXT_MUTED
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=8)
        
        # Texto
        display_text = self.text if self.text else self.placeholder
        text_color = self.theme.TEXT if self.text else self.theme.TEXT_MUTED
        
        # Añadir cursor si está activo
        if self.active and self.cursor_visible:
            display_text += "|"
        
        text_surf = self.theme.FONT_S.render(display_text, True, text_color)
        text_rect = text_surf.get_rect(midleft=(self.rect.x + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)


class MessageBox(Component):
    """Cuadro de mensaje temporal"""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y, width, height)
        self.theme = Theme()
        self.message = ""
        self.message_type = "info"  # "info", "success", "error"
        self.duration = 0
        self.visible = False
    
    def show_message(self, text: str, msg_type: str = "info", duration: int = 180):
        """Muestra un mensaje temporal (duration en frames)"""
        self.message = text
        self.message_type = msg_type
        self.duration = duration
        self.visible = True
    
    def update(self, events: list, mouse_pos: Tuple[int, int]):
        if self.visible and self.duration > 0:
            self.duration -= 1
            if self.duration <= 0:
                self.visible = False
    
    def draw(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        # Color según tipo
        if self.message_type == "success":
            color = self.theme.SUCCESS
        elif self.message_type == "error":
            color = self.theme.DANGER
        else:
            color = self.theme.PRIMARY
        
        # Fondo semi-transparente
        bg_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, (*self.theme.BG, 220), bg_surf.get_rect(), border_radius=10)
        surface.blit(bg_surf, self.rect.topleft)
        
        # Borde
        pygame.draw.rect(surface, color, self.rect, width=2, border_radius=10)
        
        # Texto
        text_surf = self.theme.FONT_S.render(self.message, True, color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
