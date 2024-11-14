# RAG Employee Handbook Chatbot

Este proyecto implementa un agente conversacional que responde preguntas sobre documentos PDF largos, usando el "Google Employee Handbook" como ejemplo. A través de técnicas de *Retrieval-Augmented Generation (RAG)*, el chatbot combina búsqueda y generación de respuestas basadas exclusivamente en el contenido del manual. El objetivo es facilitar consultas rápidas y precisas sobre políticas y procedimientos del manual, optimizando el acceso a información corporativa clave en documentos extensos como el del ejemplo que cuenta con más de 60 paginas.

### Componentes Clave

- **Base de Datos Vectorial (Pinecone)**: Pinecone almacena y busca fragmentos relevantes del manual en forma de vectores, permitiendo búsquedas semánticas precisas.
  
- **División Semántica del Texto**: Se utiliza *semantic chunking* para dividir el texto en fragmentos coherentes, facilitando respuestas más exactas.
  
- **Modelos de OpenAI**: Modelos como *GPT-3.5* o *text-embedding-ada-002*, para generar respuestas utilizando los fragmentos recuperados, o pasar a embedding los distintos fragmentos del texto, los cuales permiten responder a las preguntas del manual.

## ¿Qué es RAG?

*Retrieval-Augmented Generation* (RAG) es una técnica de procesamiento de lenguaje natural que combina dos capacidades fundamentales: la **recuperación** de información y la **generación de respuestas**. 

En un sistema RAG:
1. **Recuperación**: Primero, el sistema busca fragmentos de información relevantes en una base de datos vectorial (como Pinecone) basada en la similitud semántica entre las preguntas y los datos almacenados.
2. **Generación**: Luego, un modelo generativo, como GPT-3.5, utiliza los fragmentos recuperados como contexto para construir una respuesta informada y específica a la pregunta.

Este enfoque permite que el modelo responda a preguntas complejas utilizando información actualizada y específica, incluso cuando el contenido de la respuesta no está integrado directamente en los parámetros del modelo. RAG es ideal para aplicaciones donde es fundamental responder basándose en datos precisos y extensos, como en el caso de este proyecto, que consulta un manual de empleados extenso.

## Embeddings

Los *embeddings* son representaciones vectoriales de texto que capturan el significado semántico de palabras, frases o fragmentos de texto de forma numérica. En el contexto de este proyecto, los embeddings son fundamentales para comparar la similitud entre las consultas del usuario y los fragmentos del documento, permitiendo que el chatbot identifique las respuestas relevantes en el manual de empleados.

### Cómo Funcionan los Embeddings

Cada fragmento de texto se convierte en un vector, que es un conjunto de números que representan el contenido semántico de ese fragmento. Al calcular la similitud entre el vector de la pregunta del usuario y los vectores de cada fragmento del documento, se puede identificar el fragmento que más se asemeja al contenido de la pregunta.

### Modelo Utilizado

En este proyecto se utiliza el modelo `text-embedding-ada-002` de OpenAI, que genera un vector de 1536 dimensiones para cada fragmento. Este modelo es eficiente en cuanto a costo y precisión, lo que lo hace ideal para tareas de búsqueda y recuperación de información en bases de datos vectoriales.

## Bases de Datos Vectoriales

Una base de datos vectorial es una herramienta diseñada para almacenar y buscar información en forma de vectores, permitiendo consultas rápidas y eficientes basadas en la similitud semántica del contenido. En este proyecto, utilizamos **Pinecone** como base de datos vectorial para almacenar los embeddings de los fragmentos del manual de empleados, facilitando así la búsqueda de información relevante en respuesta a las consultas del usuario.

### Configuración de la Base de Datos en Pinecone

La configuración del índice en Pinecone incluye los siguientes parámetros:

- **Nombre del índice**: El índice tiene un nombre específico que facilita su identificación y manejo.
- **Dimensiones del vector**: Cada vector tiene 1536 dimensiones, que es el tamaño del embedding generado por el modelo `text-embedding-ada-002` de OpenAI. Este número de dimensiones permite capturar patrones y relaciones semánticas complejas, lo que mejora la precisión de las búsquedas al representar conceptos abstractos y contextuales.
- **Métrica de similitud**: Se utiliza la similitud coseno en lugar de otras métricas. La similitud coseno mide el ángulo entre dos vectores en un espacio multidimensional, lo cual es ideal cuando se desea evaluar la similitud de contenido sin considerar la magnitud de los vectores. Esta métrica es particularmente adecuada para embeddings de texto, donde la similitud semántica es más importante que la escala.

### Implementación en el Proyecto

1. **Inicialización de Pinecone**: Se carga la clave de API de Pinecone y se establece una conexión con el servicio, permitiendo el acceso y uso de las funcionalidades de la base de datos vectorial.

