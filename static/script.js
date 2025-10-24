// Elementos DOM
const articleForm = document.getElementById('articleForm');
const generateBtn = document.getElementById('generateBtn');
const loading = document.getElementById('loading');
const resultCard = document.getElementById('resultCard');
const error = document.getElementById('error');
const errorMessage = document.getElementById('errorMessage');
const articleMeta = document.getElementById('articleMeta');
const articleContent = document.getElementById('articleContent');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');

// Estado da aplicação
let currentArticle = null;

// Event Listeners
articleForm.addEventListener('submit', handleFormSubmit);
copyBtn.addEventListener('click', copyArticle);
downloadBtn.addEventListener('click', downloadArticle);

// Função principal para submissão do formulário
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(articleForm);
    const requestData = {
        topic: formData.get('topic'),
        min_words: parseInt(formData.get('minWords')),
        style: formData.get('style')
    };

    try {
        showLoading();
        hideError();
        hideResult();
        
        const response = await generateArticle(requestData);
        
        if (response.success) {
            currentArticle = response;
            showResult(response);
        } else {
            showError(response.error || 'Erro desconhecido ao gerar artigo');
        }
    } catch (err) {
        console.error('Erro:', err);
        showError('Erro de conexão com o servidor. Verifique se a API está rodando.');
    } finally {
        hideLoading();
    }
}

// Função para fazer requisição à API
async function generateArticle(data) {
    const response = await fetch('/api/generate-article', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
}

// Funções de UI
function showLoading() {
    loading.style.display = 'block';
    generateBtn.disabled = true;
    generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Gerando...';
    
    // Animação dos steps
    animateProgressSteps();
}

function hideLoading() {
    loading.style.display = 'none';
    generateBtn.disabled = false;
    generateBtn.innerHTML = '<i class="fas fa-magic"></i> Gerar Artigo';
}

function showResult(data) {
    // Extrair dados do artigo da resposta
    const article = data.article || {};
    const metadata = article.metadata || {};
    
    // Mostrar metadados
    articleMeta.innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            <div>
                <strong><i class="fas fa-tag"></i> Título:</strong><br>
                ${article.title || 'Sem título'}
            </div>
            <div>
                <strong><i class="fas fa-align-left"></i> Palavras:</strong><br>
                ${article.word_count || 0}
            </div>
            <div>
                <strong><i class="fas fa-clock"></i> Gerado em:</strong><br>
                ${metadata.generated_at ? new Date(metadata.generated_at).toLocaleString('pt-BR') : new Date().toLocaleString('pt-BR')}
            </div>
            <div>
                <strong><i class="fas fa-palette"></i> Estilo:</strong><br>
                ${metadata.topic || 'Informativo'}
            </div>
        </div>
    `;

    // Mostrar conteúdo
    articleContent.innerHTML = formatArticleContent(article.content || 'Conteúdo não disponível');
    
    resultCard.style.display = 'block';
    resultCard.scrollIntoView({ behavior: 'smooth' });
}

function hideResult() {
    resultCard.style.display = 'none';
}

function showError(message) {
    errorMessage.textContent = message;
    error.style.display = 'flex';
}

function hideError() {
    error.style.display = 'none';
}

function formatArticleContent(content) {
    // Converter quebras de linha em parágrafos
    const paragraphs = content.split('\n\n').filter(p => p.trim());
    
    return paragraphs.map(paragraph => {
        const trimmed = paragraph.trim();
        
        // Detectar títulos (linhas que começam com #)
        if (trimmed.startsWith('# ')) {
            return `<h1>${trimmed.substring(2)}</h1>`;
        } else if (trimmed.startsWith('## ')) {
            return `<h2>${trimmed.substring(3)}</h2>`;
        } else if (trimmed.startsWith('### ')) {
            return `<h3>${trimmed.substring(4)}</h3>`;
        } else {
            return `<p>${trimmed}</p>`;
        }
    }).join('');
}

function animateProgressSteps() {
    const steps = document.querySelectorAll('.step');
    let currentStep = 0;

    const interval = setInterval(() => {
        if (currentStep < steps.length) {
            // Remover active da step anterior
            if (currentStep > 0) {
                steps[currentStep - 1].classList.remove('active');
                steps[currentStep - 1].classList.add('completed');
            }
            
            // Adicionar active na step atual
            steps[currentStep].classList.add('active');
            currentStep++;
        } else {
            clearInterval(interval);
        }
    }, 2000);

    // Limpar interval quando loading for escondido
    setTimeout(() => clearInterval(interval), 10000);
}

// Função para copiar artigo
async function copyArticle() {
    if (!currentArticle || !currentArticle.article) {
        showError('Nenhum artigo disponível para copiar');
        return;
    }

    try {
        const article = currentArticle.article;
        const textToCopy = `# ${article.title}\n\n${article.content}`;
        
        await navigator.clipboard.writeText(textToCopy);
        
        // Feedback visual
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copiado!';
        copyBtn.style.backgroundColor = '#28a745';
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.backgroundColor = '';
        }, 2000);
        
    } catch (err) {
        console.error('Erro ao copiar:', err);
        showError('Erro ao copiar artigo para a área de transferência');
    }
}

