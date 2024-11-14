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

Una base de datos vectorial es una herramienta diseñada para almacenar y buscar información representada en forma de vectores. En este proyecto, utilizamos **Pinecone** como base de datos vectorial para almacenar los embeddings del manual de empleados, lo que permite realizar búsquedas semánticas eficientes y precisas.

### ¿Por Qué Usar una Base de Datos Vectorial?

Al convertir los fragmentos del manual en vectores mediante embeddings, el sistema puede buscar fragmentos basados en la similitud de su contenido semántico. Esto permite que el chatbot identifique rápidamente el contenido más relevante en respuesta a una consulta, independientemente de las palabras exactas usadas en la pregunta.

### Pinecone en el Proyecto

**Pinecone** es una base de datos vectorial que permite almacenar grandes volúmenes de vectores y realizar búsquedas rápidas usando medidas de similitud, como la similitud coseno. En este proyecto, cada fragmento del manual de empleados se almacena en Pinecone junto con su embedding, facilitando una recuperación precisa de información.

### Implementación en el Proyecto

1. **Inicialización de Pinecone**: Primero, el código carga la clave de API de Pinecone y conecta con el servicio.

2. **Creación del Índice**: Se crea un índice en Pinecone, donde cada fragmento del manual es almacenado con su embedding. El índice permite definir la métrica de similitud (coseno en este caso) y la dimensión de los vectores.

3. **Búsqueda de Fragmentos Relevantes**: Cuando un usuario hace una pregunta, el sistema genera un embedding de la consulta y busca en Pinecone los fragmentos de texto más similares. Esto asegura que solo se usen los fragmentos más relevantes para generar la respuesta.

### Ventajas de Usar Pinecone

Al utilizar Pinecone, el proyecto obtiene acceso a una infraestructura de búsqueda vectorial optimizada y escalable, que puede manejar grandes volúmenes de datos y consultas en tiempo real. Esto permite que el chatbot responda de manera rápida y precisa, basándose en información relevante del manual de empleados.
