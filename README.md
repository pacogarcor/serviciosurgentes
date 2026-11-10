# serviciosurgentes.es

Directorio estático de servicios urgentes por provincia (52 provincias × 8 servicios).

## Estructura
- `index.html` – portada con buscador, desplegable de provincias en el menú y cuadrante de provincias.
- `provincias/<slug>.html` – una página por provincia con 8 cajas (imagen, WhatsApp y web).
- `data/empresas.json` – **aquí se editan las empresas** (nombre, whatsapp, web, imagen) de cada provincia y servicio.
- `data/servicios.json` / `data/provincias.json` – listado de servicios y provincias.
- `build.py` – genera todas las páginas a partir de los datos.

## Añadir o cambiar una empresa
1. Edita `data/empresas.json`, por ejemplo:
   ```json
   "madrid": {
     "cerrajeros": {
       "nombre": "Cerrajería Ejemplo Madrid",
       "whatsapp": "34611222333",
       "web": "https://www.ejemplo.es",
       "imagen": "img/empresas/cerrajeria-ejemplo.jpg"
     }
   }
   ```
   - `whatsapp`: número con prefijo de país, sin `+` ni espacios.
   - `imagen`: ruta dentro del proyecto (p. ej. `img/empresas/...`) o URL completa. Si se deja vacía se usa la imagen genérica del servicio.
   - Mientras una plaza no tenga WhatsApp ni web aparece como **«Plaza disponible»** con los botones desactivados.
2. Ejecuta `python3 build.py`.
3. Haz commit y push: Vercel publica automáticamente.

## Publicar en Vercel
Importa el repositorio en Vercel como proyecto estático (Framework: *Other*, sin comando de build, directorio raíz `/`). `vercel.json` activa las URLs limpias (`/provincias/madrid`).
