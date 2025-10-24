"""
Ferramenta personalizada para consultar a API da Wikipedia.

Esta ferramenta permite que agentes CrewAI busquem informações
relevantes na Wikipedia em português para enriquecer o contexto
de geração de artigos.
"""

import requests
from typing import Type, Optional
from pydantic import BaseModel, Field
from crewai.tools import BaseTool


class WikipediaSearchInput(BaseModel):
    """Input schema para WikipediaTool."""
    topic: str = Field(..., description="Tópico ou termo a ser pesquisado na Wikipedia")


class WikipediaTool(BaseTool):
    """
    Ferramenta para consultar a API da Wikipedia e extrair conteúdo relevante.
    
    Attributes:
        name (str): Nome da ferramenta
        description (str): Descrição detalhada para o agente entender quando usar
        args_schema (Type[BaseModel]): Schema de validação dos argumentos
    """
    
    name: str = "Wikipedia Search Tool"
    description: str = (
        "Ferramenta para pesquisar informações na Wikipedia em português. "
        "Use esta ferramenta quando precisar de informações factuais, "
        "contexto histórico, definições ou dados enciclopédicos sobre qualquer tópico. "
        "A ferramenta retorna um resumo detalhado do artigo da Wikipedia. "
        "Input: o título ou termo de busca (string). "
        "Output: conteúdo extraído do artigo da Wikipedia."
    )
    args_schema: Type[BaseModel] = WikipediaSearchInput
    
    def _run(self, topic: str, language: str = "pt") -> str:
        """
        Executa a busca na Wikipedia.
        
        Args:
            topic (str): Tópico ou termo a ser pesquisado
            language (str): Código do idioma (padrão: 'pt')
            
        Returns:
            str: Conteúdo extraído do artigo ou mensagem de erro
        """
        try:
            base_url = f"https://{language}.wikipedia.org/w/api.php"
            
            # Parâmetros da API da Wikipedia
            params = {
                "action": "query",
                "prop": "extracts",
                "exlimit": 1,
                "explaintext": 1,
                "titles": topic,
                "format": "json",
                "utf8": 1,
                "redirects": 1,
                "exintro": 0,  # Não apenas a introdução, mas o artigo completo
            }
            
            # Fazer requisição à API com User-Agent
            headers = {
                "User-Agent": "CrewAI-Article-Generator/1.0 (Educational Project)"
            }
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extrair conteúdo da resposta
            pages = data.get("query", {}).get("pages", {})
            
            if not pages:
                return f"Nenhum resultado encontrado para '{topic}' na Wikipedia."
            
            # Pegar a primeira (e única) página
            page_id = list(pages.keys())[0]
            
            # Verificar se a página existe (page_id != -1)
            if page_id == "-1":
                return f"O artigo '{topic}' não foi encontrado na Wikipedia."
            
            page_data = pages[page_id]
            extract = page_data.get("extract", "")
            title = page_data.get("title", topic)
            
            if not extract:
                return f"O artigo '{title}' existe mas não possui conteúdo disponível."
            
            # Limitar o tamanho do conteúdo para não sobrecarregar o contexto
            # Pegar os primeiros 3000 caracteres (aproximadamente 500 palavras)
            if len(extract) > 3000:
                extract = extract[:3000] + "..."
            
            result = f"**Artigo da Wikipedia: {title}**\n\n{extract}\n\n"
            result += f"Fonte: https://{language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
            
            return result
            
        except requests.exceptions.Timeout:
            return f"Timeout ao buscar '{topic}' na Wikipedia. Tente novamente."
        
        except requests.exceptions.RequestException as e:
            return f"Erro ao acessar a Wikipedia: {str(e)}"
        
        except Exception as e:
            return f"Erro inesperado ao processar '{topic}': {str(e)}"


# Função auxiliar para criar instância da ferramenta
def create_wikipedia_tool() -> WikipediaTool:
    """
    Factory function para criar uma instância da WikipediaTool.
        
    Returns:
        WikipediaTool: Instância configurada da ferramenta
    """
    return WikipediaTool()


if __name__ == "__main__":
    # Teste básico da ferramenta
    tool = create_wikipedia_tool()
    result = tool._run("Inteligência Artificial")
    print(result)

