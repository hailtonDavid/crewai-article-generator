# Exemplos de Uso da API

Este documento fornece exemplos práticos de como usar a API REST do sistema.

## Iniciando o Servidor

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Windows: venv\Scripts\activate

# Iniciar servidor
uvicorn src.api:app --reload

# Servidor estará disponível em: http://127.0.0.1:8000
```

## Documentação Interativa

Acesse `http://127.0.0.1:8000/docs` para ver a documentação Swagger UI interativa.

## Exemplos de Requisições

### 1. Health Check

Verifica se a API está funcionando.

**Requisição:**
```bash
curl -X GET "http://127.0.0.1:8000/api/health"
```

**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-24T10:00:00.000000",
  "version": "1.0.0"
}
```

### 2. Gerar Artigo - Exemplo Básico

**Requisição:**
```bash
curl -X POST "http://127.0.0.1:8000/api/generate-article" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Inteligência Artificial",
    "language": "pt",
    "min_words": 300
  }'
```

**Resposta (resumida):**
```json
{
  "success": true,
  "message": "Artigo gerado com sucesso! 450 palavras.",
  "article": {
    "title": "Inteligência Artificial: Conceitos e Aplicações",
    "content": "# Inteligência Artificial: Conceitos e Aplicações\n\n## Introdução\n\nA inteligência artificial...",
    "word_count": 450,
    "sources": [
      "https://pt.wikipedia.org/wiki/Inteligência_artificial"
    ],
    "metadata": {
      "generated_at": "2025-10-24T10:05:30.123456",
      "language": "pt",
      "topic": "Inteligência Artificial",
      "agent_info": {
        "llm_provider": "gemini",
        "agents": "Researcher, Writer",
        "framework": "CrewAI"
      }
    },
    "summary": null
  },
  "error": null
}
```

### 3. Gerar Artigo - Tópico Personalizado

**Requisição:**
```bash
curl -X POST "http://127.0.0.1:8000/api/generate-article" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "História do Brasil",
    "language": "pt",
    "min_words": 400
  }'
```

### 4. Listar Provedores de LLM

**Requisição:**
```bash
curl -X GET "http://127.0.0.1:8000/api/providers"
```

**Resposta:**
```json
{
  "providers": [
    {
      "name": "gemini",
      "description": "Google Gemini (opção gratuita disponível)",
      "env_var": "GEMINI_API_KEY",
      "model": "gemini-2.0-flash-exp"
    },
    {
      "name": "groq",
      "description": "Groq (alta velocidade)",
      "env_var": "GROQ_API_KEY",
      "model": "llama-3.3-70b-versatile"
    },
    {
      "name": "openrouter",
      "description": "OpenRouter (múltiplos modelos)",
      "env_var": "OPENROUTER_API_KEY",
      "model": "google/gemini-2.0-flash-exp:free"
    }
  ],
  "current_provider": "gemini"
}
```

## Exemplos em Python

### Usando requests

```python
import requests
import json

# URL da API
API_URL = "http://127.0.0.1:8000"

# Gerar artigo
response = requests.post(
    f"{API_URL}/api/generate-article",
    json={
        "topic": "Machine Learning",
        "language": "pt",
        "min_words": 300
    }
)

if response.status_code == 200:
    data = response.json()
    if data["success"]:
        article = data["article"]
        print(f"Título: {article['title']}")
        print(f"Palavras: {article['word_count']}")
        print(f"\nConteúdo:\n{article['content'][:500]}...")
        
        # Salvar em arquivo
        with open("artigo.md", "w", encoding="utf-8") as f:
            f.write(article["content"])
    else:
        print(f"Erro: {data['error']}")
else:
    print(f"Erro HTTP: {response.status_code}")
```

### Usando httpx (async)

```python
import httpx
import asyncio

async def gerar_artigo(topic: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8000/api/generate-article",
            json={
                "topic": topic,
                "language": "pt",
                "min_words": 300
            },
            timeout=180.0  # 3 minutos
        )
        return response.json()

# Executar
result = asyncio.run(gerar_artigo("Python (linguagem de programação)"))
print(result["article"]["title"])
```

## Exemplos em JavaScript

### Usando fetch

```javascript
// Gerar artigo
async function gerarArtigo(topic) {
  const response = await fetch('http://127.0.0.1:8000/api/generate-article', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      topic: topic,
      language: 'pt',
      min_words: 300
    })
  });

  const data = await response.json();
  
  if (data.success) {
    console.log('Título:', data.article.title);
    console.log('Palavras:', data.article.word_count);
    console.log('Conteúdo:', data.article.content.substring(0, 500) + '...');
  } else {
    console.error('Erro:', data.error);
  }
}

// Executar
gerarArtigo('Blockchain');
```

### Usando axios

```javascript
const axios = require('axios');

axios.post('http://127.0.0.1:8000/api/generate-article', {
  topic: 'Computação Quântica',
  language: 'pt',
  min_words: 350
})
.then(response => {
  const { article } = response.data;
  console.log(`Artigo gerado: ${article.title}`);
  console.log(`Total de palavras: ${article.word_count}`);
})
.catch(error => {
  console.error('Erro:', error.response?.data || error.message);
});
```

## Tratamento de Erros

### Erro 422 - Validação

Ocorre quando os dados da requisição são inválidos.

**Exemplo:**
```json
{
  "detail": [
    {
      "loc": ["body", "topic"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Erro 500 - Erro Interno

Ocorre quando há um problema na geração do artigo.

**Exemplo:**
```json
{
  "success": false,
  "message": "Erro ao gerar artigo",
  "error": "API key não configurada. Defina a variável de ambiente GEMINI_API_KEY"
}
```

## Dicas de Uso

1. **Timeout**: A geração de artigos pode levar de 30 segundos a 3 minutos. Configure timeouts adequados.
2. **Rate Limiting**: Dependendo do provedor de LLM, pode haver limites de requisições por minuto.
3. **Tópicos Específicos**: Quanto mais específico o tópico, melhor o resultado.
4. **Idioma**: O sistema funciona melhor com `language="pt"` para a Wikipedia em português.

## Integração com Frontend

Exemplo de integração com React:

```jsx
import { useState } from 'react';

function ArticleGenerator() {
  const [topic, setTopic] = useState('');
  const [article, setArticle] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/generate-article', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic, language: 'pt', min_words: 300 })
      });
      const data = await response.json();
      if (data.success) {
        setArticle(data.article);
      }
    } catch (error) {
      console.error('Erro:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input 
        value={topic} 
        onChange={(e) => setTopic(e.target.value)}
        placeholder="Digite um tópico"
      />
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? 'Gerando...' : 'Gerar Artigo'}
      </button>
      {article && (
        <div>
          <h2>{article.title}</h2>
          <p>{article.word_count} palavras</p>
          <div dangerouslySetInnerHTML={{ __html: article.content }} />
        </div>
      )}
    </div>
  );
}
```

## Recursos Adicionais

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
- **OpenAPI Schema**: `http://127.0.0.1:8000/openapi.json`

