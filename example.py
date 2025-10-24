"""
Exemplo de uso do Sistema Multiagente de Geração de Artigos.

Este script demonstra como usar o sistema para gerar artigos.
"""

import os
from dotenv import load_dotenv
from src.crew import ArticleGenerator
from src.models.article_models import ArticleRequest

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


def main():
    """Exemplo de geração de artigo."""
    
    print("="*70)
    print("Sistema Multiagente de Geração de Artigos - Exemplo")
    print("="*70)
    
    # Verificar se há API key configurada
    if not os.getenv("GEMINI_API_KEY") and not os.getenv("GROQ_API_KEY") and not os.getenv("OPENROUTER_API_KEY"):
        print("\n⚠ AVISO: Nenhuma API key configurada!")
        print("\nPara usar o sistema, configure uma das seguintes variáveis de ambiente:")
        print("  - GEMINI_API_KEY (Google Gemini - opção gratuita)")
        print("  - GROQ_API_KEY (Groq)")
        print("  - OPENROUTER_API_KEY (OpenRouter)")
        print("\nCopie o arquivo .env.example para .env e configure sua API key.")
        return
    
    # Configurar provedor (padrão: gemini)
    llm_provider = os.getenv("LLM_PROVIDER", "gemini")
    
    print(f"\n📝 Provedor LLM: {llm_provider}")
    print(f"🔧 Inicializando gerador de artigos...")
    
    try:
        # Criar gerador
        generator = ArticleGenerator(llm_provider=llm_provider)
        
        # Definir tópico
        topic = input("\n💡 Digite o tópico do artigo (ou Enter para 'Inteligência Artificial'): ").strip()
        if not topic:
            topic = "Inteligência Artificial"
        
        # Criar requisição
        request = ArticleRequest(
            topic=topic,
            language="pt",
            min_words=300
        )
        
        print(f"\n🚀 Gerando artigo sobre '{topic}'...")
        print("⏳ Isso pode levar alguns minutos. Aguarde...\n")
        
        # Gerar artigo
        response = generator.generate_article(request)
        
        if response.success:
            article = response.article
            
            print("\n" + "="*70)
            print("✅ ARTIGO GERADO COM SUCESSO!")
            print("="*70)
            print(f"\n📌 Título: {article.title}")
            print(f"📊 Palavras: {article.word_count}")
            print(f"📚 Fontes: {len(article.sources)}")
            print(f"🕐 Gerado em: {article.metadata.generated_at.strftime('%Y-%m-%d %H:%M:%S')}")
            
            print("\n" + "-"*70)
            print("CONTEÚDO DO ARTIGO:")
            print("-"*70)
            print(article.content)
            print("-"*70)
            
            # Salvar artigo em arquivo
            filename = f"artigo_{topic.replace(' ', '_').lower()}.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {article.title}\n\n")
                f.write(article.content)
                f.write(f"\n\n---\n")
                f.write(f"**Gerado em:** {article.metadata.generated_at.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"**Palavras:** {article.word_count}\n")
                f.write(f"**Fontes:**\n")
                for source in article.sources:
                    f.write(f"- {source}\n")
            
            print(f"\n💾 Artigo salvo em: {filename}")
            
        else:
            print("\n" + "="*70)
            print("❌ ERRO AO GERAR ARTIGO")
            print("="*70)
            print(f"\n{response.error}")
            
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

