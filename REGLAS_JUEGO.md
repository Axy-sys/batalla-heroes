# 🎮 BATALLA DE HÉROES - REGLAS DEL JUEGO

## 📋 **Resumen del Juego**

Batalla de Héroes es un juego de combate por turnos donde 4 héroes únicos luchan entre sí en una arena mágica. El último héroe en pie es declarado ganador. El juego combina elementos estratégicos con mecánicas aleatorias para crear batallas dinámicas e impredecibles.

---

## 🦸 **Estadísticas de los Héroes**

Cada héroe tiene las siguientes estadísticas:

### **Estadísticas Principales**
- **❤️ Puntos de Vida (PV)**: Vida actual del héroe
- **❤️ PV Máximo**: Vida máxima que puede tener
- **⚔️ Ataque (ATK)**: Daño base que inflige
- **🛡️ Defensa (DEF)**: Reduce el daño recibido
- **🏅 Nivel**: Nivel del héroe
- **⚡ Energía**: Recurso para habilidades especiales (max 100)

### **Estadísticas Especiales**
- **💥 Crítico**: Probabilidad de golpe crítico (+50% daño)
- **💨 Esquiva**: Probabilidad de esquivar ataques

---

## 👥 **Héroes Disponibles**

### **🏹 Artemis - La Cazadora**
- **Nivel**: 5
- **PV**: 100
- **Ataque**: 25
- **Defensa**: 8
- **Crítico**: 25%
- **Esquiva**: 15%
- **Especialidad**: Balance entre ataque y defensa

### **🧙 Merlín - El Hechicero**
- **Nivel**: 6
- **PV**: 85
- **Ataque**: 30
- **Defensa**: 5
- **Crítico**: 20%
- **Esquiva**: 12%
- **Especialidad**: Alto daño, baja defensa

### **⚡ Thor - El Dios del Trueno**
- **Nivel**: 7
- **PV**: 120
- **Ataque**: 20
- **Defensa**: 12
- **Crítico**: 15%
- **Esquiva**: 8%
- **Especialidad**: Tanque con alta resistencia

### **🌙 Shadow - El Asesino**
- **Nivel**: 5
- **PV**: 80
- **Ataque**: 35
- **Defensa**: 6
- **Crítico**: 30%
- **Esquiva**: 20%
- **Especialidad**: Alto riesgo, alto daño, muy ágil

---

## ⚔️ **Mecánicas de Combate**

### **Sistema de Turnos**
- Los héroes atacan en orden circular
- Cada héroe tiene un turno para realizar una acción
- El héroe activo tiene un borde brillante en su tarjeta

### **Acciones Disponibles**

#### **1. ⚔️ Ataque Normal (55% probabilidad)**
- Inflige daño basado en el ATK del atacante
- El daño varía aleatoriamente (±5-15)
- Puede ser un **golpe crítico** (💥 +50% daño)
- Puede ser **esquivado** (💨 0 daño)
- **Ganancia de energía**: +15

**Fórmula de daño:**
```
Daño = (ATK + variación aleatoria) × multiplicador crítico
Daño reducido = Daño × (1 - (DEF × 0.02))
```

#### **2. ✨ Habilidad Especial (IA inteligente)**
- **Costo**: 50 de energía
- Inflige **daño masivo** (ATK × 2.5 + bonus)
- **Ignora la defensa** del objetivo
- Puede ser esquivada
- Solo se usa cuando:
  - El héroe tiene ≥50 energía
  - Hay un enemigo con <60 PV
  - 40% de probabilidad si se cumplen las condiciones

**Fórmula:**
```
Daño = (ATK × 2.5) + variación (20-40)
```

#### **3. 💚 Curación (25% probabilidad)**
- Restaura vida al héroe
- Aumenta si está por debajo del 40% de vida (60% probabilidad)
- **Ganancia de energía**: +10

**Fórmula:**
```
Curación = 15 + (Nivel × 5) + variación (5-20)
```

#### **4. ⏭️ Pasar Turno (20% probabilidad)**
- Regenera energía masivamente
- Recupera vida pasivamente
- **Ganancia de energía**: +25
- **Curación pasiva**: 5% de PV máximo

---

## 🎯 **Mecánicas Avanzadas**

### **💥 Golpe Crítico**
- Cada héroe tiene una probabilidad de crítico
- Los críticos infligen **+50% de daño**
- Se muestra con el ícono 💥 en el log

### **💨 Esquiva**
- Probabilidad de evitar completamente un ataque
- Funciona contra ataques normales y habilidades
- Se muestra con el ícono 💨 en el log

### **🛡️ Defensa**
- Reduce el daño recibido de ataques normales
- **Fórmula**: Reducción = DEF × 2% (máximo 70%)
- No afecta a las habilidades especiales

### **⚡ Sistema de Energía**
- Comienza en 0
- Se gana al realizar acciones:
  - Atacar: +15
  - Curar: +10
  - Pasar: +25
- Máximo: 100
- Se usa para habilidades especiales (costo: 50)

---

## 🎲 **IA y Estrategia**

El sistema de IA toma decisiones inteligentes:

1. **Prioridad a habilidad especial** si:
   - Tiene ≥50 energía
   - Hay enemigo con <60 PV
   - 40% de probabilidad

