"""
Script de teste do sistema completo de geração de artigos.

Este script testa a integração completa:
- Ferramenta Wikipedia
- Agentes CrewAI
- Geração de artigos
- Validação Pydantic
"""

import os
import sys
from datetime import datetime

# Configurar variável de ambiente para teste
# Em produção, usar arquivo .env
os.environ["GEMINI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")  # Usar a key disponível
os.environ["LLM_PROVIDER"] = "gemini"

from src.crew import ArticleGenerator
from src.models.article_models import ArticleRequest


def test_wikipedia_tool():
    """Testa a ferramenta Wikipedia."""
    print("\n" + "="*70)
    print("TESTE 1: Ferramenta Wikipedia")
    print("="*70)
    
    try:
        from src.tools.wikipedia_tool import create_wikipedia_tool
        
        tool = create_wikipedia_tool()
        result = tool._run("Inteligência Artificial")
        
        if result and len(result) > 100:
            print("✓ Ferramenta Wikipedia funcionando")
            print(f"  Tamanho do resultado: {len(result)} caracteres")
            print(f"  Preview: {result[:150]}...")
            return True
        else:
            print("✗ Ferramenta retornou resultado vazio ou muito curto")
            return False
            
    except Exception as e:
        print(f"✗ Erro ao testar ferramenta: {e}")
        return False


def test_pydantic_models():
    """Testa os modelos Pydantic."""
    print("\n" + "="*70)
    print("TESTE 2: Modelos Pydantic")
    print("="*70)
    
    try:
        from src.models.article_models import ArticleRequest, ArticleOutput, ArticleMetadata
        
        # Testar ArticleRequest
        request = ArticleRequest(
            topic="Teste",
            language="pt",
            min_words=300
        )
        print(f"✓ ArticleRequest validado: {request.topic}")
        
        # Testar ArticleMetadata
        metadata = ArticleMetadata(
            language="pt",
            topic="Teste",
            agent_info={"test": "value"}
        )
        print(f"✓ ArticleMetadata criado: {metadata.generated_at}")
        
        # Testar ArticleOutput
        article = ArticleOutput(
            title="Título de Teste",
            content="Este é um conteúdo de teste " * 50,  # ~300 palavras
            word_count=300,
            sources=["https://test.com"],
            metadata=metadata
        )
        print(f"✓ ArticleOutput validado: {article.word_count} palavras")
        
        return True
        
    except Exception as e:
        print(f"✗ Erro ao testar modelos: {e}")
        return False


def test_article_generation():
    """Testa a geração completa de artigos."""
    print("\n" + "="*70)
    print("TESTE 3: Geração de Artigo Completo")
    print("="*70)
    
    # Verificar se temos API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠ API key não disponível - pulando teste de geração")
        print("  Para testar completamente, configure GEMINI_API_KEY, GROQ_API_KEY ou OPENROUTER_API_KEY")
        return None
    
    try:
        print("Criando gerador de artigos...")
        
        # Usar o modelo disponível via OPENAI_API_KEY
        generator = ArticleGenerator(llm_provider="gemini")
        
        print("Criando requisição...")
        request = ArticleRequest(
            topic="Futebol",
            language="pt",
            min_words=300
        )
        
        print(f"Gerando artigo sobre '{request.topic}'...")
        print("(Isso pode levar alguns minutos...)\n")
        
        response = generator.generate_article(request)
        
        if response.success:
            article = response.article
            print("✓ Artigo gerado com sucesso!")
            print(f"  Título: {article.title}")
            print(f"  Palavras: {article.word_count}")
            print(f"  Fontes: {len(article.sources)}")
            print(f"\n  Preview do conteúdo:")
            print("  " + "-"*66)
            preview = article.content[:300].replace('\n', '\n  ')
            print(f"  {preview}...")
            print("  " + "-"*66)
            return True
        else:
            print(f"✗ Falha na geração: {response.error}")
            return False
            
    except Exception as e:
        print(f"✗ Erro ao gerar artigo: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Executa todos os testes."""
    print("\n" + "="*70)
    print("SISTEMA DE TESTES - CrewAI Article Generator")
    print("="*70)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Teste 1: Wikipedia Tool
    results.append(("Wikipedia Tool", test_wikipedia_tool()))
    
    # Teste 2: Pydantic Models
    results.append(("Pydantic Models", test_pydantic_models()))
    
    # Teste 3: Article Generation
    gen_result = test_article_generation()
    if gen_result is not None:
        results.append(("Article Generation", gen_result))
    
    # Resumo
    print("\n" + "="*70)
    print("RESUMO DOS TESTES")
    print("="*70)
    
    for name, result in results:
        status = "✓ PASSOU" if result else "✗ FALHOU"
        print(f"{status}: {name}")
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram com sucesso!")
        return 0
    else:
        print("\n⚠ Alguns testes falharam. Verifique os detalhes acima.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

