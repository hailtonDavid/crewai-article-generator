"""
Testes para as ferramentas personalizadas.

Testa a funcionalidade da WikipediaTool.
"""

import pytest
from src.tools.wikipedia_tool import WikipediaTool, create_wikipedia_tool


class TestWikipediaTool:
    """Testes para a WikipediaTool."""
    
    def test_create_tool(self):
        """Testa a criação da ferramenta."""
        tool = create_wikipedia_tool()
        assert tool is not None
        assert isinstance(tool, WikipediaTool)
        assert tool.language == "pt"
    
    def test_tool_attributes(self):
        """Testa os atributos da ferramenta."""
        tool = create_wikipedia_tool()
        assert tool.name == "Wikipedia Search Tool"
        assert "Wikipedia" in tool.description
        assert "pt.wikipedia.org" in tool.base_url
    
    def test_search_valid_topic(self):
        """Testa busca com tópico válido."""
        tool = create_wikipedia_tool()
        result = tool._run("Python (linguagem de programação)")
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 100
        assert "Python" in result
        assert "wikipedia.org" in result.lower()
    
    def test_search_invalid_topic(self):
        """Testa busca com tópico inválido."""
        tool = create_wikipedia_tool()
        result = tool._run("XYZ_TOPICO_INEXISTENTE_123456")
        
        assert result is not None
        assert isinstance(result, str)
        assert "não foi encontrado" in result.lower() or "nenhum resultado" in result.lower()
    
    def test_search_empty_topic(self):
        """Testa busca com tópico vazio."""
        tool = create_wikipedia_tool()
        result = tool._run("")
        
        assert result is not None
        assert isinstance(result, str)
    
    def test_different_language(self):
        """Testa criação de ferramenta com idioma diferente."""
        tool = WikipediaTool(language="en")
        assert tool.language == "en"
        assert "en.wikipedia.org" in tool.base_url


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

