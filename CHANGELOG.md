# 📝 Changelog

Todos los cambios notables del proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [3.0.0] - 2025-11-10 🎮 **EDICIÓN MODULAR**

### ✨ Agregado
- **Arquitectura modular profesional** con separación MVC
- **8 patrones de diseño** implementados:
  - MVC (Model-View-Controller)
  - State Pattern para pantallas
  - Strategy Pattern para acciones
  - Factory Pattern para héroes
  - Observer Pattern para eventos
  - Singleton Pattern para tema
  - Composite Pattern para UI
  - Facade Pattern para motor

### 🎯 Nuevas Mecánicas de Combate
- **Sistema de energía** (0-100) para habilidades
- **Habilidades especiales** con daño masivo (costo: 50 energía)
- **Sistema de críticos** (15-30% probabilidad, +50% daño)
- **Sistema de esquiva** (8-20% probabilidad)
- **Sistema de defensa** (reduce daño recibido)
- **Regeneración pasiva** al pasar turno (5% PV + 25 energía)
- **IA mejorada** con decisiones estratégicas

### 🎨 Mejoras de UI/UX
- **Tarjetas de héroe mejoradas** con más información
- **Barra de energía** visual (cyan/azul)
- **Log de batalla enriquecido** con iconos contextuales
- **Panel de estadísticas expandido** (críticos, esquivas, habilidades)
- **Sistema de escalado responsivo** completo
- **Soporte completo para emojis** en todas las fuentes

### 📊 Nuevas Estadísticas
- Trackeo de críticos
- Trackeo de esquivas
- Trackeo de habilidades especiales
- Estadísticas detalladas en resultados

### 🦸 Héroes Balanceados
- **Artemis**: Cazadora balanceada (crítico 25%, esquiva 15%, defensa 8)
- **Merlín**: Hechicero de alto daño (crítico 20%, esquiva 12%, defensa 5)
- **Thor**: Tanque resistente (crítico 15%, esquiva 8%, defensa 12)
- **Shadow**: Asesino ágil (crítico 30%, esquiva 20%, defensa 6)

### 📚 Documentación
- `ARQUITECTURA_MODULAR.md` - Documentación completa de arquitectura
- `README_MODULAR.md` - Guía de usuario para versión modular
- `REGLAS_JUEGO.md` - Reglas detalladas del juego
- `GITHUB_SETUP.md` - Guía para configurar y subir a GitHub
- `CHANGELOG.md` - Este archivo

### 🔧 Mejoras Técnicas
- **Complejidad ciclomática reducida**: 4.1 → 2.0
- **Código modular**: 1413 líneas → 4 archivos de ~368 líneas cada uno
- **Principios SOLID aplicados** en toda la arquitectura
- **Componentes UI reutilizables** con Composite Pattern
- **Sistema de escalado** para diferentes resoluciones

### 🎮 Características de Ventana
- Ventana redimensionable
- Modo pantalla completa (F11)
- Adaptación automática a diferentes pantallas
- Fuentes escalables dinámicamente

---

## [2.0.0] - 2025-11-09 🎨 **VERSIÓN GUI MONOLÍTICA**

### ✨ Agregado
- **Interfaz gráfica completa** con Pygame
- **Diseño moderno** con paleta de colores profesional
- **Animaciones fluidas** y efectos visuales
- **Sistema de pausa** y control de ritmo
- **Pantalla de resultados** con estadísticas

### 🎨 Elementos Visuales
- Degradados y efectos de glow
- Animaciones de barras de vida
- Efectos de partículas
- Screen shake en eventos importantes
- Transiciones suaves entre pantallas

### 🎯 Funcionalidades
- Modo batalla estándar (5 rondas)
- Modo batalla personalizada (10 rondas)
- Modo prueba para gestión de héroes
- Sistema de turnos visual
- Log de batalla en tiempo real

### 📊 Estadísticas
- Ataques totales
- Daño total infligido
- Curaciones totales
- Salud restaurada

