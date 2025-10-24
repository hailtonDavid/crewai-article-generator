'''
# Sistema Multiagente para Geração de Artigos com CrewAI

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.86.0-orange.svg)](https://docs.crewai.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green.svg)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.10.0-purple.svg)](https://docs.pydantic.dev/)

Este projeto implementa um sistema multiagente autônomo para a geração automatizada de artigos, utilizando o framework **CrewAI**. O sistema é capaz de pesquisar informações sobre um determinado tópico na Wikipedia, processar o conteúdo e criar um artigo coeso e bem estruturado com no mínimo 300 palavras.

O projeto foi desenvolvido para ser uma solução robusta e extensível, com uma API REST para fácil integração e uso de boas práticas de desenvolvimento, como validação de dados com Pydantic e engenharia de prompts avançada.

## ✨ Funcionalidades Principais

- **Automação Completa**: Gera artigos completos a partir de um único tópico.
- **Dois Agentes Especializados**:
  - **Pesquisador (Researcher)**: Especializado em coletar informações precisas e relevantes da Wikipedia.
  - **Escritor (Writer)**: Especializado em transformar a pesquisa em um artigo bem escrito e estruturado.
- **Ferramenta Personalizada**: Inclui uma `WikipediaTool` customizada para interagir com a API da Wikipedia em qualquer idioma.
- **API REST**: Uma API construída com **FastAPI** para executar o sistema de forma programática.
- **Validação de Dados**: Uso de **Pydantic** para garantir que as entradas e saídas da API e da Crew sejam estruturadas e validadas.
- **Engenharia de Prompts**: Aplicação de técnicas como *role-based prompting*, *chain-of-thought* e *structured output* para otimizar a qualidade dos resultados.
- **Suporte a Múltiplos LLMs**: Facilmente configurável para usar diferentes provedores de LLM, como **Google Gemini**, **Groq** ou **OpenRouter**.
- **Código Documentado**: Todo o código é bem documentado para facilitar o entendimento e a manutenção.

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Versão | Propósito |
| :--- | :--- | :--- |
| **Python** | 3.9+ | Linguagem principal do projeto |
| **CrewAI** | 0.86.0 | Framework para orquestração de agentes autônomos |
| **CrewAI-Tools** | 0.17.0 | Ferramentas base para agentes |
| **FastAPI** | 0.115.0 | Framework para construção da API REST |
| **Pydantic** | 2.10.0 | Validação e estruturação de dados |
| **Uvicorn** | 0.32.0 | Servidor ASGI para FastAPI |
| **Requests** | 2.32.0 | Cliente HTTP para a API da Wikipedia |
| **python-dotenv** | 1.0.0 | Gerenciamento de variáveis de ambiente |

## 📂 Estrutura do Projeto

O projeto está organizado de forma modular para facilitar a manutenção e escalabilidade.

```
crewai-article-generator/
├── src/
│   ├── agents/             # Definição dos agentes (Pesquisador, Escritor)
│   │   └── article_agents.py
│   ├── tools/              # Ferramentas personalizadas para os agentes
│   │   └── wikipedia_tool.py
│   ├── models/             # Modelos Pydantic para validação de dados
│   │   └── article_models.py
│   ├── crew.py             # Orquestração da Crew e lógica de geração
│   └── api.py              # Implementação da API com FastAPI
├── tests/                  # Testes unitários e de integração
│   └── test_tools.py
├── .env.example            # Arquivo de exemplo para variáveis de ambiente
├── .gitignore              # Arquivos e diretórios a serem ignorados pelo Git
├── requirements.txt        # Lista de dependências do projeto
├── example.py              # Script para demonstrar o uso do sistema via terminal
├── test_system.py          # Script de teste completo do sistema
└── README.md               # Este arquivo
```

## 🚀 Como Executar

Siga os passos abaixo para configurar e executar o projeto em seu ambiente local.

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/crewai-article-generator.git
cd crewai-article-generator
```

### 2. Criar um Ambiente Virtual

É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

### 3. Instalar as Dependências

Instale todas as bibliotecas necessárias com o `pip`.

```bash
pip install -r requirements.txt
```

### 4. Configurar as Variáveis de Ambiente

O sistema precisa de uma chave de API para acessar o LLM. O projeto suporta Gemini (gratuito), Groq e OpenRouter.

1.  **Copie o arquivo de exemplo:**

    ```bash
    cp .env.example .env
    ```

2.  **Obtenha uma API Key:**
    - **Google Gemini**: Acesse [Google AI Studio](https://makersuite.google.com/app/apikey) para obter sua chave gratuita.

3.  **Edite o arquivo `.env`:**
    Abra o arquivo `.env` e adicione sua chave de API.

    ```dotenv
    # Configuração do Sistema Multiagente de Geração de Artigos

    # Opções: gemini, groq, openrouter
    LLM_PROVIDER=gemini

    # Descomente e configure a chave do provedor que você vai usar
    GEMINI_API_KEY=sua_api_key_aqui
    # GROQ_API_KEY=sua_api_key_aqui
    # OPENROUTER_API_KEY=sua_api_key_aqui

    # Configuração da API
    HOST=0.0.0.0
    PORT=8000
    ```

### 5. Executar a Aplicação

Você pode interagir com o sistema de duas formas: via API REST ou através do script de exemplo.

#### a) Executar a API REST

Inicie o servidor FastAPI com Uvicorn.

```bash
uvicorn src.api:app --reload
```

O servidor estará disponível em `http://127.0.0.1:8000`.

- **Documentação Interativa**: Acesse `http://127.0.0.1:8000/docs` para ver a documentação do Swagger UI e testar os endpoints.
- **Endpoint Principal**: `POST /api/generate-article`
  - **Corpo da Requisição (JSON):**
    ```json
    {
      "topic": "História do Brasil",
      "language": "pt",
      "min_words": 350
    }
    ```

#### b) Executar o Script de Exemplo

Para uma demonstração rápida via terminal, execute o script `example.py`.

```bash
python example.py
```

O script solicitará um tópico e, em seguida, gerará o artigo e o salvará em um arquivo Markdown.

## 🧪 Testes

O projeto inclui um script de teste para validar a funcionalidade dos principais componentes.

```bash
python test_system.py
```

Este script testa a ferramenta da Wikipedia, os modelos Pydantic e a geração completa de um artigo.

## 🤖 Detalhes dos Agentes

### Agente 1: Pesquisador Especializado
- **Objetivo**: Coletar dados precisos e abrangentes da Wikipedia.
- **Ferramentas**: `WikipediaTool`.
- **Engenharia de Prompt**: Utiliza um *backstory* detalhado que o posiciona como um especialista em pesquisa, incentivando um raciocínio sistemático para coletar definições, contexto histórico e aplicações práticas.

### Agente 2: Redator Profissional
- **Objetivo**: Criar um artigo informativo e bem estruturado com no mínimo 300 palavras.
- **Engenharia de Prompt**: Possui um *backstory* de redator experiente, com instruções claras sobre a estrutura do artigo (título, introdução, desenvolvimento, conclusão), estilo de escrita e formatação em Markdown.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* ou enviar *pull requests* para melhorias.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
'''
