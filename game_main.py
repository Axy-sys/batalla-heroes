"""
🎮 BATALLA DE HÉROES - MAIN APPLICATION
Aplicación principal con gestión de estados
"""

import pygame
import sys
from typing import Dict, Optional
from game_screens import *


# ============================================================================
# CONTROLADOR DE APLICACIÓN (Application Controller Pattern)
# ============================================================================

class GameApp:
    """Controlador principal de la aplicación"""
    
    def __init__(self, width: int = 1366, height: int = 768):
        # Inicializar Pygame
        pygame.init()
        
        # Obtener tamaño de pantalla disponible
        display_info = pygame.display.Info()
        max_width = display_info.current_w
        max_height = display_info.current_h
        
        # Configuración de ventana (ajustar al 90% del tamaño de pantalla si es muy grande)
        self.base_width = 1366
        self.base_height = 768
        
        # Si la pantalla es más pequeña, ajustar
        if max_width < width or max_height < height:
            # Escalar al 90% del tamaño disponible
            scale = min(max_width * 0.9 / width, max_height * 0.9 / height)
            width = int(width * scale)
            height = int(height * scale)
        
        self.width = width
        self.height = height
        self.scale_x = width / self.base_width
        self.scale_y = height / self.base_height
        
        # Crear ventana redimensionable
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption("⚔️ Batalla de Héroes - Edición Modular")
        
        # Reloj para FPS
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Estado del juego
        self.running = True
        self.current_state: Optional[GameState] = None
        self.states: Dict[str, type] = {
            'menu': MenuState,
            'battle': BattleState,
            'results': ResultsState,
            'test': TestState,
            'custom': BattleState  # Usa el mismo estado pero con parámetros diferentes
        }
        
        # Iniciar en el menú
        self.change_state('menu')
    
    def change_state(self, state_name: str, **kwargs):
        """Cambia el estado actual (State Pattern)"""
        if state_name not in self.states:
            print(f"⚠️ Estado '{state_name}' no existe")
            return
        
        # Salir del estado actual
        if self.current_state:
            self.current_state.exit()
        
        # Crear nuevo estado
        StateClass = self.states[state_name]
        
        # Pasar parámetros adicionales si es batalla personalizada
        if state_name == 'custom':
            kwargs.setdefault('num_rondas', 10)
        
        self.current_state = StateClass(self, **kwargs)
        self.current_state.enter()
    
    def quit(self):
        """Termina la aplicación"""
        self.running = False
    
    def run(self):
        """Bucle principal del juego"""
        while self.running:
            # Manejar eventos
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        # Toggle fullscreen
                        pygame.display.toggle_fullscreen()
                elif event.type == pygame.VIDEORESIZE:
                    # Manejar redimensionamiento de ventana
                    self.width = event.w
                    self.height = event.h
                    self.scale_x = event.w / self.base_width
                    self.scale_y = event.h / self.base_height
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    
                    # Notificar al estado actual sobre el cambio de tamaño
                    if self.current_state and hasattr(self.current_state, 'on_resize'):
                        self.current_state.on_resize(event.w, event.h)
            
            # Actualizar estado actual
            if self.current_state:
                self.current_state.handle_events(events)
                self.current_state.update()
            
            # Renderizar
            if self.current_state:
                self.current_state.render(self.screen)
            
            # Actualizar pantalla
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        # Limpiar
        pygame.quit()
        sys.exit()


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

def main():
    """Función principal"""
    print("="*70)
    print("🎮 BATALLA DE HÉROES - EDICIÓN MODULAR")
    print("="*70)
    print("\n✨ Características:")
    print("  • Arquitectura modular con separación de responsabilidades")
    print("  • Patrones de diseño: MVC, State, Factory, Observer, Singleton")
    print("  • Componentes UI reutilizables")
    print("  • Sistema de combate configurable")
    print("  • Interfaz intuitiva y profesional")
    print("\n🎮 Controles:")
    print("  • ESC - Volver al menú")
    print("  • ESPACIO - Pausar/Reanudar batalla")
    print("  • F11 - Pantalla completa")
    print("  • Redimensionar ventana - Ajusta automáticamente la interfaz")
    print("\n🚀 Iniciando juego...\n")
    
    # Crear y ejecutar aplicación
    app = GameApp()
    app.run()


if __name__ == "__main__":
    main()