2. **Creación del Índice**: El índice se configura con el nombre específico, la cantidad de dimensiones y la métrica de similitud coseno. Este índice almacena cada fragmento del manual de empleados junto con su embedding, lo que permite realizar búsquedas basadas en la similitud semántica de manera rápida y precisa.

3. **Búsqueda de Fragmentos Relevantes**: Cuando el usuario hace una pregunta, el sistema genera un embedding de la consulta y lo compara con los embeddings en Pinecone. Los fragmentos con mayor similitud coseno se seleccionan como los más relevantes para responder la consulta del usuario.

### Ventajas de Usar Pinecone con Similitud Coseno

La configuración de Pinecone con similitud coseno y 1536 dimensiones proporciona:

- **Precisión en la búsqueda**: La similitud coseno permite encontrar fragmentos de texto con significados similares, mejorando la relevancia de las respuestas.
- **Optimización para consultas semánticas**: La estructura de Pinecone permite manejar grandes volúmenes de datos y consultas en tiempo real, lo que asegura respuestas rápidas y contextualmente relevantes basadas en el contenido del manual de empleados.

Esta configuración permite que el chatbot responda con precisión y eficiencia a preguntas complejas, aprovechando al máximo la estructura semántica del documento original.
## Chunking

*Chunking* es el proceso de dividir un texto extenso en fragmentos más pequeños y manejables. Esta técnica es fundamental en documentos largos, como el manual de empleados, para garantizar que las consultas se respondan basándose en fragmentos coherentes y relevantes. Dividir el texto en unidades significativas mejora la precisión y la eficiencia en la búsqueda de información.

### Técnica de Semantic Chunking

En este proyecto se emplea *semantic chunking*, un método avanzado que utiliza embeddings y criterios semánticos para identificar puntos de ruptura en el texto. A diferencia de los métodos tradicionales de chunking que dividen el texto de manera uniforme (por palabras o caracteres), el *semantic chunking* segmenta el texto en fragmentos lógicamente completos, asegurando que cada fragmento mantenga un contexto coherente y representativo.

#### Funcionamiento del Semantic Chunking

1. **Generación de Embeddings Iniciales**: El proceso comienza aplicando un modelo de embeddings, como `text-embedding-ada-002`, para representar el texto completo en un espacio vectorial. Cada fragmento potencial del texto se representa como un vector de alta dimensionalidad que captura su contenido semántico.

2. **Identificación de Puntos de Ruptura Semánticos**: Utilizando el modelo de *SemanticChunker*, se detectan cambios en el contenido semántico en base a un umbral de ruptura (*breakpoint threshold*) que se configura por percentil. Este umbral define la "profundidad" de la segmentación, asegurando que solo se realicen rupturas en puntos donde el contenido cambia significativamente, lo que minimiza el riesgo de interrumpir ideas o contextos importantes.

3. **Segmentación en Fragmentos Coherentes**: Una vez identificados los puntos de ruptura, el texto se divide en fragmentos semánticos, donde cada fragmento representa una unidad lógica completa. Estos fragmentos capturan ideas o secciones con significado completo, lo que facilita que el sistema de recuperación utilice este contexto para encontrar respuestas precisas.

4. **Generación de Embeddings Específicos para Cada Fragmento**: Finalmente, se genera un embedding para cada fragmento resultante del *semantic chunking*. Estos embeddings permiten almacenar cada fragmento en una base de datos vectorial y realizar búsquedas precisas. Los embeddings por fragmento reflejan el contexto completo de cada unidad de texto, maximizando la precisión de las búsquedas basadas en similitud.

#### Justificación Técnica del Uso de Semantic Chunking

El *semantic chunking* proporciona una segmentación optimizada y permite generar embeddings que son más representativos en comparación con los métodos de chunking de longitud fija. Los fragmentos semánticos, al conservar el contexto y la coherencia lógica, mejoran significativamente la relevancia y precisión de las respuestas generadas. Esta técnica es particularmente útil en documentos extensos y complejos, donde la interrupción arbitraria de ideas podría llevar a respuestas incompletas o ambiguas.

### Ventajas Técnicas del Semantic Chunking en el Proyecto

- **Reducción de Pérdida de Contexto**: La segmentación semántica asegura que cada fragmento retenga un contexto completo, eliminando la necesidad de unir fragmentos parciales para construir respuestas coherentes.
- **Mejora en la Relevancia de las Respuestas**: Al trabajar con fragmentos que representan ideas completas, el modelo de lenguaje puede generar respuestas basadas en contextos más precisos, mejorando la relevancia de la información proporcionada.
- **Optimización de la Búsqueda Semántica**: Al aplicar un umbral de ruptura basado en percentiles, el sistema garantiza una segmentación dinámica que se ajusta al contenido específico del documento, en lugar de seguir una longitud fija.

Esta estrategia permite al chatbot responder de manera más precisa y eficiente a preguntas basadas en el contenido del documento, maximizando la utilidad y relevancia de cada fragmento en el contexto de las consultas del usuario.

