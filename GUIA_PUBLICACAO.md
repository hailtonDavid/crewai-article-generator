# Guia de Publicação no GitHub

Este documento fornece instruções passo a passo para publicar o projeto no GitHub.

## Pré-requisitos


1. **Conta no GitHub**: Crie uma conta em [github.com](https://github.com) se ainda não tiver.
2. **Git instalado**: Verifique com `git --version`.
3. **Repositório local inicializado**: O projeto já foi inicializado com Git.

## Passos para Publicação

### 1. Criar Repositório no GitHub


1. Acesse [github.com](https://github.com) e faça login.
2. Clique no botão **"+"** no canto superior direito e selecione **"New repository"**.
3. Configure o repositório:
   * **Repository name**: `crewai-article-generator`
   * **Description**: "Sistema Multiagente para Geração de Artigos usando CrewAI"
   * **Visibility**: Selecione **Public**
   * **NÃO** marque "Initialize this repository with a README" (já temos um README local)
4. Clique em **"Create repository"**.

### 2. Conectar o Repositório Local ao GitHub

Após criar o repositório, o GitHub mostrará instruções. Execute os seguintes comandos no terminal:

```bash
cd /home/ubuntu/crewai-article-generator

# Adicionar o repositório remoto
git remote add origin https://github.com/SEU-USUARIO/crewai-article-generator.git

# Renomear a branch para 'main' (opcional, mas recomendado)
git branch -M main

# Fazer push do código para o GitHub
git push -u origin main
```

**Importante**: Substitua `SEU-USUARIO` pelo seu nome de usuário do GitHub.

### 3. Verificar a Publicação

Acesse `https://github.com/SEU-USUARIO/crewai-article-generator` no navegador para verificar se todos os arquivos foram enviados corretamente.

## Estrutura de Branches (Opcional)

Para projetos mais complexos, considere criar branches para desenvolvimento:

```bash
# Criar branch de desenvolvimento
git checkout -b develop

# Fazer alterações e commit
git add .
git commit -m "feat: Nova funcionalidade"

# Enviar para o GitHub
git push origin develop
```

## Boas Práticas


1. **Commits Semânticos**: Use prefixos como `feat:`, `fix:`, `docs:`, `refactor:`, etc.
2. **Arquivo .env**: Nunca faça commit do arquivo `.env` com chaves de API reais. Use `.env.example`.
3. **Documentação**: Mantenha o README.md sempre atualizado.
4. **Issues e Pull Requests**: Use as funcionalidades do GitHub para gerenciar melhorias e bugs.

## Comandos Úteis do Git

```bash
# Ver status dos arquivos
git status

# Adicionar arquivos modificados
git add .

# Fazer commit
git commit -m "Mensagem descritiva"

# Enviar para o GitHub
git push

# Atualizar repositório local
git pull

# Ver histórico de commits
git log --oneline
```

## Próximos Passos

Após publicar no GitHub, você pode:


1. **Adicionar uma licença**: Crie um arquivo `LICENSE` (MIT é recomendado).
2. **Configurar GitHub Actions**: Automatize testes e deploy.
3. **Criar uma Wiki**: Documente casos de uso e exemplos avançados.
4. **Adicionar badges**: Mostre o status de build, cobertura de testes, etc.
5. **Compartilhar**: Divulgue o projeto em comunidades de IA e desenvolvimento.

## Problemas Comuns

### Erro de autenticação ao fazer push

Se você receber erro de autenticação, configure um Personal Access Token:


1. Acesse GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Clique em "Generate new token"
3. Selecione os escopos necessários (repo, workflow)
4. Use o token como senha ao fazer push

### Arquivo muito grande

Se algum arquivo for muito grande (>100MB), use Git LFS:

```bash
git lfs install
git lfs track "*.modelo"
git add .gitattributes
```

## Recursos Adicionais

* [Documentação do Git](https://git-scm.com/doc)
* [Guia do GitHub](https://guides.github.com/)
* [Conventional Commits](https://www.conventionalcommits.org/)


