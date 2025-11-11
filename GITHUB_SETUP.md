# 🚀 Guía para Subir a GitHub

## 📋 Pasos para conectar con GitHub

### 1. Crear Repositorio en GitHub

1. Ve a [GitHub](https://github.com)
2. Inicia sesión en tu cuenta
3. Haz clic en el botón **"New"** (verde) o en el **"+"** en la esquina superior derecha
4. Completa:
   - **Repository name**: `batalla-heroes`
   - **Description**: "🎮 Juego de combate por turnos con arquitectura modular profesional"
   - **Public** o **Private** (tu elección)
   - ❌ NO marques "Initialize with README" (ya lo tenemos)
5. Haz clic en **"Create repository"**

### 2. Conectar Repositorio Local con GitHub

Después de crear el repositorio, GitHub te mostrará comandos. Usa estos:

```powershell
# Agregar el remoto (reemplaza 'TU_USUARIO' con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/batalla-heroes.git

# Renombrar la rama principal a 'main' (convención moderna)
git branch -M main

# Subir el código
git push -u origin main
```

### 3. Comandos Completos (Copiar y Pegar)

```powershell
# En PowerShell, desde la carpeta del proyecto:

# 1. Agregar remoto (CAMBIA TU_USUARIO por tu usuario real)
git remote add origin https://github.com/TU_USUARIO/batalla-heroes.git

# 2. Verificar que se agregó correctamente
git remote -v

# 3. Cambiar rama a 'main'
git branch -M main

# 4. Subir código
git push -u origin main
```

### 4. Autenticación

Si es tu primera vez usando Git con GitHub:

#### Opción A: HTTPS (Recomendado para principiantes)
- GitHub te pedirá credenciales
- Usa tu **Personal Access Token** (no tu contraseña)
- Crear token en: Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token

#### Opción B: SSH (Más seguro, usuarios avanzados)
```powershell
# Generar clave SSH (si no tienes)
ssh-keygen -t ed25519 -C "tu_email@example.com"

# Copiar clave pública
Get-Content ~/.ssh/id_ed25519.pub | clip

# Agregar en GitHub: Settings → SSH and GPG keys → New SSH key
# Pegar la clave copiada

# Cambiar URL remota a SSH
git remote set-url origin git@github.com:TU_USUARIO/batalla-heroes.git
```

---

## 📦 Flujo de Trabajo Git

### Hacer cambios y subirlos

```powershell
# 1. Verificar cambios
git status

# 2. Agregar archivos modificados
git add .

# 3. Hacer commit con mensaje descriptivo
git commit -m "✨ feat: Descripción del cambio"

# 4. Subir a GitHub
git push
```

### Tipos de commits (Convenciones)

| Prefijo | Uso | Ejemplo |
|---------|-----|---------|
| `✨ feat:` | Nueva característica | `✨ feat: Agregar sistema de niveles` |
| `🐛 fix:` | Corrección de bug | `🐛 fix: Corregir error en esquiva` |
| `📚 docs:` | Documentación | `📚 docs: Actualizar README` |
| `🎨 style:` | Formato/estilo | `🎨 style: Mejorar UI del menú` |
| `♻️ refactor:` | Refactorización | `♻️ refactor: Optimizar motor de combate` |
| `⚡ perf:` | Mejora de rendimiento | `⚡ perf: Optimizar renderizado` |
| `✅ test:` | Agregar tests | `✅ test: Tests para HeroFactory` |
| `🔧 chore:` | Mantenimiento | `🔧 chore: Actualizar dependencias` |

---

## 🌿 Trabajar con Branches (Ramas)

### Crear y usar ramas

```powershell
# Crear nueva rama para feature
git checkout -b feature/nueva-caracteristica

# Ver ramas
git branch

# Cambiar de rama
git checkout main

# Fusionar rama
git merge feature/nueva-caracteristica

# Subir rama a GitHub
git push origin feature/nueva-caracteristica
```

### Estrategia de branches sugerida

```
main (o master)           ← Código estable, siempre funcional
  ├── develop             ← Desarrollo activo
  │   ├── feature/heroes  ← Nueva característica
  │   └── feature/items   ← Otra característica
  └── hotfix/bug-critico  ← Correcciones urgentes
```

---

## 📊 Verificar Estado

```powershell
# Ver estado de archivos
git status

# Ver historial de commits
git log --oneline --graph --all

# Ver cambios no commiteados
git diff

# Ver remotos configurados
git remote -v
```

---

## 🔄 Actualizar desde GitHub

```powershell
# Descargar cambios (sin aplicar)
git fetch

# Descargar y fusionar cambios
git pull

# O específicamente desde main
git pull origin main
```

---

## 🎯 Configuración Recomendada

### Archivo .gitattributes (para evitar problemas con line endings)

Crear archivo `.gitattributes` en la raíz:

```
* text=auto
*.py text eol=lf
*.md text eol=lf
*.json text eol=lf
*.yml text eol=lf
```

### Configuración global útil

```powershell
# Configurar nombre y email (si no lo has hecho)
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@example.com"

# Colorear la salida de Git
git config --global color.ui auto

# Editor por defecto (VS Code)
git config --global core.editor "code --wait"

# Alias útiles
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.cm commit
git config --global alias.lg "log --oneline --graph --all"
```

---

## 🚨 Solución de Problemas Comunes

### Error: "fatal: remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/batalla-heroes.git
```

### Error: Authentication failed
- Asegúrate de usar un **Personal Access Token** en vez de tu contraseña
- Genéralo en: GitHub → Settings → Developer settings → Personal access tokens

### Deshacer último commit (sin perder cambios)
```powershell
git reset --soft HEAD~1
```

### Deshacer cambios no commiteados
```powershell
# Archivo específico
git checkout -- archivo.py

# Todos los archivos
git checkout -- .
```

### Ver diferencias entre commits
```powershell
git diff HEAD~1 HEAD
```

---

## 📁 Estructura Recomendada en GitHub

```
batalla-heroes/
├── .github/
│   ├── workflows/          # GitHub Actions (CI/CD)
│   └── ISSUE_TEMPLATE/     # Templates para issues
├── docs/                   # Documentación adicional
│   ├── ARQUITECTURA_MODULAR.md
│   ├── README_MODULAR.md
│   └── REGLAS_JUEGO.md
├── src/                    # Código fuente (opcional, reorganizar)
│   ├── game_core.py
│   ├── game_main.py
│   ├── game_screens.py
│   └── ui_components.py
├── tests/                  # Tests unitarios
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 🏷️ Crear Releases

### En GitHub

1. Ve a tu repositorio
2. Click en **"Releases"** → **"Create a new release"**
3. Completa:
   - **Tag**: `v3.0.0`
   - **Title**: `🎮 Batalla de Héroes v3.0 - Edición Modular`
   - **Description**: Copiar del CHANGELOG
4. Click en **"Publish release"**

### Desde la terminal

```powershell
# Crear tag
git tag -a v3.0.0 -m "🎮 Release v3.0.0 - Edición Modular"

# Subir tag
git push origin v3.0.0
```

---

## 📝 Ejemplo Completo: Tu Primera Subida

```powershell
# 1. Navegar a la carpeta del proyecto
cd C:\Users\kiwic\Documents\Datos

# 2. Verificar que todo está commiteado
git status

# 3. Agregar remoto de GitHub (CAMBIA TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/batalla-heroes.git

# 4. Cambiar a rama main
git branch -M main

# 5. Subir código
git push -u origin main

# ¡Listo! 🎉
```

---

## 🎯 Próximos Pasos

Después de subir:

1. ✅ Agregar descripción y topics en GitHub
2. ✅ Crear archivo LICENSE (MIT recomendado)
3. ✅ Agregar badges al README
4. ✅ Configurar GitHub Pages para documentación
5. ✅ Agregar screenshots/GIFs
6. ✅ Crear issues para futuras features
7. ✅ Configurar GitHub Actions para CI/CD

---

## 📸 Agregar Screenshots

Crear carpeta `assets/` o `screenshots/`:

```powershell
mkdir assets
# Agregar imágenes
git add assets/
git commit -m "📸 docs: Agregar screenshots del juego"
git push
```

En README.md:
```markdown
![Batalla en progreso](assets/batalla.png)
```

---

## 🌟 Hacer el Proyecto Destacable

### Agregar al README principal:

```markdown
## 🌟 Características Destacadas

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5.0-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

[Demo en vivo] [Documentación] [Reportar Bug] [Solicitar Feature]
```

---

¡Tu proyecto ahora está listo para brillar en GitHub! 🚀✨