---

## [1.0.0] - 2025-11-08 💻 **VERSIÓN CONSOLA**

### ✨ Agregado - Funcionalidad Base
- **Lista Enlazada Simple** para gestión de héroes
- **Lista Circular** para sistema de turnos
- **Sistema de combate** por turnos básico
- **3 modos de juego**:
  - Modo batalla estándar
  - Modo prueba (gestión de héroes)
  - Modo batalla personalizada

### 🦸 Características de Héroes
- 4 héroes predefinidos iniciales
- Estadísticas base: PV, Nivel, Ataque
- Sistema de mejora de héroes

### ⚔️ Mecánicas de Combate Básicas
- Atacar (daño aleatorio)
- Curarse (recuperación de PV)
- Pasar turno
- Eliminación automática a 0 PV
- Ordenamiento por PV al final de ronda

### 🎮 Interfaz de Consola
- Menús interactivos
- Validaciones de entrada
- Mensajes explicativos
- Visualización de lista de héroes
- Log de batalla en texto

### 🧪 Testing
- 22 pruebas automatizadas
- Validación de casos límite
- Tests de estructuras de datos

### 📋 Cumplimiento de Requisitos
- ✅ Lista Enlazada Simple implementada
- ✅ Lista Circular implementada
- ✅ Simulación de juego funcional
- ✅ Sin uso de list/dict de Python
- ✅ Validaciones completas

---

## Tipos de Cambios

- **✨ Agregado** - Nuevas características
- **🔧 Cambiado** - Cambios en funcionalidad existente
- **❌ Eliminado** - Características removidas
- **🐛 Corregido** - Corrección de bugs
- **🔒 Seguridad** - Vulnerabilidades corregidas
- **📚 Documentación** - Cambios en documentación
- **🎨 Estilo** - Cambios de formato/estilo
- **⚡ Rendimiento** - Mejoras de performance
- **♻️ Refactorización** - Cambios en código sin afectar funcionalidad

---

## [Unreleased] - Próximas Versiones

### 🚀 v3.1.0 (Planificado)
- [ ] Tests unitarios completos para todos los módulos
- [ ] Sistema de sonido y efectos de audio
- [ ] Más tipos de héroes jugables
- [ ] Habilidades especiales únicas por héroe
- [ ] Sistema de items/equipamiento
- [ ] Tutorial interactivo para nuevos jugadores

### 🌟 v4.0.0 (Futuro)
- [ ] Persistencia de datos (guardar/cargar partidas)
- [ ] Sistema de niveles y experiencia
- [ ] Multiplayer local (hot-seat)
- [ ] Modo historia con campañas
- [ ] Editor de héroes avanzado
- [ ] Sistema de logros/achievements

### 🔮 v5.0.0 (Visión a Largo Plazo)
- [ ] Multiplayer online
- [ ] Ranking global
- [ ] Torneos automatizados
- [ ] Cliente-Servidor arquitectura
- [ ] Base de datos para persistencia
- [ ] API REST para extensiones

---

## Notas de Versión

### Convención de Versionado

El proyecto sigue [Semantic Versioning](https://semver.org/lang/es/):

- **MAJOR** (X.0.0): Cambios incompatibles con versiones anteriores
- **MINOR** (0.X.0): Nuevas funcionalidades compatibles con versiones anteriores
- **PATCH** (0.0.X): Correcciones de bugs compatibles

### Links de Comparación

- [3.0.0 vs 2.0.0](./docs/comparison_v3_v2.md) - Cambios arquitectónicos mayores
- [2.0.0 vs 1.0.0](./docs/comparison_v2_v1.md) - De consola a GUI

---

## Agradecimientos

- Comunidad de Pygame por el excelente framework
- Patrones de diseño Gang of Four
- Principios SOLID de Robert C. Martin
- Convenciones de Conventional Commits

---

**Última actualización**: 10 de noviembre de 2025
