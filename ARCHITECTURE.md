# Arquitetura do Sistema Multiagente para Geração de Artigos

## Visão Geral

Sistema multiagente baseado em CrewAI para geração automatizada de artigos com pesquisa na Wikipedia. O sistema oferece tanto uma **interface web moderna** quanto uma **API REST completa** para máxima flexibilidade de uso.

## Componentes Principais

### 1. Interface Web (static/)

#### Frontend Moderno
* **HTML5**: Estrutura semântica e acessível
* **CSS3**: Design responsivo com animações e transições
* **JavaScript ES6+**: Interação dinâmica com a API
* **Funcionalidades**:
  - Formulário intuitivo para geração de artigos
  - Validação em tempo real
  - Indicadores de progresso
  - Visualização formatada dos resultados
  - Download e cópia de artigos

### 2. Agentes (src/agents/)

#### Agente Pesquisador (Researcher)
* **Papel**: Pesquisar informações relevantes sobre o tópico
* **Objetivo**: Coletar dados precisos e abrangentes da Wikipedia
* **Ferramentas**: WikipediaTool (personalizada)
* **Técnicas de Prompt**: Few-shot learning, Chain-of-thought
* **Configuração**: Backstory especializado em pesquisa acadêmica

#### Agente Escritor (Writer)
* **Papel**: Criar artigos bem estruturados
* **Objetivo**: Produzir conteúdo de qualidade com mínimo 300 palavras
* **Ferramentas**: Acesso ao contexto do pesquisador
* **Técnicas de Prompt**: Structured output, Role-based prompting
* **Configuração**: Backstory de redator profissional

### 3. Ferramentas Personalizadas (src/tools/)

#### WikipediaTool
* **Funcionalidades**:
  - Consulta à API da Wikipedia em múltiplos idiomas
  - Extração de conteúdo relevante
  - Tratamento de erros e redirecionamentos
  - Cache de resultados para otimização
  - Suporte a busca por títulos e conteúdo

### 4. Modelos de Dados (src/models/)

#### ArticleRequest (Input)
```python
- topic: str (obrigatório)
- language: str = "pt"
- min_words: int = 300
- style: str = "informativo"
```

#### ArticleResponse (Output)
```python
- title: str
- content: str
- word_count: int
- sources: List[str]
- metadata: dict
- generated_at: datetime
```

#### HealthResponse
```python
- status: str
- timestamp: datetime
- version: str
- llm_provider: str
```

### 5. API REST (src/api.py)

#### Configuração FastAPI
* **Middleware CORS**: Configurado para desenvolvimento
* **Arquivos Estáticos**: Servindo interface web via `/static`
* **Documentação**: Swagger UI em `/docs` e ReDoc em `/redoc`
* **Tratamento de Erros**: Handler global para exceções

#### Endpoints

##### GET /
* **Função**: Serve a interface web principal
* **Retorno**: FileResponse (index.html)

##### GET /api/health
* **Função**: Status do sistema e configurações
* **Retorno**: HealthResponse com informações do sistema

##### POST /api/generate-article
* **Função**: Gerar artigo via agentes
* **Input**: ArticleRequest
* **Output**: ArticleResponse
* **Validação**: Pydantic para entrada e saída

##### GET /api/providers
* **Função**: Listar provedores LLM disponíveis
* **Retorno**: Lista de provedores e suas configurações

### 6. Orquestração (src/crew.py)

#### ArticleGenerator
* **Responsabilidades**:
  - Configuração dinâmica de LLM
  - Instanciação de agentes e tarefas
  - Execução da crew
  - Processamento de resultados

#### Configuração LLM
* **Provedores Suportados**:
  - Google Gemini (gratuito)
  - Groq (rápido)
  - OpenRouter (múltiplos modelos)
* **Configuração**: Via variáveis de ambiente
* **Fallback**: Sistema de recuperação entre provedores

## Fluxo de Execução

### Via Interface Web
1. **Usuário acessa** `http://localhost:8000`
2. **Preenche formulário** com tópico, palavras e estilo
3. **JavaScript valida** entrada e envia requisição
4. **API processa** requisição via agentes
5. **Interface exibe** resultado com opções de ação

