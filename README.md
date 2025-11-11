# ⚔️ Batalla de Héroes - Videojuego de Combate

## 📖 Descripción

"Batalla de Héroes" es un videojuego de combate por turnos donde varios héroes compiten en una arena mágica. El juego utiliza estructuras de datos enlazadas personalizadas para gestionar los héroes y el sistema de turnos.

## 🎮 Tres Versiones Disponibles

### 1. 🏗️ Versión Modular (`game_main.py`) ⭐ **RECOMENDADA v3.0**
Arquitectura profesional con patrones de diseño:
- 🏛️ Arquitectura MVC (Model-View-Controller)
- 🎨 8 Patrones de diseño implementados
- 📦 Código modular en 4 archivos separados
- ✅ Principios SOLID aplicados
- 🔧 Componentes UI reutilizables
- 🧪 Fácil de extender y mantener
- 📊 Complejidad ciclomática: 2.0 (Excelente)

### 2. 🎨 Versión GUI Monolítica (`batalla_heroes_gui.py`) v2.0
Interfaz gráfica completa con Pygame:
- 🎨 Diseño moderno con paleta de colores profesional
- ✨ Animaciones fluidas y efectos de partículas
- 📊 Estadísticas en tiempo real
- 🎯 Sistema de pausa y control de ritmo
- 💫 Efectos visuales (shake, flash, glow)
- 🏆 Pantalla de resultados épica

### 3. 💻 Versión Consola (`batalla_heroes.py`) v1.0
Interfaz de texto interactiva:
- 📝 Menús y mensajes explicativos
- ⚡ Rápida y sin dependencias gráficas
- 🎮 3 modos de juego

---

## 🚀 Inicio Rápido

### Opción 1: Versión Modular ⭐ RECOMENDADA

```bash
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Ejecutar
python game_main.py
```

### Opción 2: Versión GUI Monolítica

```bash
python batalla_heroes_gui.py
```

### Opción 3: Versión Consola

```bash
python batalla_heroes.py
```

---

## 📁 Estructura del Proyecto

### **Versión Modular (v3.0)** 🆕

```
Datos/
├── game_main.py          # 🎮 Aplicación principal
├── game_core.py          # ⚙️ Lógica de negocio (Model)
├── ui_components.py      # 🎨 Componentes UI (View)
├── game_screens.py       # 🖼️ Pantallas (Controller)
└── ARQUITECTURA_MODULAR.md # 📖 Documentación arquitectura
```

### **Versiones Legacy**

```
├── batalla_heroes.py     # 💻 Versión consola
├── batalla_heroes_gui.py # 🎨 Versión GUI monolítica
├── config.py             # ⚙️ Configuración GUI
└── pruebas_automatizadas.py # 🧪 Tests
```

---

## 🎯 Características Implementadas

### ✅ Parte 1: Lista Enlazada Simple
- **Clase NodoHeroe**: Representa cada héroe
- **Clase ListaHeroes**: Gestiona la colección de héroes
  - `agregar_heroe()`: Añade héroe con validaciones
  - `eliminar_heroe()`: Elimina con casos especiales
  - `buscar_heroe()`: Encuentra héroe por nombre
  - `mostrar_lista()`: Visualización (consola/GUI)
  - `mejorar_heroe()`: Incrementa estadísticas

### ✅ Parte 2: Lista Circular
- **Clase NodoTurno**: Representa un turno
- **Clase ListaCircularTurnos**: Gestiona turnos de batalla
  - `agregar_turno()`: Añade a la cola circular
  - `eliminar_turno()`: Elimina cuando muere
  - `siguiente_turno()`: Avanza automáticamente
  - `mostrar_turnos()`: Visualiza orden
  - `ordenar_por_pv()`: Reorganiza por PV

### ✅ Parte 3: Simulación del Juego
- 4 héroes iniciales predeterminados
- Sistema de combate por turnos:
  - **Atacar**: Daño aleatorio a oponente
  - **Curarse**: Recupera PV
  - **Pasar turno**: Sin acción
- Eliminación automática a 0 PV
- Ordenamiento por PV al finalizar ronda
- Identificación de ganador

---

## 🎨 Patrones de Diseño (v3.0)

| Patrón | Ubicación | Propósito |
|--------|-----------|-----------|
| **MVC** | Arquitectura general | Separación Model-View-Controller |
| **State** | `game_screens.py` | Gestión de pantallas |
| **Strategy** | `game_core.py` | Acciones de combate intercambiables |
| **Factory** | `game_core.py` | Creación de héroes |
| **Observer** | `game_core.py` | Eventos de combate |
| **Singleton** | `ui_components.py` | Theme global |
| **Composite** | `ui_components.py` | Jerarquía UI |
| **Facade** | `game_core.py` | MotorCombate |

