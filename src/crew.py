"""
Módulo principal para orquestração da Crew de geração de artigos.

Este módulo integra os agentes, tarefas e ferramentas para
executar o processo completo de geração de artigos.
"""

import os
from datetime import datetime
from typing import Optional, Dict, Any
from crewai import LLM

from src.agents.article_agents import create_article_crew
from src.models.article_models import (
    ArticleOutput,
    ArticleMetadata,
    ArticleRequest,
    ArticleResponse
)


class ArticleGenerator:
    """
    Classe principal para geração de artigos usando CrewAI.
    
    Gerencia a configuração do LLM, execução da Crew e
    formatação do output usando Pydantic.
    """
    
    def __init__(self, llm_provider: str = "gemini", api_key: Optional[str] = None):
        """
        Inicializa o gerador de artigos.
        
        Args:
            llm_provider (str): Provedor de LLM ('gemini', 'groq', 'openrouter')
            api_key (str): Chave de API (se None, busca de variável de ambiente)
        """
        self.llm_provider = llm_provider
        self.llm = self._setup_llm(llm_provider, api_key)
    
    def _setup_llm(self, provider: str, api_key: Optional[str] = None) -> LLM:
        """
        Configura o LLM baseado no provedor escolhido.
        
        Args:
            provider (str): Nome do provedor
            api_key (str): Chave de API
            
        Returns:
            LLM: Instância configurada do LLM
        """
        # Mapeamento de provedores e modelos
        # Usar modelos disponíveis via OpenAI-compatible API
        provider_config = {
            "gemini": {
                "model": "gemini-2.5-flash",
                "env_var": "GEMINI_API_KEY",
            },
            "groq": {
                "model": "groq/llama-3.3-70b-versatile",
                "env_var": "GROQ_API_KEY",
            },
            "openrouter": {
                "model": "openrouter/google/gemini-2.0-flash-exp:free",
                "env_var": "OPENROUTER_API_KEY",
            }
        }
        
        if provider not in provider_config:
            raise ValueError(
                f"Provedor '{provider}' não suportado. "
                f"Use: {', '.join(provider_config.keys())}"
            )
        
        config = provider_config[provider]
        
        # Obter API key
        final_api_key = api_key or os.getenv(config["env_var"])
        
        if not final_api_key:
            raise ValueError(
                f"API key não fornecida para {provider}. "
                f"Defina a variável de ambiente {config['env_var']} "
                f"ou passe api_key no construtor."
            )
        
        # Criar instância do LLM
        return LLM(
            model=config["model"],
            api_key=final_api_key,
            temperature=0.7,  # Criatividade moderada
        )
    
    def generate_article(self, request: ArticleRequest) -> ArticleResponse:
        """
        Gera um artigo baseado na requisição.
        
        Args:
            request (ArticleRequest): Requisição validada com Pydantic
            
        Returns:
            ArticleResponse: Resposta estruturada com o artigo ou erro
        """
        try:
            # Criar a Crew para o tópico
            crew = create_article_crew(topic=request.topic, llm=self.llm)
            
            # Executar a Crew
            result = crew.kickoff()
            
            # Extrair o conteúdo do resultado
            article_content = str(result)
            
            # Extrair título (primeira linha com #)
            lines = article_content.split('\n')
            title = request.topic  # Fallback
            content_without_title = article_content
            
            for i, line in enumerate(lines):
                if line.strip().startswith('#'):
                    title = line.strip().lstrip('#').strip()
                    content_without_title = '\n'.join(lines[i:])
                    break
            
            # Calcular contagem de palavras
            word_count = len(article_content.split())
            
            # Verificar se atende ao mínimo de palavras
            if word_count < request.min_words:
                return ArticleResponse(
                    success=False,
                    message=f"Artigo gerado tem apenas {word_count} palavras, "
                            f"mínimo requerido: {request.min_words}",
                    error="Artigo não atende ao requisito mínimo de palavras"
                )
            
            # Criar metadados
            metadata = ArticleMetadata(
                generated_at=datetime.now(),
                language=request.language,
                topic=request.topic,
                agent_info={
                    "llm_provider": self.llm_provider,
                    "agents": "Researcher, Writer",
                    "framework": "CrewAI"
                }
            )
            
            # Criar output estruturado
            article_output = ArticleOutput(
                title=title,
                content=content_without_title,
                word_count=word_count,
                sources=[
                    f"https://{request.language}.wikipedia.org/wiki/{request.topic.replace(' ', '_')}"
                ],
                metadata=metadata,
                summary=None  # Pode ser adicionado em versões futuras
            )
            
            return ArticleResponse(
                success=True,
                message=f"Artigo gerado com sucesso! {word_count} palavras.",
                article=article_output
            )
            
        except Exception as e:
            return ArticleResponse(
                success=False,
                message="Erro ao gerar artigo",
                error=str(e)
            )
    
    def generate_article_simple(self, topic: str, min_words: int = 300) -> Dict[str, Any]:
        """
        Método simplificado para geração de artigos.
        
        Args:
            topic (str): Tópico do artigo
            min_words (int): Número mínimo de palavras
            
        Returns:
            Dict: Dicionário com o resultado
        """
        request = ArticleRequest(topic=topic, min_words=min_words)
        response = self.generate_article(request)
        
        if response.success:
            return {
                "success": True,
                "title": response.article.title,
                "content": response.article.content,
                "word_count": response.article.word_count,
                "sources": response.article.sources
            }
        else:
            return {
                "success": False,
                "error": response.error
            }


# Função auxiliar para uso direto
def generate_article(
    topic: str,
    min_words: int = 300,
    llm_provider: str = "gemini",
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Função auxiliar para gerar artigos diretamente.
    
    Args:
        topic (str): Tópico do artigo
        min_words (int): Número mínimo de palavras
        llm_provider (str): Provedor de LLM
        api_key (str): Chave de API
        
    Returns:
        Dict: Resultado da geração
    """
    generator = ArticleGenerator(llm_provider=llm_provider, api_key=api_key)
    return generator.generate_article_simple(topic=topic, min_words=min_words)


if __name__ == "__main__":
    # Exemplo de uso
    print("Gerando artigo sobre 'Inteligência Artificial'...")
    result = generate_article("Inteligência Artificial", min_words=300)
    
    if result["success"]:
        print(f"\n✓ Artigo gerado com sucesso!")
        print(f"Título: {result['title']}")
        print(f"Palavras: {result['word_count']}")
        print(f"\nConteúdo:\n{result['content'][:500]}...")
    else:
        print(f"\n✗ Erro: {result['error']}")

