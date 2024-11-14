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

*Chunking* es el proceso de dividir un texto en fragmentos más pequeños y manejables. Este paso es crucial en documentos largos, como el manual de empleados, para asegurar que las consultas se respondan basándose en fragmentos de contexto relevantes y coherentes. Al dividir el documento en fragmentos, cada uno puede ser procesado de forma independiente, facilitando la recuperación de información precisa y contextual.

### Técnica de Semantic Chunking

En este proyecto, se utiliza *semantic chunking*, una técnica avanzada que divide el texto en fragmentos coherentes en función del significado y contexto, en lugar de utilizar límites fijos de longitud. Esto garantiza que cada fragmento mantenga una idea completa y contextual, lo que mejora la precisión de la búsqueda y respuesta.

#### ¿Cómo Funciona el Semantic Chunking?

1. **Análisis del Texto Completo**: A diferencia de los métodos tradicionales que cortan el texto en bloques de un número específico de caracteres o palabras, el *semantic chunking* comienza con un análisis del contenido para identificar puntos de ruptura naturales basados en el contexto y el significado. Esto asegura que cada fragmento tenga una idea coherente y no se interrumpa en puntos arbitrarios.

2. **Identificación de Temas y Contextos**: El algoritmo de *semantic chunking* identifica temas, ideas principales y contextos en el texto. Se basa en la detección de cambios en el flujo de ideas, como el inicio de un nuevo tema o la conclusión de uno existente, para definir dónde deben comenzar y terminar los fragmentos.

3. **Creación de Fragmentos Cohesivos**: Una vez identificados los puntos de ruptura semánticos, el texto se divide en fragmentos que reflejan unidades de significado. Cada fragmento es una porción de texto que tiene sentido por sí misma, lo que facilita que el sistema interprete y utilice el contexto completo de ese fragmento al buscar respuestas.

4. **Generación de Embeddings Específicos para Cada Fragmento**: Al dividir el texto en fragmentos con significado completo, se obtienen embeddings más representativos. Cada vector generado captura el contexto total de la idea en ese fragmento, mejorando así la calidad y precisión de las búsquedas.

#### Ventajas del Semantic Chunking

El *semantic chunking* tiene varias ventajas sobre los métodos tradicionales de chunking basados en longitud fija:

- **Contexto Coherente**: Los fragmentos generados contienen ideas completas, lo que facilita que el modelo de lenguaje interprete y responda preguntas de manera precisa.
- **Reducción de Respuestas Incompletas**: Al mantener fragmentos semánticamente coherentes, se minimizan las respuestas incompletas o ambiguas, que pueden surgir cuando los fragmentos se cortan en puntos arbitrarios.
- **Mejor Rendimiento en Consultas**: Al proporcionar fragmentos significativos, el modelo de lenguaje obtiene un contexto más útil para generar respuestas, lo que mejora la relevancia de las mismas.

### Justificación del Uso de Semantic Chunking

El *semantic chunking* es especialmente útil para documentos largos y complejos como el manual de empleados, donde el contexto y el flujo de ideas son importantes. En este proyecto, el uso de *semantic chunking* permite que cada fragmento de texto sea útil y completo en sí mismo, optimizando así la precisión del agente al responder preguntas basadas en el contenido del documento.
