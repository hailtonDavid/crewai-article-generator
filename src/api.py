"""
API REST para o sistema de geração de artigos.

Implementa endpoints usando FastAPI para permitir acesso
programático ao sistema de geração de artigos via HTTP.
"""

import os
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError

from src.models.article_models import (
    ArticleRequest,
    ArticleResponse,
    HealthResponse
)
from src.crew import ArticleGenerator


# Criar instância do FastAPI
app = FastAPI(
    title="Sistema Multiagente de Geração de Artigos",
    description=(
        "API REST para geração automatizada de artigos usando CrewAI. "
        "O sistema utiliza agentes especializados (Pesquisador e Escritor) "
        "que colaboram para criar artigos informativos baseados em pesquisa da Wikipedia."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


# Variável global para armazenar o gerador
# Em produção, considerar usar dependency injection
_generator: Optional[ArticleGenerator] = None


def get_generator() -> ArticleGenerator:
    """
    Obtém ou cria uma instância do ArticleGenerator.
    
    Returns:
        ArticleGenerator: Instância configurada
    """
    global _generator
    
    if _generator is None:
        # Determinar provedor de LLM baseado em variáveis de ambiente
        llm_provider = os.getenv("LLM_PROVIDER", "gemini")
        
        # Validar que a API key está disponível
        provider_env_vars = {
            "gemini": "GEMINI_API_KEY",
            "groq": "GROQ_API_KEY",
            "openrouter": "OPENROUTER_API_KEY"
        }
        
        env_var = provider_env_vars.get(llm_provider)
        if env_var and not os.getenv(env_var):
            raise ValueError(
                f"API key não configurada. Defina a variável de ambiente {env_var}"
            )
        
        _generator = ArticleGenerator(llm_provider=llm_provider)
    
    return _generator


@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raiz da API - serve a interface web.
    
    Returns:
        FileResponse: Página HTML principal da interface
    """
    return FileResponse("static/index.html")


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Verifica o status de saúde da API.
    
    Returns:
        HealthResponse: Status do sistema
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )


@app.post(
    "/api/generate-article",
    response_model=ArticleResponse,
    status_code=status.HTTP_200_OK,
    tags=["Articles"],
    summary="Gera um artigo sobre um tópico específico",
    description=(
        "Endpoint principal para geração de artigos. "
        "Recebe um tópico e retorna um artigo completo gerado "
        "por agentes especializados usando pesquisa da Wikipedia."
    )
)
async def generate_article(request: ArticleRequest) -> ArticleResponse:
    """
    Gera um artigo baseado no tópico fornecido.
    
    Args:
        request (ArticleRequest): Requisição com tópico e parâmetros
        
    Returns:
        ArticleResponse: Artigo gerado ou mensagem de erro
        
    Raises:
        HTTPException: Em caso de erro na geração
    """
    try:
        # Obter gerador
        generator = get_generator()
        
        # Gerar artigo
        response = generator.generate_article(request)
        
        # Se não teve sucesso, retornar erro HTTP
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=response.error or "Erro desconhecido ao gerar artigo"
            )
        
        return response
        
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Erro de validação: {str(e)}"
        )
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno do servidor: {str(e)}"
        )


@app.get("/api/providers", tags=["Configuration"])
async def list_providers():
    """
    Lista os provedores de LLM suportados.
    
    Returns:
        dict: Lista de provedores e suas configurações
    """
    return {
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
        "current_provider": os.getenv("LLM_PROVIDER", "gemini")
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Handler global para exceções não tratadas.
    
    Args:
        request: Requisição HTTP
        exc: Exceção capturada
        
    Returns:
        JSONResponse: Resposta de erro formatada
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Erro interno do servidor",
            "error": str(exc)
        }
    )


# Evento de inicialização
@app.on_event("startup")
async def startup_event():
    """
    Executado quando a API inicia.
    Valida configurações e prepara o sistema.
    """
    print("🚀 Iniciando Sistema Multiagente de Geração de Artigos...")
    print(f"📝 Provedor LLM: {os.getenv('LLM_PROVIDER', 'gemini')}")
    
    # Tentar inicializar o gerador para validar configuração
    try:
        get_generator()
        print("✓ Gerador de artigos inicializado com sucesso")
    except Exception as e:
        print(f"⚠ Aviso: Erro ao inicializar gerador: {e}")
        print("   A API continuará funcionando, mas pode falhar ao gerar artigos")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Executado quando a API é desligada.
    Limpa recursos se necessário.
    """
    print("👋 Encerrando Sistema Multiagente de Geração de Artigos...")


if __name__ == "__main__":
    import uvicorn
    
    # Configuração do servidor
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Iniciando servidor em http://{host}:{port}")
    print(f"Documentação disponível em http://{host}:{port}/docs")
    
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=True,  # Auto-reload em desenvolvimento
        log_level="info"
    )

