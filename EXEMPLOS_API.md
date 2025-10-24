# Exemplos de Uso da API e Interface Web

Este documento fornece exemplos práticos de como usar tanto a **interface web** quanto a **API REST** do sistema.

## 🌐 Interface Web (Recomendado)

### Acesso Rápido

A maneira mais fácil de usar o sistema é através da interface web moderna:

```bash
# Iniciar servidor
uvicorn src.api:app --reload --port 8001

# Acessar interface web
http://127.0.0.1:8001
```

### Funcionalidades da Interface Web

* ✅ **Formulário intuitivo** com validação em tempo real
* ✅ **Indicadores de progresso** durante a geração
* ✅ **Visualização formatada** do artigo gerado
* ✅ **Download em Markdown** com um clique
* ✅ **Cópia para clipboard** instantânea
* ✅ **Design responsivo** para desktop e mobile
* ✅ **Tratamento de erros** com mensagens claras

### Como Usar a Interface Web

1. **Acesse** `http://127.0.0.1:8001`
2. **Preencha** o tópico desejado (ex: "Inteligência Artificial")
3. **Configure** número mínimo de palavras (padrão: 300)
4. **Selecione** o estilo de escrita (Informativo, Acadêmico, Jornalístico)
5. **Clique** em "Gerar Artigo"
6. **Aguarde** o processamento (30s - 3min)
7. **Visualize** o resultado formatado
8. **Baixe** ou **copie** o artigo conforme necessário

## 🔧 API REST (Para Desenvolvedores)

### Iniciando o Servidor

```bash
# Ativar ambiente virtual
source venv/bin/activate  # Windows: venv\Scripts\activate

# Iniciar servidor
uvicorn src.api:app --reload --port 8001

# Servidor estará disponível em: http://127.0.0.1:8001
```

### Documentação Interativa

* **Swagger UI**: `http://127.0.0.1:8001/docs`
* **ReDoc**: `http://127.0.0.1:8001/redoc`
* **OpenAPI Schema**: `http://127.0.0.1:8001/openapi.json`

## 📋 Endpoints Disponíveis

### 1. Interface Web Principal

