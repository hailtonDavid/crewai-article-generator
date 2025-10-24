"""
Modelos Pydantic para validação e estruturação de dados.

Define os schemas de entrada e saída para o sistema de geração de artigos.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class ArticleRequest(BaseModel):
    """
    Schema para requisição de geração de artigo.
    
    Attributes:
        topic (str): Tópico do artigo a ser gerado
        language (str): Idioma do artigo (padrão: 'pt')
        min_words (int): Número mínimo de palavras (padrão: 300)
    """
    
    topic: str = Field(
        ...,
        description="Tópico ou assunto do artigo a ser gerado",
        min_length=3,
        max_length=200,
        example="Inteligência Artificial"
    )
    
    language: str = Field(
        default="pt",
        description="Código do idioma do artigo",
        pattern="^[a-z]{2}$",
        example="pt"
    )
    
    min_words: int = Field(
        default=300,
        description="Número mínimo de palavras no artigo",
        ge=100,
        le=2000,
        example=300
    )
    
    @validator('topic')
    def topic_must_not_be_empty(cls, v):
        """Valida que o tópico não seja apenas espaços em branco."""
        if not v.strip():
            raise ValueError('O tópico não pode ser vazio')
        return v.strip()


class ArticleMetadata(BaseModel):
    """
    Metadados do artigo gerado.
    
    Attributes:
        generated_at (datetime): Data e hora de geração
        language (str): Idioma do artigo
        topic (str): Tópico original
        agent_info (Dict): Informações sobre os agentes utilizados
    """
    
    generated_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp de geração do artigo"
    )
    
    language: str = Field(
        ...,
        description="Idioma do artigo gerado"
    )
    
    topic: str = Field(
        ...,
        description="Tópico original da requisição"
    )
    
    agent_info: Dict[str, str] = Field(
        default_factory=dict,
        description="Informações sobre os agentes que geraram o artigo"
    )


class ArticleOutput(BaseModel):
    """
    Schema para output estruturado do artigo gerado.
    
    Este modelo garante que o artigo gerado pela Crew tenha
    todos os campos necessários e esteja devidamente validado.
    
    Attributes:
        title (str): Título do artigo
        content (str): Conteúdo completo do artigo
        word_count (int): Contagem de palavras
        sources (List[str]): Lista de fontes consultadas
        metadata (ArticleMetadata): Metadados do artigo
        summary (str): Resumo executivo do artigo
    """
    
    title: str = Field(
        ...,
        description="Título do artigo gerado",
        min_length=10,
        max_length=200,
        example="Inteligência Artificial: Conceitos e Aplicações"
    )
    
    content: str = Field(
        ...,
        description="Conteúdo completo do artigo em formato markdown",
        min_length=300,
        example="# Introdução\n\nA inteligência artificial..."
    )
    
    word_count: int = Field(
        ...,
        description="Número total de palavras no artigo",
        ge=100,
        example=450
    )
    
    sources: List[str] = Field(
        default_factory=list,
        description="Lista de URLs das fontes consultadas",
        example=["https://pt.wikipedia.org/wiki/Inteligência_artificial"]
    )
    
    metadata: ArticleMetadata = Field(
        ...,
        description="Metadados do artigo"
    )
    
    summary: Optional[str] = Field(
        None,
        description="Resumo executivo do artigo (opcional)",
        max_length=500
    )
    
    @validator('content')
    def content_must_have_minimum_words(cls, v, values):
        """Valida que o conteúdo tenha o número mínimo de palavras."""
        word_count = len(v.split())
        if word_count < 100:
            raise ValueError(f'O artigo deve ter no mínimo 100 palavras, mas tem apenas {word_count}')
        return v
    
    @validator('word_count', always=True)
    def calculate_word_count(cls, v, values):
        """Calcula automaticamente a contagem de palavras se não fornecida."""
        if 'content' in values:
            return len(values['content'].split())
        return v


class ArticleResponse(BaseModel):
    """
    Schema para resposta da API.
    
    Attributes:
        success (bool): Indica se a geração foi bem-sucedida
        message (str): Mensagem descritiva
        article (ArticleOutput): Artigo gerado (se sucesso)
        error (str): Mensagem de erro (se falha)
    """
    
    success: bool = Field(
        ...,
        description="Indica se a operação foi bem-sucedida"
    )
    
    message: str = Field(
        ...,
        description="Mensagem descritiva do resultado"
    )
    
    article: Optional[ArticleOutput] = Field(
        None,
        description="Artigo gerado (presente apenas se success=True)"
    )
    
    error: Optional[str] = Field(
        None,
        description="Detalhes do erro (presente apenas se success=False)"
    )


class HealthResponse(BaseModel):
    """
    Schema para resposta do endpoint de health check.
    
    Attributes:
        status (str): Status do sistema
        timestamp (datetime): Timestamp da verificação
        version (str): Versão do sistema
    """
    
    status: str = Field(
        default="healthy",
        description="Status do sistema"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp da verificação"
    )
    
    version: str = Field(
        default="1.0.0",
        description="Versão do sistema"
    )

