# Guia de Publicação e Deploy

Este documento fornece instruções completas para publicar o projeto no GitHub e fazer deploy da aplicação com interface web.

## 📋 Pré-requisitos

1. **Conta no GitHub**: Crie uma conta em [github.com](https://github.com) se ainda não tiver
2. **Git instalado**: Verifique com `git --version`
3. **Python 3.8+**: Para executar a aplicação
4. **Chave de API**: Pelo menos uma chave configurada (Gemini, Groq ou OpenRouter)

## 🚀 Publicação no GitHub

### 1. Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito e selecione **"New repository"**
3. Configure o repositório:
   * **Repository name**: `crewai-article-generator`
   * **Description**: "Sistema Multiagente para Geração de Artigos com Interface Web - CrewAI + FastAPI"
   * **Visibility**: Selecione **Public**
   * **NÃO** marque "Initialize this repository with a README" (já temos um README local)
4. Clique em **"Create repository"**

### 2. Conectar o Repositório Local ao GitHub

```bash
cd crewai-article-generator

# Adicionar o repositório remoto
git remote add origin https://github.com/SEU-USUARIO/crewai-article-generator.git

# Renomear a branch para 'main' (se necessário)
git branch -M main

# Fazer push do código para o GitHub
git push -u origin main
```

**Importante**: Substitua `SEU-USUARIO` pelo seu nome de usuário do GitHub.

### 3. Verificar a Publicação

Acesse `https://github.com/SEU-USUARIO/crewai-article-generator` no navegador para verificar se todos os arquivos foram enviados corretamente.

## 🌐 Deploy da Aplicação

### Opção 1: Deploy Local (Desenvolvimento)

```bash
# 1. Clonar o repositório
git clone https://github.com/SEU-USUARIO/crewai-article-generator.git
cd crewai-article-generator

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas chaves de API

# 5. Iniciar a aplicação
uvicorn src.api:app --reload --port 8001

# 6. Acessar a interface web
# http://127.0.0.1:8001
```

### Opção 2: Deploy com Docker

Crie um `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Expor porta
EXPOSE 8001

# Comando para iniciar a aplicação
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8001"]
```

E um `docker-compose.yml`:

```yaml
version: '3.8'

services:
  article-generator:
    build: .
    ports:
      - "8001:8001"
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - GROQ_API_KEY=${GROQ_API_KEY}
      - OPENROUTER_API_KEY=${OPENROUTER_API_KEY}
    env_file:
      - .env
    restart: unless-stopped
    volumes:
      - ./static:/app/static:ro
```

**Comandos Docker:**

```bash
# Construir e executar
docker-compose up --build

# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down
```

### Opção 3: Deploy na Nuvem

#### Render.com (Gratuito)

1. **Conectar repositório**:
   - Acesse [render.com](https://render.com)
   - Conecte sua conta GitHub
   - Selecione o repositório

2. **Configurar Web Service**:
   - **Name**: `crewai-article-generator`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.api:app --host 0.0.0.0 --port $PORT`

3. **Variáveis de Ambiente**:
   ```
   GEMINI_API_KEY=sua_chave_aqui
   GROQ_API_KEY=sua_chave_aqui
   OPENROUTER_API_KEY=sua_chave_aqui
   ```

#### Railway.app

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway deploy
```

#### Heroku

```bash
# Instalar Heroku CLI
# Criar Procfile
echo "web: uvicorn src.api:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create crewai-article-generator
heroku config:set GEMINI_API_KEY=sua_chave
git push heroku main
```

## 🔧 Configuração de Produção

### 1. Variáveis de Ambiente

Crie um arquivo `.env` com suas chaves:

```env
# LLM Providers (configure pelo menos uma)
GEMINI_API_KEY=your_gemini_key_here
GROQ_API_KEY=your_groq_key_here
OPENROUTER_API_KEY=your_openrouter_key_here

# Configurações da aplicação
ENVIRONMENT=production
DEBUG=false
CORS_ORIGINS=["https://seudominio.com"]
```

### 2. Configurações de Segurança

Para produção, atualize `src/api.py`:

```python
# Configuração CORS para produção
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seudominio.com"],  # Domínios específicos
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### 3. Monitoramento e Logs

Adicione logging estruturado:

```python
import logging
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

## 📊 Monitoramento da Aplicação

### Health Check Endpoint

A aplicação inclui um endpoint de health check:

```bash
curl https://sua-app.com/api/health
```

Resposta esperada:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-24T10:00:00.000000",
  "version": "1.0.0",
  "llm_provider": "gemini"
}
```

### Métricas Importantes

- **Tempo de resposta**: Geração de artigos (30s - 3min)
- **Taxa de sucesso**: >95% para tópicos válidos
- **Uso de recursos**: CPU e memória durante geração
- **Erros comuns**: API keys inválidas, timeouts

## 🔄 Estrutura de Branches

Para projetos colaborativos:

```bash
# Branch principal (produção)
main

# Branch de desenvolvimento
git checkout -b develop

# Features específicas
git checkout -b feature/nova-funcionalidade

# Hotfixes
git checkout -b hotfix/correcao-urgente

# Merge para develop
git checkout develop
git merge feature/nova-funcionalidade

# Merge para main (via Pull Request)
git checkout main
git merge develop
```

## 📝 Boas Práticas

### 1. Commits Semânticos

```bash
feat: adicionar interface web responsiva
fix: corrigir erro de timeout na API
docs: atualizar documentação de deploy
style: melhorar CSS da interface
refactor: otimizar código dos agentes
test: adicionar testes para API
chore: atualizar dependências
```

### 2. Segurança

- ✅ **Nunca** faça commit de chaves de API reais
- ✅ Use `.env.example` para documentar variáveis necessárias
- ✅ Configure CORS adequadamente para produção
- ✅ Use HTTPS em produção
- ✅ Implemente rate limiting se necessário

### 3. Documentação

- ✅ Mantenha README.md atualizado
- ✅ Documente mudanças no CHANGELOG.md
- ✅ Use comentários no código quando necessário
- ✅ Mantenha exemplos funcionais

## 🛠️ Comandos Úteis

### Git

```bash
# Ver status dos arquivos
git status

# Adicionar arquivos modificados
git add .

# Fazer commit
git commit -m "feat: nova funcionalidade"

# Enviar para o GitHub
git push

# Atualizar repositório local
git pull

# Ver histórico de commits
git log --oneline --graph

# Criar e trocar de branch
git checkout -b nova-branch

# Merge de branches
git merge nome-da-branch
```

### Aplicação

```bash
# Iniciar servidor de desenvolvimento
uvicorn src.api:app --reload --port 8001

# Iniciar com logs detalhados
uvicorn src.api:app --reload --port 8001 --log-level debug

# Testar API
curl -X GET http://127.0.0.1:8001/api/health

# Executar testes
python -m pytest tests/

# Verificar dependências
pip list --outdated

# Atualizar requirements.txt
pip freeze > requirements.txt
```

## 🚨 Solução de Problemas

### Erro de Autenticação no GitHub

Se receber erro de autenticação ao fazer push:

1. **Personal Access Token**:
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token com escopo `repo`
   - Use o token como senha

2. **SSH Keys** (alternativa):
   ```bash
   ssh-keygen -t ed25519 -C "seu-email@example.com"
   cat ~/.ssh/id_ed25519.pub
   # Adicionar a chave no GitHub → Settings → SSH Keys
   ```

### Problemas de Deploy

1. **Dependências**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

2. **Porta em uso**:
   ```bash
   # Windows
   netstat -ano | findstr :8001
   taskkill /PID <PID> /F
   
   # Linux/Mac
   lsof -ti:8001 | xargs kill -9
   ```

3. **Variáveis de ambiente**:
   ```bash
   # Verificar se estão carregadas
   python -c "import os; print(os.getenv('GEMINI_API_KEY'))"
   ```

### Performance Issues

1. **Timeout de API**:
   - Aumentar timeout para 180s
   - Verificar status do provedor LLM
   - Usar fallback entre provedores

2. **Memória**:
   - Monitorar uso durante geração
   - Implementar cache se necessário
   - Limitar requisições simultâneas

## 📈 Próximos Passos

Após o deploy bem-sucedido:

1. **🔒 Segurança**:
   - Implementar autenticação (JWT)
   - Rate limiting
   - Logs de auditoria

2. **📊 Analytics**:
   - Google Analytics na interface web
   - Métricas de uso da API
   - Dashboard de monitoramento

3. **🚀 Funcionalidades**:
   - Cache de artigos gerados
   - Histórico de gerações
   - Exportação em múltiplos formatos
   - API de busca de artigos

4. **🤝 Comunidade**:
   - Adicionar licença MIT
   - Configurar GitHub Actions (CI/CD)
   - Criar templates de issues
   - Wiki com casos de uso

5. **📱 Mobile**:
   - PWA (Progressive Web App)
   - App mobile nativo
   - API mobile-friendly

## 🔗 Recursos Adicionais

- **Documentação do Git**: [git-scm.com/doc](https://git-scm.com/doc)
- **Guia do GitHub**: [guides.github.com](https://guides.github.com/)
- **FastAPI Deploy**: [fastapi.tiangolo.com/deployment](https://fastapi.tiangolo.com/deployment/)
- **Docker Docs**: [docs.docker.com](https://docs.docker.com/)
- **Conventional Commits**: [conventionalcommits.org](https://www.conventionalcommits.org/)

---

**🎉 Parabéns!** Sua aplicação de geração de artigos com interface web está pronta para o mundo!