// Função para download do artigo
function downloadArticle() {
    if (!currentArticle || !currentArticle.article) {
        showError('Nenhum artigo disponível para download');
        return;
    }

    try {
        const article = currentArticle.article;
        const content = `# ${article.title}\n\n${article.content}`;
        
        // Criar blob com o conteúdo
        const blob = new Blob([content], { type: 'text/markdown;charset=utf-8' });
        
        // Criar URL temporária
        const url = window.URL.createObjectURL(blob);
        
        // Criar elemento de download
        const a = document.createElement('a');
        a.href = url;
        a.download = sanitizeFilename(`${article.title || 'artigo'}.md`);
        
        // Trigger download
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        // Limpar URL temporária
        window.URL.revokeObjectURL(url);
        
        // Feedback visual
        const originalText = downloadBtn.innerHTML;
        downloadBtn.innerHTML = '<i class="fas fa-check"></i> Baixado!';
        downloadBtn.style.background = '#48bb78';
        
        setTimeout(() => {
            downloadBtn.innerHTML = originalText;
            downloadBtn.style.background = '';
        }, 2000);
        
    } catch (err) {
        console.error('Erro ao fazer download:', err);
        showError('Erro ao fazer download do artigo');
    }
}

// Função auxiliar para sanitizar nome do arquivo
function sanitizeFilename(filename) {
    return filename
        .toLowerCase()
        .replace(/[^a-z0-9\s-]/g, '')
        .replace(/\s+/g, '-')
        .replace(/-+/g, '-')
        .trim('-');
}

// Verificar status da API ao carregar a página
async function checkApiStatus() {
    try {
        const response = await fetch('/api/health');
        if (response.ok) {
            console.log('API está funcionando');
        }
    } catch (err) {
        console.warn('API não está respondendo:', err);
        showError('Servidor não está respondendo. Verifique se a API está rodando na porta 8001.');
    }
}

// Inicializar aplicação
document.addEventListener('DOMContentLoaded', () => {
    checkApiStatus();
    
    // Reset dos steps de progresso
    document.querySelectorAll('.step').forEach(step => {
        step.classList.remove('active', 'completed');
    });
});

// Adicionar validação em tempo real
document.getElementById('topic').addEventListener('input', function() {
    const value = this.value.trim();
    if (value.length < 3) {
        this.style.borderColor = '#e53e3e';
    } else {
        this.style.borderColor = '#48bb78';
    }
});

document.getElementById('minWords').addEventListener('input', function() {
    const value = parseInt(this.value);
    if (value < 100 || value > 2000) {
        this.style.borderColor = '#e53e3e';
    } else {
        this.style.borderColor = '#48bb78';
    }
});