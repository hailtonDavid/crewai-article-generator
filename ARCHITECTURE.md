# Arquitetura do Sistema Multiagente para Geração de Artigos

## Visão Geral

Sistema multiagente baseado em CrewAI para geração automatizada de artigos com pesquisa na Wikipedia.

## Componentes Principais

### 1. Agentes (src/agents/)

#### Agente Pesquisador (Researcher)

* **Papel**: Pesquisar informações relevantes sobre o tópico
* **Objetivo**: Coletar dados precisos e abrangentes da Wikipedia
* **Ferramentas**: WikipediaTool (personalizada)
* **Técnicas de Prompt**: Few-shot learning, Chain-of-thought

#### Agente Escritor (Writer)

* **Papel**: Criar artigos bem estruturados
* **Objetivo**: Produzir conteúdo de qualidade com mínimo 300 palavras
* **Ferramentas**: Acesso ao contexto do pesquisador
* **Técnicas de Prompt**: Structured output, Role-based prompting

### 2. Ferramentas Personalizadas (src/tools/)

#### WikipediaTool

* Consulta à API da Wikipedia em português
* Extração de conteúdo relevante
* Tratamento de erros e redirecionamentos
* Cache de resultados

### 3. Modelos de Dados (src/models/)

#### ArticleOutput (Pydantic)

```python
- title: str
- content: str
- word_count: int
- sources: List[str]
- metadata: dict
```

### 4. API REST (src/api.py)

#### Endpoints

* POST /api/generate-article
  * Input: {"topic": str, "language": str}
  * Output: ArticleOutput
* GET /api/health
  * Status do sistema

### 5. Configuração LLM

* Suporte a múltiplos provedores (Gemini, Groq, OpenRouter)
* Configuração via variáveis de ambiente
* Fallback entre provedores

## Fluxo de Execução


1. Cliente faz requisição POST com tópico
2. API instancia Crew com agentes
3. Agente Pesquisador consulta Wikipedia via WikipediaTool
4. Agente Escritor recebe contexto e gera artigo
5. Output validado via Pydantic
6. Retorno estruturado ao cliente

## Estrutura de Diretórios

```
crewai-article-generator/
├── src/
│   ├── tools/
│   │   └── wikipedia_tool.py
│   ├── agents/
│   │   └── article_agents.py
│   ├── models/
│   │   └── article_models.py
│   ├── crew.py
│   └── api.py
├── tests/
│   ├── test_tools.py
│   ├── test_agents.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── ARCHITECTURE.md
```

## Tecnologias

* **Framework**: CrewAI
* **API**: FastAPI
* **Validação**: Pydantic
* **LLM**: Gemini (gratuito), Groq, OpenRouter
* **HTTP Client**: requests
* **Testes**: pytest


