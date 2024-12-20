**Glosario de Términos**

1. **API (Interfaz de Programación de Aplicaciones):**
   - Es un conjunto de reglas y protocolos que permiten que diferentes aplicaciones o servicios se comuniquen entre sí. Las APIs facilitan la interacción y el intercambio de datos entre sistemas de software.

2. **API REST (API Representational State Transfer):**
   - Es un tipo de API que sigue el estilo arquitectónico REST. Las APIs REST utilizan protocolos web estándar, como HTTP, y permiten operaciones como GET, POST, PUT y DELETE para interactuar con recursos en un servidor.

3. **FastAPI:**
   - Es un framework web moderno y de alto rendimiento para construir APIs en Python. FastAPI es conocido por su facilidad de uso, velocidad y soporte para características avanzadas como validación automática de datos y documentación interactiva.

4. **Endpoint GET:**
   - En el contexto de una API REST, un "endpoint" es una URL específica donde se pueden realizar operaciones. El método GET es una operación HTTP utilizada para solicitar datos de un servidor sin modificar ningún recurso. Un endpoint GET, por lo tanto, es una ruta en la API que permite recuperar información.

5. **LLM (Modelo de Lenguaje de Gran Escala):**
   - Son modelos de inteligencia artificial entrenados en grandes cantidades de datos textuales que pueden comprender y generar lenguaje natural. Ejemplos incluyen GPT-3 y GPT-4.

6. **RAG (Generación Aumentada por Recuperación):**
   - Es un enfoque que combina la recuperación de información relevante de una base de datos o conjunto de documentos con la generación de lenguaje natural para proporcionar respuestas más precisas y contextualizadas.

7. **Embeddings:**
   - Son representaciones numéricas de texto que capturan el significado y contexto de palabras o frases, permitiendo que los algoritmos procesen y comparen textos de manera eficiente.

8. **ChromaDB:**
   - Es una base de datos especializada en almacenar y gestionar vectores, como embeddings. Permite búsquedas eficientes de similitud entre vectores, lo cual es útil para recuperar documentos relevantes basados en su contenido.

9. **Retriever (Recuperador):**
   - Es un componente que, dado un input (como una consulta), recupera información o documentos relevantes de una base de datos o índice.

10. **Prompt:**
    - Es el mensaje o texto de entrada que se proporciona a un modelo de lenguaje para generar una respuesta. Los prompts pueden ser diseñados o formateados de cierta manera para guiar al modelo a producir respuestas específicas.

11. **Template (Plantilla):**
    - Es un formato predefinido que se utiliza para estructurar el prompt que se envía al modelo de lenguaje, incorporando variables como la consulta del usuario y el contexto recuperado.

12. **uvicorn:**
    - Es un servidor web ligero y rápido para aplicaciones ASGI (Asynchronous Server Gateway Interface) en Python. Se utiliza comúnmente para ejecutar aplicaciones desarrolladas con frameworks como FastAPI.

13. **ASGI (Interfaz de Servidor de Gateway Asíncrono):**
    - Es un estándar para construir aplicaciones web asíncronas en Python, que permite manejar conexiones concurrentes y comunicaciones en tiempo real.

14. **Cliente LLM:**
    - Es un componente o librería que permite interactuar con un modelo de lenguaje alojado en un servidor, enviando prompts y recibiendo respuestas generadas.

15. **Contexto:**
    - En este código, el contexto se refiere al texto adicional (como fragmentos de documentos relevantes) que se proporciona al modelo de lenguaje junto con la consulta del usuario para mejorar la precisión de la respuesta.

16. **Consulta (Query):**
    - Es la pregunta o solicitud que el usuario hace al sistema, la cual será procesada para generar una respuesta.

17. **HTTP Methods (Métodos HTTP):**
    - Son operaciones estándar definidas en el protocolo HTTP para interactuar con recursos web. Los más comunes son GET (obtener datos), POST (enviar datos), PUT (actualizar datos) y DELETE (eliminar datos).

18. **Servidor REST:**
    - Es un servidor que expone una API REST, permitiendo a los clientes realizar operaciones sobre recursos a través de métodos HTTP estándar.

19. **Dispositivo 'cpu' en Model_kwargs:**
    - Indica que el modelo de embeddings o el modelo de lenguaje utilizará la CPU para el procesamiento, en lugar de una GPU.

20. **Chunk (Fragmento):**
    - Es una porción o segmento de texto. En el contexto de este código, los chunks son partes de documentos que se utilizan para construir el contexto proporcionado al modelo de lenguaje.

21. **Max_new_tokens:**
    - Es un parámetro que especifica el número máximo de tokens (palabras o subpalabras) que el modelo de lenguaje generará en su respuesta.

22. **Endpoint "/":**
    - Es la ruta raíz de la API REST. En este caso, es donde se define el método que manejará las solicitudes GET enviadas al servidor.

23. **Decorador @app.get("/"):**
    - En FastAPI, los decoradores como `@app.get("/")` se utilizan para definir rutas de la API y asociarlas con funciones que manejan las solicitudes a esas rutas.

24. **__name__ == "__main__":**
    - Es una construcción en Python que verifica si el script está siendo ejecutado directamente (no importado como módulo), y permite que el código dentro de este bloque se ejecute en ese caso.

25. **Servicio Web:**
    - Es una aplicación o componente que se ejecuta en un servidor y proporciona funcionalidades a través de la red, permitiendo a los clientes interactuar con él mediante protocolos estándar.

26. **Serialización y Deserialización:**
    - Son procesos de convertir datos a un formato que pueda ser transmitido (como JSON) y luego reconvertirlos a objetos o estructuras utilizables en código.

27. **Cliente HTTP:**
    - Es una herramienta o librería que permite enviar solicitudes HTTP a servidores y recibir respuestas, utilizada para interactuar con APIs web.

28. **Biblioteca (Library) vs Framework:**
    - Una biblioteca es un conjunto de funciones y clases reutilizables que los desarrolladores pueden llamar en su código. Un framework es una estructura completa que proporciona una base sobre la cual se construyen aplicaciones, dictando la arquitectura y flujo de la aplicación.

29. **Generación de Lenguaje Natural:**
    - Es el proceso por el cual un modelo de inteligencia artificial produce texto que imita el lenguaje humano, respondiendo preguntas o creando contenido coherente y relevante.

30. **Depuración (Debugging):**
    - Es el proceso de identificar y corregir errores o problemas en el código. En el script, se utilizan impresiones (`print`) para mostrar el prompt y la respuesta, lo cual ayuda en la depuración.