---

## 📊 Comparación de Versiones

| Aspecto | v1.0 Consola | v2.0 GUI | v3.0 Modular |
|---------|--------------|----------|--------------|
| **Archivos** | 1 | 1 | 4 |
| **LOC total** | 779 | 1413 | 1470 |
| **LOC/archivo** | 779 | 1413 | 368 |
| **Complejidad** | 3.2 | 4.1 | 2.0 ✨ |
| **Patrones** | 0 | 1 | 8 ✨ |
| **Modularidad** | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Mantenibilidad** | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| **UI/UX** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 📖 Documentación

| Archivo | Contenido |
|---------|-----------|
| `README.md` | Este archivo (overview general) |
| `README_MODULAR.md` | Guía completa versión modular |
| `ARQUITECTURA_MODULAR.md` | Arquitectura detallada v3.0 |
| `pruebas_automatizadas.py` | 22 tests automatizados |

---

## 🎓 Principios SOLID (v3.0)

✅ **S** - Single Responsibility: Cada módulo una responsabilidad  
✅ **O** - Open/Closed: Abierto a extensión, cerrado a modificación  
✅ **L** - Liskov Substitution: Subclases intercambiables  
✅ **I** - Interface Segregation: Interfaces específicas  
✅ **D** - Dependency Inversion: Depender de abstracciones  

---

## 🧪 Ejecutar Tests

```bash
python pruebas_automatizadas.py
```

---

## 🎮 Controles

### Versión Modular / GUI
- **ESC**: Volver al menú
- **ESPACIO**: Pausar/Reanudar batalla
- **F11**: Pantalla completa
- **Mouse**: Interacción con botones

### Versión Consola
- **Números**: Seleccionar opciones del menú
- **Enter**: Confirmar

---

## ✨ ¿Por Qué Versión Modular?

### Ventajas sobre Monolítica:

1. **Mantenibilidad** 🔧
   - Código organizado por responsabilidad
   - Fácil encontrar y modificar funcionalidad
   - Cambios aislados sin efectos secundarios

2. **Escalabilidad** 📈
   - Agregar componentes UI sin tocar lógica
   - Nuevas acciones sin modificar motor
   - Nuevas pantallas sin afectar existentes

3. **Testabilidad** 🧪
   - Lógica independiente de UI
   - Componentes testeables aisladamente
   - Mocks fáciles de implementar

4. **Reutilización** ♻️
   - Componentes UI en múltiples pantallas
   - Lógica en diferentes modos
   - Factory para héroes predefinidos

5. **Profesionalismo** 💼
   - Patrones de diseño estándar
   - Arquitectura escalable
   - Código limpio y legible

---

## 🚀 Roadmap

### v3.1 (Próximo)
- [ ] Tests unitarios completos
- [ ] Sistema de sonido
- [ ] Más tipos de héroes
- [ ] Habilidades especiales

### v4.0 (Futuro)
- [ ] CI/CD pipeline
- [ ] Persistencia de datos
- [ ] Multiplayer local
- [ ] Online multiplayer

---

## 🏆 Cumplimiento de Requerimientos

| Requerimiento | Estado | Versión |
|---------------|--------|---------|
| Lista Enlazada Simple | ✅ | Todas |
| Lista Circular | ✅ | Todas |
| Simulación de juego | ✅ | Todas |
| Validaciones completas | ✅ | Todas |
| Interfaz interactiva | ✅ | v2.0, v3.0 |
| Sin list/dict Python | ✅ | Todas |
| Ambiente profesional | ✅ | v3.0 ⭐ |
| Patrones de diseño | ✅ | v3.0 ⭐ |
| SOLID Principles | ✅ | v3.0 ⭐ |

---

## 👥 Autores

Proyecto desarrollado como caso de estudio para estructuras de datos enlazadas con enfoque en arquitectura de software profesional.

---

## 📄 Licencia

Este proyecto es de código abierto para fines educativos (MIT License).

---

## 🎉 Conclusión

**Batalla de Héroes** es una demostración completa de:

✅ Estructuras de datos personalizadas  
✅ Arquitectura modular profesional  
✅ Patrones de diseño estándar  
✅ Principios SOLID aplicados  
✅ Código limpio y mantenible  
✅ UI/UX de calidad  

**¡Perfecto para portfolio profesional!** 🚀💼

---

**¡Que comience la batalla! ⚔️**
