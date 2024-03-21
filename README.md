# MecanOdei
## Aplicación para mejorar la mecanografía
Aplicación sugerida por **Odei Bilbao** para practicar la mecanografía de textos

## Views
Aplicación con un menú como pantalla principal.

### Menú principal
2 secciones principales:
1. Con acceso a las otras 3 views:
    1. Practicar
    2. Estadísticas
    3. Configuración

2. Visualización de las mejores stats hasta la fecha

### View practicar
Cargar un texto, darle a comenzar y mecanografiar el texto. A medida que pulsamos las teclas correctas el texto se irá coloreando de color. Si la tecla pulsada es incorrecta mostrará la letra en rojo y no seguirá avanzando hasta que se pulse la tecla correcta.

Al acabar el texto se muestra un resumen de las estadísticas como número de teclas por minuto pulsadas etc.

Posibilidad de guardar en base de datos tanto el texto como las estadísticas:
O guardado automático tras completar el texto

### View Estadísticas
Un resumen más completo de todas las estadísticas, con teclas más veces pulsadas,
teclas falladas, teclas falladas cuando la siguiente era tecla X etc.
Poner un teclado virtual y mostrar las stats en el teclado ?

### View Configuración
Meter alguans configuraciones para la app que pueda
personalizar el usuario: paleta de colores ?, carga de archivos?
etc

- 27/02/2024
Odei me explica cómo será su examen y me detalla que en él, escuchará un audio (de 1 min) y tras él, tendrá un tiempo limitado para transcribir el contenido del mismo lo más fielmente posible.
Esto hace que me plantee lo siguiente:
    - Posibilidad de una nueva modalidad en la aplicación que sea **Examinar**
    - Buscar IA de text to speech que reproduzca el contenido de un archivo.
    - Cargar en la app un directorio con archivos .**txt** y que al hacer clic en **empezar** la app aleatoriamente escoja uno.
    - Al terminar enviar el texto original y la transcripción para que chatgpt la evalúe.
    - chatgpt devolverá en formato **json** la puntuación del 1 al 10 de la calidad de la transcripción en relación a la cantidad de información retenida y los fallos encontrados o las mejoras a realizar.

## Mejoras a implementar
### 03/03/2024
- En la partede Estadísticas, trackear la palabra perteneciente a las letras falladas
- [x] Hay un problema capturando la **Ñ**
### 21/03/2024
- [] Crear otro botón debajo del de carga para generar un texto aleatorio basado en una plantilla en el que ciertos elementos son variables y seleccionado aleatoriamente de entre varias opciones prefijadas. Crear el archivo ficticio en función de algunas variables
- [] Añadir más configuraciones