### Via API REST
1. **Cliente faz requisição** POST para `/api/generate-article`
2. **FastAPI valida** entrada via Pydantic
3. **ArticleGenerator instancia** Crew com agentes configurados
4. **Agente Pesquisador** consulta Wikipedia via WikipediaTool
5. **Agente Escritor** recebe contexto e gera artigo estruturado
6. **Output validado** via Pydantic ArticleResponse
7. **Retorno estruturado** ao cliente com metadados

## Estrutura de Diretórios Atualizada

```
crewai-article-generator/
├── src/                    # Código fonte principal
│   ├── agents/             # Definição dos agentes
│   │   └── article_agents.py
│   ├── tools/              # Ferramentas personalizadas
│   │   └── wikipedia_tool.py
│   ├── models/             # Modelos Pydantic
│   │   └── article_models.py
│   ├── crew.py             # Orquestração da Crew
│   └── api.py              # API FastAPI
├── static/                 # Interface web
│   ├── index.html          # Página principal
│   ├── style.css           # Estilos responsivos
│   └── script.js           # Lógica de interação
├── tests/                  # Testes automatizados
│   ├── test_tools.py       # Testes das ferramentas
│   ├── test_agents.py      # Testes dos agentes
│   └── test_api.py         # Testes da API
├── docs/                   # Documentação
│   ├── ARCHITECTURE.md     # Este arquivo
│   ├── EXEMPLOS_API.md     # Exemplos de uso
│   └── GUIA_PUBLICACAO.md  # Guia de deploy
├── .env.example            # Configurações de exemplo
├── .gitignore              # Arquivos ignorados
├── requirements.txt        # Dependências Python
├── example.py              # Script de demonstração
├── test_system.py          # Teste completo do sistema
└── README.md               # Documentação principal
```

## Tecnologias e Dependências

### Backend
* **CrewAI 0.86.0**: Framework de agentes autônomos
* **FastAPI 0.115.0**: Framework web moderno e rápido
* **Pydantic 2.10.0**: Validação e serialização de dados
* **Uvicorn 0.32.0**: Servidor ASGI de alta performance
* **Requests 2.32.0**: Cliente HTTP para Wikipedia API

### Frontend
* **HTML5**: Estrutura semântica moderna
* **CSS3**: Grid, Flexbox, animações e responsividade
* **JavaScript ES6+**: Fetch API, async/await, DOM manipulation
* **Font Awesome**: Ícones vetoriais

### LLM e IA
* **Google Gemini**: Modelo gratuito e eficiente
* **Groq**: Inferência rápida
* **OpenRouter**: Acesso a múltiplos modelos

## Padrões de Design Implementados

### 1. **Separation of Concerns**
- Interface separada da lógica de negócio
- Agentes com responsabilidades específicas
- Modelos de dados isolados

### 2. **Dependency Injection**
- Configuração de LLM via factory pattern
- Injeção de ferramentas nos agentes

### 3. **Observer Pattern**
- Callbacks para progresso de execução
- Eventos de interface para feedback visual

### 4. **Strategy Pattern**
- Múltiplos provedores LLM intercambiáveis
- Diferentes estilos de escrita configuráveis

## Segurança e Boas Práticas

### API Security
* **Validação de entrada**: Pydantic models
* **Tratamento de erros**: Exception handlers globais
* **CORS configurado**: Para desenvolvimento seguro
* **Rate limiting**: Preparado para implementação

### Frontend Security
* **Validação client-side**: Prevenção de entradas inválidas
* **Sanitização**: Escape de conteúdo HTML
* **HTTPS ready**: Preparado para produção

### Environment Management
* **Variáveis de ambiente**: Configuração sensível isolada
* **API keys**: Nunca expostas no frontend
* **Configuração flexível**: Múltiplos ambientes suportados

## Escalabilidade e Performance

### Otimizações Implementadas
* **Cache de resultados**: Wikipedia API responses
* **Lazy loading**: Componentes carregados sob demanda
* **Compressão**: Assets otimizados
* **Async operations**: Operações não-bloqueantes

### Preparação para Escala
* **Containerização**: Docker-ready
* **Load balancing**: Stateless design
* **Database ready**: Estrutura preparada para persistência
* **Monitoring**: Logs estruturados e métricas


