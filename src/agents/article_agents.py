"""
Definição dos agentes para o sistema de geração de artigos.

Este módulo implementa os agentes especializados usando CrewAI,
aplicando técnicas de engenharia de prompts para otimizar os resultados.
"""

from crewai import Agent, Task, Crew
from typing import List
from src.tools.wikipedia_tool import create_wikipedia_tool


class ArticleAgents:
    """
    Classe para gerenciar os agentes de geração de artigos.
    
    Implementa dois agentes principais:
    1. Researcher: Pesquisa e coleta informações
    2. Writer: Cria o artigo baseado na pesquisa
    """
    
    def __init__(self, llm=None):
        """
        Inicializa os agentes com configuração de LLM.
        
        Args:
            llm: Instância do modelo de linguagem a ser usado
        """
        self.llm = llm
        self.wikipedia_tool = create_wikipedia_tool()
    
    def create_researcher_agent(self) -> Agent:
        """
        Cria o agente pesquisador.
        
        Técnicas de Prompt Engineering aplicadas:
        - Role-based prompting: Define claramente o papel do agente
        - Chain-of-thought: Incentiva raciocínio passo a passo
        - Few-shot learning: Fornece exemplos do comportamento esperado
        
        Returns:
            Agent: Agente pesquisador configurado
        """
        return Agent(
            role="Pesquisador Especializado em Conteúdo",
            goal=(
                "Pesquisar informações precisas, relevantes e abrangentes sobre o tópico solicitado, "
                "coletando dados factuais da Wikipedia e outras fontes confiáveis para fornecer "
                "um contexto rico e bem fundamentado para a criação de artigos."
            ),
            backstory=(
                "Você é um pesquisador experiente com formação em jornalismo investigativo e "
                "biblioteconomia. Trabalhou por anos em grandes enciclopédias e bases de conhecimento, "
                "desenvolvendo expertise em encontrar, validar e sintetizar informações de múltiplas fontes. "
                "Você tem um olhar crítico para distinguir fatos de opiniões e sempre busca "
                "as fontes mais confiáveis e atualizadas. Sua metodologia de pesquisa é sistemática: "
                "primeiro você identifica os conceitos-chave, depois busca definições precisas, "
                "contexto histórico, aplicações práticas e informações complementares relevantes. "
                "Você sempre cita suas fontes e organiza as informações de forma lógica e estruturada."
            ),
            tools=[self.wikipedia_tool],
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=5,  # Limita iterações para evitar loops
        )
    
    def create_writer_agent(self) -> Agent:
        """
        Cria o agente escritor.
        
        Técnicas de Prompt Engineering aplicadas:
        - Role-based prompting: Define o papel de escritor profissional
        - Structured output: Especifica formato e estrutura esperados
        - Constraint-based prompting: Define limites claros (mínimo de palavras)
        - Style guidance: Orienta tom e estilo de escrita
        
        Returns:
            Agent: Agente escritor configurado
        """
        return Agent(
            role="Redator Profissional de Conteúdo",
            goal=(
                "Criar artigos informativos, bem estruturados e envolventes com no mínimo 300 palavras, "
                "transformando pesquisas em conteúdo de alta qualidade que seja ao mesmo tempo "
                "educativo e acessível para o público geral."
            ),
            backstory=(
                "Você é um redator profissional com mais de 10 anos de experiência em criação de "
                "conteúdo para websites, blogs e publicações digitais. Formado em Letras e com "
                "especialização em Comunicação Digital, você domina a arte de transformar informações "
                "técnicas e complexas em textos claros, objetivos e interessantes. "
                "\n\n"
                "Seu estilo de escrita é caracterizado por:\n"
                "- Introduções cativantes que prendem a atenção do leitor\n"
                "- Estrutura lógica com parágrafos bem conectados\n"
                "- Uso de exemplos práticos e analogias quando apropriado\n"
                "- Linguagem clara e acessível, evitando jargões desnecessários\n"
                "- Conclusões que sintetizam os pontos principais\n"
                "\n"
                "Você sempre se certifica de que seus artigos tenham:\n"
                "1. Um título atraente e descritivo\n"
                "2. Uma introdução que contextualiza o tema\n"
                "3. Desenvolvimento organizado em seções lógicas\n"
                "4. Mínimo de 300 palavras de conteúdo substantivo\n"
                "5. Conclusão que agrega valor\n"
                "\n"
                "Você valoriza a precisão factual e sempre baseia seu conteúdo nas pesquisas fornecidas, "
                "citando fontes quando apropriado. Seu objetivo é educar e informar, mantendo o leitor "
                "engajado do início ao fim."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            max_iter=3,
        )
    
    def create_research_task(self, agent: Agent, topic: str) -> Task:
        """
        Cria a tarefa de pesquisa.
        
        Args:
            agent (Agent): Agente pesquisador
            topic (str): Tópico a ser pesquisado
            
        Returns:
            Task: Tarefa de pesquisa configurada
        """
        return Task(
            description=(
                f"Realize uma pesquisa abrangente sobre o tema: '{topic}'.\n\n"
                "Siga este processo sistemático:\n"
                "1. Use a ferramenta Wikipedia Search Tool para buscar informações sobre o tópico\n"
                "2. Identifique e extraia os seguintes elementos:\n"
                "   - Definição clara e precisa do conceito\n"
                "   - Contexto histórico e evolução\n"
                "   - Principais características e componentes\n"
                "   - Aplicações práticas e exemplos\n"
                "   - Relevância e impacto atual\n"
                "3. Organize as informações de forma lógica e estruturada\n"
                "4. Anote todas as fontes consultadas\n\n"
                "Importante: Foque em informações factuais e verificáveis. "
                "Colete dados suficientes para permitir a criação de um artigo completo e informativo."
            ),
            agent=agent,
            expected_output=(
                "Um relatório de pesquisa estruturado contendo:\n"
                "- Resumo executivo do tópico\n"
                "- Informações detalhadas organizadas por categoria\n"
                "- Lista de fontes consultadas com URLs\n"
                "- Insights e pontos-chave para o artigo\n\n"
                "O relatório deve ter informação suficiente para permitir a criação "
                "de um artigo de no mínimo 300 palavras."
            )
        )
    
    def create_writing_task(self, agent: Agent, topic: str, context_task: Task) -> Task:
        """
        Cria a tarefa de escrita.
        
        Args:
            agent (Agent): Agente escritor
            topic (str): Tópico do artigo
            context_task (Task): Tarefa de pesquisa (para contexto)
            
        Returns:
            Task: Tarefa de escrita configurada
        """
        return Task(
            description=(
                f"Escreva um artigo completo e informativo sobre: '{topic}'.\n\n"
                "Use a pesquisa fornecida pelo agente pesquisador como base.\n\n"
                "Estrutura obrigatória do artigo:\n"
                "1. **Título**: Crie um título atraente e descritivo (use # para markdown)\n"
                "2. **Introdução**: 1-2 parágrafos contextualizando o tema e sua importância\n"
                "3. **Desenvolvimento**: 3-5 seções explorando diferentes aspectos do tema\n"
                "   - Use subtítulos (## para markdown) para organizar as seções\n"
                "   - Desenvolva cada seção com informações substantivas\n"
                "   - Use exemplos e explicações claras\n"
                "4. **Conclusão**: 1-2 parágrafos sintetizando os pontos principais\n\n"
                "Requisitos técnicos:\n"
                "- Mínimo de 300 palavras de conteúdo\n"
                "- Formato: Markdown\n"
                "- Tom: Informativo, educativo e acessível\n"
                "- Linguagem: Clara e objetiva, evitando jargões excessivos\n"
                "- Parágrafos: Bem conectados com transições suaves\n\n"
                "Importante: Baseie-se APENAS nas informações da pesquisa fornecida. "
                "Não invente fatos ou dados. Se a pesquisa for insuficiente, indique isso."
            ),
            agent=agent,
            expected_output=(
                "Um artigo completo em formato Markdown contendo:\n"
                "- Título em H1 (#)\n"
                "- Introdução contextualizada\n"
                "- Desenvolvimento organizado em seções com subtítulos (##)\n"
                "- Conclusão sintetizando os pontos principais\n"
                "- Mínimo de 300 palavras\n"
                "- Linguagem clara e acessível\n"
                "- Baseado nas informações da pesquisa\n\n"
                "O artigo deve ser informativo, bem escrito e pronto para publicação."
            ),
            context=[context_task],  # Recebe o output da tarefa de pesquisa
        )


def create_article_crew(topic: str, llm=None) -> Crew:
    """
    Factory function para criar uma Crew completa de geração de artigos.
    
    Args:
        topic (str): Tópico do artigo a ser gerado
        llm: Instância do modelo de linguagem
        
    Returns:
        Crew: Crew configurada e pronta para execução
    """
    # Criar instância dos agentes
    agents_manager = ArticleAgents(llm=llm)
    
    # Criar agentes
    researcher = agents_manager.create_researcher_agent()
    writer = agents_manager.create_writer_agent()
    
    # Criar tarefas
    research_task = agents_manager.create_research_task(researcher, topic)
    writing_task = agents_manager.create_writing_task(writer, topic, research_task)
    
    # Criar e retornar a Crew
    return Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        verbose=True,
    )