2. **Prioridad a curación** si:
   - PV < 40% de PV máximo
   - 60% de probabilidad

3. **Distribución normal**:
   - 55% Atacar
   - 25% Curar
   - 20% Pasar (regenerar energía)

---

## 📊 **Estadísticas de Batalla**

Durante y después de la batalla, se rastrean:
- **⚔️ Ataques totales**: Número de ataques realizados
- **💥 Críticos**: Número de golpes críticos
- **💨 Esquivas**: Número de ataques esquivados
- **✨ Habilidades**: Número de habilidades especiales usadas
- **🩸 Daño total**: Daño total infligido
- **💚 Curaciones**: Número de curaciones
- **Salud restaurada**: PV total recuperados

---

## 🏆 **Condiciones de Victoria**

- La batalla termina cuando solo queda **1 héroe vivo**
- El último héroe en pie es declarado **ganador**
- Se muestran las estadísticas finales
- El ganador recibe la corona 👑

---

## 🎮 **Controles del Juego**

### **Durante la Batalla**
- **▶ Siguiente**: Avanza al siguiente turno manualmente
- **⏸️ Pausa**: Pausa/Reanuda el modo automático
- **🏠 Menú**: Vuelve al menú principal
- **ESPACIO**: Atajo para pausar/reanudar
- **ESC**: Vuelve al menú principal

### **Menú Principal**
- **⚔️ Iniciar Batalla**: Batalla estándar (5 rondas)
- **🎲 Batalla Personalizada**: Batalla extendida (10 rondas)
- **🧪 Modo Prueba**: Gestiona héroes personalizados
- **❌ Salir**: Cierra el juego
- **F11**: Pantalla completa

---

## 🎨 **Elementos de UI**

### **Tarjeta de Héroe**
- **Nombre y Nivel**: Esquina superior
- **⚔️ ATK**: Ataque del héroe
- **🛡️ DEF**: Defensa del héroe
- **❤️ Barra de vida**: 
  - Verde: >60% vida
  - Amarillo: 30-60% vida
  - Rojo: <30% vida
- **⚡ Barra de energía**: Barra azul/cyan (0-100)
- **Borde brillante**: Indica turno activo
- **💀 Overlay**: Héroe muerto

### **Panel de Log**
- Muestra los últimos 8 eventos
- Íconos para cada tipo de acción:
  - ⚔️ Ataque normal
  - 💥 Golpe crítico
  - ✨ Habilidad especial
  - 💨 Esquiva
  - 💚 Curación
  - ⏭️ Pasar turno
  - 💀 Muerte

### **Panel de Estadísticas**
- Actualización en tiempo real
- Muestra todas las métricas de combate
- Borde rosa/magenta distintivo

---

## 🔧 **Modo Prueba**

Permite crear y gestionar héroes personalizados:
- **➕ Agregar**: Crear nuevo héroe
- **🗑️ Eliminar**: Eliminar por nombre
- **🔍 Buscar**: Buscar héroe específico
- **⬆️ Mejorar**: Aumentar nivel (+10 PV, +5 ATK, +1 DEF)
- **⚔️ Batalla**: Iniciar batalla con héroes personalizados

---

## 💡 **Estrategias y Consejos**

1. **Gestión de Energía**: Pasar turno cuando necesites energía para una habilidad especial
2. **Timing de Habilidades**: Usa habilidades contra enemigos debilitados para garantizar eliminaciones
3. **Balance de Stats**: 
   - **Alta defensa** = mayor supervivencia
   - **Alto ataque** = eliminaciones rápidas
   - **Alta esquiva** = estilo arriesgado pero efectivo
4. **Curación Preventiva**: Cura antes de estar crítico
5. **Observa Patrones**: La IA toma decisiones basadas en estadísticas

---

## 🌟 **Características Especiales**

- ✅ **Ventana redimensionable**: Arrastra los bordes
- ✅ **Pantalla completa**: Presiona F11
- ✅ **Escalado responsivo**: Se adapta a cualquier resolución
- ✅ **Emojis**: Soporte completo para iconos emoji
- ✅ **Arquitectura modular**: Diseño profesional con patrones de diseño
- ✅ **Auto-play**: Modo automático con pausa manual
- ✅ **Animaciones suaves**: Barras de vida animadas

---

## 📈 **Niveles y Progresión**

Al mejorar un héroe (Modo Prueba):
- **Nivel +1**
- **PV Max +10**
- **PV actual +10** (sin exceder máximo)
- **Ataque +5**
- **Defensa +1**
- **Crítico +2%** (máximo 50%)

---

## 🎯 **Balance del Juego**

El juego está balanceado para que:
- Ningún héroe sea dominante
- La suerte juega un rol (esquivas, críticos)
- La estrategia importa (cuándo usar habilidades)
- Batallas duren 20-40 turnos aproximadamente
- Haya oportunidades de comeback (regeneración de energía)

---

## 🐛 **Versión**

**v3.0 - Edición Modular Mejorada**
- Sistema de energía y habilidades especiales
- Mecánicas de crítico y esquiva
- IA mejorada con decisiones inteligentes
- UI/UX completamente rediseñada
- Estadísticas expandidas
- Sistema de defensa
- Arquitectura modular con patrones de diseño

---

**¡Disfruta del juego y que gane el mejor héroe! ⚔️🏆**
