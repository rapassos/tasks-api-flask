# 📋 Tasks API - Gerenciador de Tarefas

> API REST completa para gerenciamento de tarefas desenvolvida com Flask e SQLite. CRUD completo com validações, tratamento de erros e deploy em produção no Render.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**🌐 API em Produção:** [https://tasks-api-flask.onrender.com](https://tasks-api-flask.onrender.com)

---

## 🎯 Sobre o Projeto

API RESTful para gerenciamento de tarefas (To-Do List) com operações CRUD completas, validações de dados, tratamento de erros e persistência em banco de dados SQLite.

**Desenvolvida para demonstrar:**
- ✅ Criação de APIs REST com Flask
- ✅ Operações CRUD (Create, Read, Update, Delete)
- ✅ Integração com banco de dados
- ✅ Validação de dados e tratamento de erros
- ✅ Testes unitários automatizados
- ✅ Deploy em produção (Render)
- ✅ Boas práticas de desenvolvimento de APIs

---

## ✨ Funcionalidades

### Endpoints Disponíveis

| Método | Endpoint | Descrição | Status Code |
|--------|----------|-----------|-------------|
| GET | `/` | Informações da API | 200 |
| GET | `/health` | Health check | 200 |
| GET | `/tasks` | Lista todas as tarefas | 200 |
| GET | `/tasks/<id>` | Retorna uma tarefa específica | 200, 404 |
| POST | `/tasks` | Cria nova tarefa | 201, 400 |
| PUT | `/tasks/<id>` | Atualiza tarefa existente | 200, 400, 404 |
| DELETE | `/tasks/<id>` | Remove uma tarefa | 200, 404 |

### Validações Implementadas

- ✅ Campo `title` obrigatório
- ✅ Títulos vazios não são aceitos
- ✅ Verificação de existência antes de atualizar/deletar
- ✅ Tratamento de erros 400, 404, 500
- ✅ Respostas padronizadas em JSON
- ✅ Conexões de banco gerenciadas corretamente

---

## 🚀 Como Executar Localmente

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/rapassos/tasks-api-flask.git
cd tasks-api-flask

# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Execução

```bash
# Execute a API
python app.py

# A API estará disponível em:
# http://localhost:5000
```

### Testes

```bash
# Execute os testes unitários
python test_app.py

# Saída esperada: 6/6 testes passando
```

---

## 📖 Documentação da API

### 1. Informações da API

```http
GET /
```

**Resposta (200 OK):**
```json
{
  "message": "Tasks API - Gerenciador de Tarefas",
  "version": "1.0.1",
  "author": "Rafael Passos",
  "status": "running",
  "endpoints": {
    "GET /": "Informações da API",
    "GET /health": "Health check",
    "GET /tasks": "Lista todas as tarefas",
    ...
  }
}
```

### 2. Health Check

```http
GET /health
```

**Resposta (200 OK):**
```json
{
  "status": "healthy",
  "database": "connected",
  "tasks_count": 3
}
```

### 3. Listar Todas as Tarefas

```http
GET /tasks
```

**Resposta (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "tasks": [
    {
      "id": 1,
      "title": "Estudar Flask",
      "description": "Aprender a criar APIs REST",
      "completed": false,
      "created_at": "2025-02-13T10:30:00",
      "updated_at": "2025-02-13T10:30:00"
    },
    {
      "id": 2,
      "title": "Deploy no Render",
      "description": "Colocar API em produção",
      "completed": true,
      "created_at": "2025-02-13T11:00:00",
      "updated_at": "2025-02-13T12:00:00"
    }
  ]
}
```

### 4. Buscar Tarefa por ID

```http
GET /tasks/1
```

**Resposta (200 OK):**
```json
{
  "success": true,
  "task": {
    "id": 1,
    "title": "Estudar Flask",
    "description": "Aprender a criar APIs REST",
    "completed": false,
    "created_at": "2025-02-13T10:30:00",
    "updated_at": "2025-02-13T10:30:00"
  }
}
```

**Erro (404 Not Found):**
```json
{
  "success": false,
  "error": "Tarefa não encontrada"
}
```

### 5. Criar Nova Tarefa

```http
POST /tasks
Content-Type: application/json

{
  "title": "Minha nova tarefa",
  "description": "Descrição opcional"
}
```

**Resposta (201 Created):**
```json
{
  "success": true,
  "message": "Tarefa criada com sucesso",
  "task": {
    "id": 3,
    "title": "Minha nova tarefa",
    "description": "Descrição opcional",
    "completed": false,
    "created_at": "2025-02-13T13:00:00",
    "updated_at": "2025-02-13T13:00:00"
  }
}
```

**Erro (400 Bad Request):**
```json
{
  "success": false,
  "error": "Campo 'title' é obrigatório"
}
```

### 6. Atualizar Tarefa

```http
PUT /tasks/1
Content-Type: application/json

{
  "title": "Título atualizado",
  "completed": true
}
```

**Resposta (200 OK):**
```json
{
  "success": true,
  "message": "Tarefa atualizada com sucesso",
  "task": {
    "id": 1,
    "title": "Título atualizado",
    "description": "Descrição mantida",
    "completed": true,
    "created_at": "2025-02-13T10:30:00",
    "updated_at": "2025-02-13T13:15:00"
  }
}
```

### 7. Deletar Tarefa

```http
DELETE /tasks/1
```

**Resposta (200 OK):**
```json
{
  "success": true,
  "message": "Tarefa removida com sucesso"
}
```

---

## 🧪 Testando a API em Produção

### Com cURL

```bash
# URL da API em produção
API_URL="https://tasks-api-flask.onrender.com"

# 1. Informações da API
curl $API_URL/

# 2. Health check
curl $API_URL/health

# 3. Listar tarefas
curl $API_URL/tasks

# 4. Criar tarefa
curl -X POST $API_URL/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Minha tarefa","description":"Teste da API"}'

# 5. Buscar tarefa específica (substitua ID)
curl $API_URL/tasks/1

# 6. Atualizar tarefa
curl -X PUT $API_URL/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# 7. Deletar tarefa
curl -X DELETE $API_URL/tasks/1
```

### Com Postman/Insomnia

1. Importe a URL base: `https://tasks-api-flask.onrender.com`
2. Crie requests para cada endpoint
3. Teste operações CRUD

### Com JavaScript (Fetch API)

```javascript
const API_URL = 'https://tasks-api-flask.onrender.com';

// Listar tarefas
fetch(`${API_URL}/tasks`)
  .then(res => res.json())
  .then(data => console.log(data));

// Criar tarefa
fetch(`${API_URL}/tasks`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Nova tarefa',
    description: 'Descrição'
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

---

## 🗂️ Estrutura do Projeto

```
tasks-api-flask/
├── app.py              # Aplicação Flask principal
├── test_app.py         # Testes unitários (6 testes)
├── requirements.txt    # Dependências Python
├── railway.json        # Configuração Railway (tentativa inicial)
├── .gitignore         # Arquivos ignorados pelo Git
└── README.md          # Documentação
```

---

## 🗄️ Modelo de Dados

### Tabela `tasks`

| Campo | Tipo | Descrição | Constraints |
|-------|------|-----------|-------------|
| `id` | INTEGER | ID único | PRIMARY KEY, AUTOINCREMENT |
| `title` | TEXT | Título da tarefa | NOT NULL |
| `description` | TEXT | Descrição detalhada | - |
| `completed` | INTEGER | Status (0=pendente, 1=concluída) | DEFAULT 0 |
| `created_at` | TEXT | Data/hora de criação | DEFAULT CURRENT_TIMESTAMP |
| `updated_at` | TEXT | Data/hora da última atualização | DEFAULT CURRENT_TIMESTAMP |

---

## 🚢 Deploy - Lições Aprendidas

### Tentativa 1: Railway ❌

**Problema Encontrado:**
```
ModuleNotFoundError: No module named 'main'
```

**Tentativas de Correção:**
1. Ajuste do Procfile
2. Adição de runtime.txt
3. Criação de railway.json
4. Configuração de health check
5. Múltiplos ajustes de workers e timeout

**Resultado:** Após várias tentativas, Railway continuou apresentando problemas de inicialização.

**Lição Aprendida:** Railway pode ter problemas com configurações Python/Flask em free tier.

---

### Solução Final: Render ✅

**Por que Render funcionou:**
- ✅ Detecção automática de Python
- ✅ Build simples e confiável
- ✅ Free tier estável
- ✅ Logs claros e úteis
- ✅ Cold start aceitável (~30s)

**Configuração Render (simples):**
```
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

**Resultado:** Deploy bem-sucedido no primeiro try!

---

### Comparação de Plataformas

| Aspecto | Railway | Render | Azure |
|---------|---------|--------|-------|
| **Facilidade** | 🟡 Média | 🟢 Fácil | 🔴 Complexa |
| **Estabilidade** | 🟡 Variável | 🟢 Alta | 🟢 Alta |
| **Free Tier** | ✅ 5$/mês | ✅ 750h/mês | ⚠️ Trial |
| **Cold Start** | ⚡ Rápido | 🐢 ~30s | ⚡ Rápido |
| **Logs** | 🟢 Bons | 🟢 Excelentes | 🟢 Bons |
| **Python/Flask** | 🟡 Instável | 🟢 Perfeito | 🟢 Ótimo |
| **Recomendação** | Para node.js | **Para Python** | Para enterprise |

---

## 🛠️ Tecnologias Utilizadas

- **Flask 3.0** — Framework web Python
- **SQLite** — Banco de dados relacional leve
- **Flask-CORS** — Permite requisições de diferentes origens
- **Gunicorn** — Servidor WSGI para produção
- **Render** — Plataforma de deploy

---

## 📚 Conceitos Demonstrados

### Backend
- ✅ API RESTful com Flask
- ✅ Operações CRUD completas
- ✅ Validação de dados de entrada
- ✅ Tratamento de erros HTTP
- ✅ Respostas padronizadas em JSON
- ✅ Gerenciamento de conexões de banco

### Banco de Dados
- ✅ SQLite com Python
- ✅ Schema de tabelas
- ✅ Queries SQL (SELECT, INSERT, UPDATE, DELETE)
- ✅ Transações e commits
- ✅ Fechamento correto de conexões

### Testes
- ✅ Testes unitários com Flask test client
- ✅ Cobertura de todos endpoints
- ✅ Validação de erros (400, 404)
- ✅ Verificação de banco de dados
- ✅ 6 testes automatizados

### DevOps
- ✅ Deploy em produção
- ✅ Configuração de servidor WSGI
- ✅ Health check endpoint
- ✅ Versionamento com Git
- ✅ Troubleshooting de deploy

---

## 🧪 Testes Unitários

O projeto inclui suite completa de testes em `test_app.py`:

### Testes Implementados

1. **Teste de Importações** — Valida dependências
2. **Teste de Aplicação** — Cria instância Flask
3. **Teste de Banco de Dados** — Inicialização e tabelas
4. **Teste de Rotas** — Registros de endpoints
5. **Teste de Endpoints** — CRUD funcional completo
6. **Teste de Validações** — Erros 400 e 404

### Execução

```bash
python test_app.py
```

### Saída Esperada

```
======================================================================
TESTE UNITÁRIO - TASKS API
======================================================================

🧪 Teste 1: Importando módulos...
✓ Todas as dependências importadas com sucesso

🧪 Teste 2: Criando aplicação Flask...
✓ Aplicação criada
✓ Nome da aplicação: app

🧪 Teste 3: Testando banco de dados...
✓ Banco inicializado
✓ Tabelas encontradas: ['tasks']

🧪 Teste 4: Testando rotas...
✓ 7 rotas registradas

🧪 Teste 5: Testando endpoints...
  ✓ GET / retornou: Tasks API - Gerenciador de Tarefas
  ✓ GET /health: healthy
  ✓ GET /tasks retornou 0 tarefas
  ✓ POST /tasks criou tarefa ID: 1
  ✓ GET /tasks/1 retornou: Teste
  ✓ PUT /tasks/1 atualizou para completed=True
  ✓ DELETE /tasks/1 removeu a tarefa

🧪 Teste 6: Testando validações...
  ✓ Rejeitou POST sem title (400)
  ✓ Rejeitou POST com title vazio (400)
  ✓ Retornou 404 para tarefa inexistente
  ✓ Retornou 404 para DELETE inexistente

======================================================================
RESULTADO FINAL
======================================================================
✓ Passou: 6/6
✗ Falhou: 0/6

🎉 TODOS OS TESTES PASSARAM! API PRONTA PARA DEPLOY!
```

---

## 🔮 Próximas Evoluções (Roadmap)

### Curto Prazo
- [ ] **Autenticação JWT** — Login e proteção de rotas
- [ ] **Paginação** — Listar tarefas com limite e offset
- [ ] **Filtros** — Buscar por status (completed/pending)
- [ ] **Ordenação** — Ordenar por data, título, prioridade

### Médio Prazo
- [ ] **Swagger/OpenAPI** — Documentação interativa
- [ ] **PostgreSQL** — Migrar de SQLite para produção
- [ ] **Docker** — Containerização da aplicação
- [ ] **CI/CD** — GitHub Actions para testes automáticos

### Longo Prazo
- [ ] **Reescrita em Java** — Spring Boot + PostgreSQL
- [ ] **Frontend** — Interface web com React/Vue
- [ ] **Microserviços** — Separar em serviços independentes
- [ ] **Kubernetes** — Orquestração de containers

---

## 📝 Melhorias Implementadas

### Versão 1.0.0 → 1.0.1

**Correções:**
- ✅ Gerenciamento correto de conexões (`db.close()` em todas funções)
- ✅ Health check com teste de conexão ao banco
- ✅ Tratamento de erros aprimorado
- ✅ Suporte a variável de ambiente `PORT`
- ✅ Configuração otimizada para Render

**Adições:**
- ✅ Suite completa de testes unitários
- ✅ Documentação detalhada de deploy
- ✅ Lições aprendidas sobre plataformas
- ✅ Comparação Railway vs Render

---

## 👤 Autor

**Rafael Passos Guimarães**

Full-Stack Developer | Python • Java • JavaScript | 15+ anos em TI

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/rapassos)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rapassos)
[![GitLab](https://img.shields.io/badge/GitLab-FCA121?style=for-the-badge&logo=gitlab&logoColor=white)](https://gitlab.com/rapassos)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🔗 Links Úteis

- [Documentação Flask](https://flask.palletsprojects.com/)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [REST API Design](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)
- [Render Documentation](https://render.com/docs)
- [Gunicorn Documentation](https://docs.gunicorn.org/)

---

## 🎓 Aprendizados do Projeto

### Técnicos
1. **Gerenciamento de Conexões** — Sempre fechar conexões de banco
2. **Health Checks** — Essenciais para plataformas de deploy
3. **Testes Unitários** — Validam funcionamento antes do deploy
4. **Logs Detalhados** — Facilitam troubleshooting

### Deploy
1. **Railway** — Ótimo para Node.js, instável para Python
2. **Render** — Perfeito para Python, build confiável
3. **Configuração Simples** — Nem sempre é melhor (Railway detecta errado)
4. **Testes Locais** — Fundamentais antes de qualquer deploy

### Boas Práticas
1. **Versionamento Semântico** — 1.0.0 → 1.0.1 com changelog
2. **Documentação Completa** — README como guia único
3. **Endpoints Documentados** — Facilita integração
4. **Tratamento de Erros** — HTTP status codes corretos

---

> 💡 **Nota:** Esta API foi desenvolvida como projeto portfolio demonstrando competências em desenvolvimento backend Python, deploy em produção e boas práticas de engenharia de software. Para uso corporativo, considere migrar para PostgreSQL, adicionar autenticação e implementar rate limiting.

---

> 🚀 **Status do Projeto:** Concluído e em produção no Render. Próxima evolução planejada: Reescrita em Java com Spring Boot.