**GET /**

Serve a interface web principal.

```bash
curl -X GET "http://127.0.0.1:8001/"
# Retorna: index.html (interface web)
```

### 2. Health Check

Verifica se a API está funcionando e mostra configurações.

**GET /api/health**

```bash
curl -X GET "http://127.0.0.1:8001/api/health"
```

**Resposta:**

```json
{
  "status": "healthy",
  "timestamp": "2025-01-24T10:00:00.000000",
  "version": "1.0.0",
  "llm_provider": "gemini",
  "endpoints": [
    "GET /",
    "GET /api/health", 
    "POST /api/generate-article",
    "GET /api/providers"
  ]
}
```

### 3. Gerar Artigo

**POST /api/generate-article**

Endpoint principal para geração de artigos.

**Parâmetros de Entrada:**

```json
{
  "topic": "string (obrigatório)",
  "language": "string (padrão: 'pt')",
  "min_words": "integer (padrão: 300)",
  "style": "string (padrão: 'informativo')"
}
```

**Exemplo Básico:**

```bash
curl -X POST "http://127.0.0.1:8001/api/generate-article" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Inteligência Artificial",
    "language": "pt",
    "min_words": 300,
    "style": "informativo"
  }'
```

**Resposta Completa:**

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
      "generated_at": "2025-01-24T10:05:30.123456",
      "language": "pt",
      "topic": "Inteligência Artificial",
      "style": "informativo",
      "agent_info": {
        "llm_provider": "gemini",
        "agents": "Researcher, Writer",
        "framework": "CrewAI"
      }
    }
  },
  "error": null
}
```

### 4. Listar Provedores LLM

**GET /api/providers**

Lista todos os provedores de LLM disponíveis e suas configurações.

```bash
curl -X GET "http://127.0.0.1:8001/api/providers"
```

**Resposta:**

```json
{
  "providers": [
    {
      "name": "gemini",
      "description": "Google Gemini (opção gratuita disponível)",
      "env_var": "GEMINI_API_KEY",
      "model": "gemini-2.0-flash-exp",
      "status": "configured"
    },
    {
      "name": "groq",
      "description": "Groq (alta velocidade)",
      "env_var": "GROQ_API_KEY",
      "model": "llama-3.3-70b-versatile",
      "status": "not_configured"
    },
    {
      "name": "openrouter",
      "description": "OpenRouter (múltiplos modelos)",
      "env_var": "OPENROUTER_API_KEY",
      "model": "google/gemini-2.0-flash-exp:free",
      "status": "not_configured"
    }
  ],
  "current_provider": "gemini",
  "fallback_enabled": true
}
```

## 💻 Exemplos de Código

### Python com requests

```python
import requests
import json

# URL da API
API_URL = "http://127.0.0.1:8001"

def gerar_artigo(topic: str, min_words: int = 300, style: str = "informativo"):
    """Gera um artigo usando a API"""
    response = requests.post(
        f"{API_URL}/api/generate-article",
        json={
            "topic": topic,
            "language": "pt",
            "min_words": min_words,
            "style": style
        },
        timeout=180  # 3 minutos
    )
    
    if response.status_code == 200:
        data = response.json()
        if data["success"]:
            article = data["article"]
            print(f"✅ Título: {article['title']}")
            print(f"📊 Palavras: {article['word_count']}")
            print(f"🎨 Estilo: {article['metadata']['style']}")
            print(f"🔗 Fontes: {len(article['sources'])} fonte(s)")
            
            # Salvar em arquivo
            filename = f"artigo_{topic.replace(' ', '_').lower()}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(article["content"])
            print(f"💾 Salvo em: {filename}")
            
            return article
        else:
            print(f"❌ Erro: {data['error']}")
    else:
        print(f"🚨 Erro HTTP: {response.status_code}")
    
    return None

# Exemplos de uso
if __name__ == "__main__":
    # Artigo básico
    gerar_artigo("Machine Learning")
    
    # Artigo acadêmico longo
    gerar_artigo("Computação Quântica", min_words=500, style="acadêmico")
    
    # Artigo jornalístico
    gerar_artigo("Blockchain", min_words=400, style="jornalístico")
```

### Python com httpx (async)

```python
import httpx
import asyncio
from typing import Optional

async def gerar_artigo_async(topic: str, style: str = "informativo") -> Optional[dict]:
    """Gera artigo de forma assíncrona"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://127.0.0.1:8001/api/generate-article",
                json={
                    "topic": topic,
                    "language": "pt",
                    "min_words": 300,
                    "style": style
                },
                timeout=180.0
            )
            
            data = response.json()
            if data["success"]:
                return data["article"]
            else:
                print(f"Erro: {data['error']}")
                return None
                
        except httpx.TimeoutException:
            print("⏰ Timeout: A geração está demorando mais que o esperado")
            return None
        except Exception as e:
            print(f"🚨 Erro: {e}")
            return None

# Gerar múltiplos artigos simultaneamente
async def gerar_multiplos_artigos():
    topics = [
        "Python (linguagem de programação)",
        "React (biblioteca JavaScript)",
        "Docker (software)"
    ]
    
    tasks = [gerar_artigo_async(topic) for topic in topics]
    results = await asyncio.gather(*tasks)
    
    for i, article in enumerate(results):
        if article:
            print(f"✅ {topics[i]}: {article['word_count']} palavras")

# Executar
asyncio.run(gerar_multiplos_artigos())
```

### JavaScript (Frontend)

```javascript
class ArticleAPI {
    constructor(baseURL = 'http://127.0.0.1:8001') {
        this.baseURL = baseURL;
    }
    
    async generateArticle(topic, options = {}) {
        const {
            minWords = 300,
            style = 'informativo',
            language = 'pt'
        } = options;
        
        try {
            const response = await fetch(`${this.baseURL}/api/generate-article`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    topic,
                    language,
                    min_words: minWords,
                    style
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                return {
                    success: true,
                    article: data.article
                };
            } else {
                return {
                    success: false,
                    error: data.error
                };
            }
        } catch (error) {
            return {
                success: false,
                error: `Erro de rede: ${error.message}`
            };
        }
    }
    
    async checkHealth() {
        try {
            const response = await fetch(`${this.baseURL}/api/health`);
            return await response.json();
        } catch (error) {
            return { status: 'error', message: error.message };
        }
    }
    
    async getProviders() {
        try {
            const response = await fetch(`${this.baseURL}/api/providers`);
            return await response.json();
        } catch (error) {
            return { error: error.message };
        }
    }
}

// Exemplo de uso
const api = new ArticleAPI();

// Gerar artigo com callback de progresso
async function gerarArtigoComProgresso(topic) {
    console.log('🚀 Iniciando geração...');
    
    const result = await api.generateArticle(topic, {
        minWords: 400,
        style: 'acadêmico'
    });
    
    if (result.success) {
        const { article } = result;
        console.log('✅ Artigo gerado com sucesso!');
        console.log(`📝 Título: ${article.title}`);
        console.log(`📊 Palavras: ${article.word_count}`);
        console.log(`⏰ Gerado em: ${article.metadata.generated_at}`);
        
        // Exibir no DOM
        document.getElementById('article-title').textContent = article.title;
        document.getElementById('article-content').innerHTML = 
            article.content.replace(/\n/g, '<br>');
        
        return article;
    } else {
        console.error('❌ Erro:', result.error);
        alert(`Erro ao gerar artigo: ${result.error}`);
        return null;
    }
}

// Usar com async/await
gerarArtigoComProgresso('Inteligência Artificial');
```

### Node.js com axios

```javascript
const axios = require('axios');
const fs = require('fs').promises;

class ArticleGenerator {
    constructor(baseURL = 'http://127.0.0.1:8001') {
        this.api = axios.create({
            baseURL,
            timeout: 180000, // 3 minutos
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }
    
    async generateArticle(topic, options = {}) {
        try {
            const response = await this.api.post('/api/generate-article', {
                topic,
                language: options.language || 'pt',
                min_words: options.minWords || 300,
                style: options.style || 'informativo'
            });
            
            return response.data;
        } catch (error) {
            if (error.response) {
                throw new Error(`API Error: ${error.response.data.error || error.response.statusText}`);
            } else if (error.request) {
                throw new Error('Erro de rede: Servidor não respondeu');
            } else {
                throw new Error(`Erro: ${error.message}`);
            }
        }
    }
    
    async saveArticle(article, filename) {
        const content = `# ${article.title}\n\n${article.content}\n\n---\n\n**Gerado em:** ${article.metadata.generated_at}\n**Palavras:** ${article.word_count}\n**Fontes:** ${article.sources.join(', ')}`;
        
        await fs.writeFile(filename, content, 'utf8');
        console.log(`📄 Artigo salvo em: ${filename}`);
    }
}

// Exemplo de uso
async function main() {
    const generator = new ArticleGenerator();
    
    try {
        console.log('🔍 Verificando status da API...');
        const health = await generator.api.get('/api/health');
        console.log(`✅ API Status: ${health.data.status}`);
        
        console.log('📝 Gerando artigo...');
        const result = await generator.generateArticle('Blockchain', {
            minWords: 500,
            style: 'jornalístico'
        });
        
        if (result.success) {
            const { article } = result;
            console.log(`✅ ${article.title} (${article.word_count} palavras)`);
            
            await generator.saveArticle(article, 'blockchain_artigo.md');
        } else {
            console.error('❌ Falha na geração:', result.error);
        }
        
    } catch (error) {
        console.error('🚨 Erro:', error.message);
    }
}

main();
```

## 🚨 Tratamento de Erros

### Códigos de Status HTTP

| Código | Descrição | Ação |
|--------|-----------|-------|
| 200 | Sucesso | Processar resposta |
| 422 | Dados inválidos | Verificar parâmetros |
| 500 | Erro interno | Verificar logs/configuração |
| 503 | Serviço indisponível | Tentar novamente |

### Exemplos de Erros Comuns

#### 1. Erro de Validação (422)

```json
{
  "detail": [
    {
      "loc": ["body", "topic"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "min_words"],
      "msg": "ensure this value is greater than 0",
      "type": "value_error.number.not_gt"
    }
  ]
}
```

#### 2. Erro de Configuração (500)

```json
{
  "success": false,
  "message": "Erro ao gerar artigo",
  "error": "API key não configurada. Defina a variável de ambiente GEMINI_API_KEY",
  "article": null
}
```

#### 3. Erro de Timeout

```json
{
  "success": false,
  "message": "Timeout na geração do artigo",
  "error": "A geração demorou mais de 3 minutos",
  "article": null
}
```

## 🎯 Dicas de Uso

### Performance
* ⏱️ **Timeout**: Configure timeouts de 2-3 minutos
* 🔄 **Rate Limiting**: Respeite limites do provedor LLM
* 📊 **Monitoramento**: Use `/api/health` para verificar status

### Qualidade dos Artigos
* 🎯 **Tópicos Específicos**: "Python para Data Science" > "Programação"
* 🌍 **Idioma**: Use `language="pt"` para melhor qualidade
* 📝 **Palavras Mínimas**: 300-500 palavras para artigos completos
* 🎨 **Estilos**: Experimente diferentes estilos conforme o público

### Integração
* 🔗 **CORS**: Configurado para desenvolvimento local
* 📱 **Responsivo**: Interface web funciona em mobile
* 💾 **Cache**: Considere cache para tópicos frequentes
* 🔐 **Segurança**: Use HTTPS em produção

## 🔗 Recursos Adicionais

* **Interface Web**: `http://127.0.0.1:8001/`
* **Swagger UI**: `http://127.0.0.1:8001/docs`
* **ReDoc**: `http://127.0.0.1:8001/redoc`
* **Arquivos Estáticos**: `http://127.0.0.1:8001/static/`
* **Documentação**: Ver `README.md` e `ARCHITECTURE.md`


