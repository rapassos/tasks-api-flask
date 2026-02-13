# 📋 Tasks API - Gerenciador de Tarefas

> API REST completa para gerenciamento de tarefas desenvolvida com Flask e SQLite. CRUD completo com validações, tratamento de erros e documentação.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**🌐 Demo:** [https://seu-deploy.railway.app](https://seu-deploy.railway.app) *(adicionar após deploy)*

---

## 🎯 Sobre o Projeto

API RESTful para gerenciamento de tarefas (To-Do List) com operações CRUD completas, validações de dados, tratamento de erros e persistência em banco de dados SQLite.

**Desenvolvida para demonstrar:**
- ✅ Criação de APIs REST com Flask
- ✅ Operações CRUD (Create, Read, Update, Delete)
- ✅ Integração com banco de dados
- ✅ Validação de dados e tratamento de erros
- ✅ Boas práticas de desenvolvimento de APIs

---

## ✨ Funcionalidades

### Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações da API |
| GET | `/tasks` | Lista todas as tarefas |
| GET | `/tasks/<id>` | Retorna uma tarefa específica |
| POST | `/tasks` | Cria nova tarefa |
| PUT | `/tasks/<id>` | Atualiza tarefa existente |
| DELETE | `/tasks/<id>` | Remove uma tarefa |

### Validações Implementadas

- ✅ Campo `title` obrigatório
- ✅ Títulos vazios não são aceitos
- ✅ Verificação de existência antes de atualizar/deletar
- ✅ Tratamento de erros 400, 404, 500
- ✅ Respostas padronizadas em JSON

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

# Inicialize o banco de dados (opcional - dados de exemplo)
python database.py
```

### Execução

```bash
# Execute a API
python app.py

# A API estará disponível em:
# http://localhost:5000
```

---

## 📖 Documentação da API

### 1. Listar Todas as Tarefas

```http
GET /tasks
```

**Resposta (200 OK):**
```json
{
  "success": true,
  "count": 3,
  "tasks": [
    {
      "id": 1,
      "title": "Estudar Flask",
      "description": "Aprender a criar APIs REST",
      "completed": false,
      "created_at": "2025-02-13T10:30:00",
      "updated_at": "2025-02-13T10:30:00"
    }
  ]
}
```

### 2. Buscar Tarefa por ID

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

### 3. Criar Nova Tarefa

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
    "id": 4,
    "title": "Minha nova tarefa",
    "description": "Descrição opcional",
    "completed": false,
    "created_at": "2025-02-13T11:00:00",
    "updated_at": "2025-02-13T11:00:00"
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

### 4. Atualizar Tarefa

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
    "updated_at": "2025-02-13T11:15:00"
  }
}
```

### 5. Deletar Tarefa

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

## 🧪 Testando a API

### Com cURL

```bash
# Listar tarefas
curl http://localhost:5000/tasks

# Criar tarefa
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Nova tarefa","description":"Teste"}'

# Atualizar tarefa
curl -X PUT http://localhost:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# Deletar tarefa
curl -X DELETE http://localhost:5000/tasks/1
```

### Com Postman/Insomnia

1. Importe a coleção de requests
2. Configure a base URL: `http://localhost:5000`
3. Teste cada endpoint

---

## 🗂️ Estrutura do Projeto

```
tasks-api-flask/
├── app.py              # Aplicação Flask principal
├── database.py         # Configuração e inicialização do banco
├── requirements.txt    # Dependências Python
├── Procfile           # Configuração para deploy (Railway/Heroku)
├── .gitignore         # Arquivos ignorados pelo Git
└── README.md          # Documentação
```

---

## 🗄️ Modelo de Dados

### Tabela `tasks`

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | INTEGER | ID único (auto-increment) |
| `title` | TEXT | Título da tarefa (obrigatório) |
| `description` | TEXT | Descrição detalhada (opcional) |
| `completed` | INTEGER | Status (0=pendente, 1=concluída) |
| `created_at` | TEXT | Data/hora de criação (ISO 8601) |
| `updated_at` | TEXT | Data/hora da última atualização |

---

## 🚢 Deploy

### Railway (Recomendado - Grátis)

1. Crie conta no [Railway](https://railway.app)
2. Conecte seu repositório GitHub
3. Railway detecta automaticamente o `Procfile`
4. Deploy automático em cada push

### Variáveis de Ambiente (se necessário)

```env
FLASK_ENV=production
```

---

## 🛠️ Tecnologias Utilizadas

- **Flask 3.0** — Framework web Python
- **SQLite** — Banco de dados relacional leve
- **Flask-CORS** — Permite requisições de diferentes origens
- **Gunicorn** — Servidor WSGI para produção

---

## 📚 Conceitos Demonstrados

### Backend
- ✅ API RESTful com Flask
- ✅ Operações CRUD completas
- ✅ Validação de dados de entrada
- ✅ Tratamento de erros HTTP
- ✅ Respostas padronizadas em JSON

### Banco de Dados
- ✅ SQLite com Python
- ✅ Schema de tabelas
- ✅ Queries SQL (SELECT, INSERT, UPDATE, DELETE)
- ✅ Transações e commits

### Boas Práticas
- ✅ Separação de responsabilidades (app.py vs database.py)
- ✅ Códigos de status HTTP corretos
- ✅ Documentação clara de endpoints
- ✅ Versionamento com Git

---

## 🔮 Próximas Evoluções

- [ ] **Autenticação JWT** — Login e proteção de rotas
- [ ] **Paginação** — Listar tarefas com limite e offset
- [ ] **Filtros** — Buscar por status (completed/pending)
- [ ] **Ordenação** — Ordernar por data, título, etc.
- [ ] **Swagger/OpenAPI** — Documentação interativa
- [ ] **Testes unitários** — Pytest para validação
- [ ] **PostgreSQL** — Migrar de SQLite para produção
- [ ] **Docker** — Containerização da aplicação

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

---

> 💡 **Nota:** Esta API foi desenvolvida para demonstrar competências em desenvolvimento backend com Python. Para uso em produção, considere adicionar autenticação, rate limiting e migrar para um banco de dados mais robusto como PostgreSQL.
