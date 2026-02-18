"""
Tasks API - Gerenciador de Tarefas REST
Autor: Rafael Passos
Versão: 1.0.1
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

# ==================== CONFIGURAÇÃO ====================

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
DATABASE = os.environ.get('DATABASE_PATH', 'tasks.db')

# ==================== DATABASE ====================

def get_db():
    """Retorna conexão com banco de dados"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Inicializa o banco de dados"""
    try:
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
        print("✓ Database initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False
    finally:
        db.close()

# Inicializa o banco na importação do módulo
init_db()

# ==================== ROTAS ====================

@app.route('/', methods=['GET'])
def home():
    """Rota principal - informações da API"""
    return jsonify({
        'message': 'Tasks API - Gerenciador de Tarefas',
        'version': '1.0.1',
        'author': 'Rafael Passos',
        'status': 'running',
        'endpoints': {
            'GET /': 'Informações da API',
            'GET /health': 'Health check',
            'GET /tasks': 'Lista todas as tarefas',
            'GET /tasks/<id>': 'Retorna uma tarefa específica',
            'POST /tasks': 'Cria nova tarefa',
            'PUT /tasks/<id>': 'Atualiza tarefa',
            'DELETE /tasks/<id>': 'Remove tarefa'
        }
    }), 200

@app.route('/health', methods=['GET'])
def health():
    """Health check para plataformas de deploy"""
    try:
        # Testa conexão com banco
        db = get_db()
        cursor = db.execute('SELECT COUNT(*) FROM tasks')
        count = cursor.fetchone()[0]
        db.close()
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'tasks_count': count
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Lista todas as tarefas"""
    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        tasks = cursor.fetchall()
        db.close()
        
        tasks_list = []
        for task in tasks:
            tasks_list.append({
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'completed': bool(task[3]),
                'created_at': task[4],
                'updated_at': task[5]
            })
        
        return jsonify({
            'success': True,
            'count': len(tasks_list),
            'tasks': tasks_list
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Retorna uma tarefa específica"""
    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        db.close()
        
        if task is None:
            return jsonify({
                'success': False,
                'error': 'Tarefa não encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'task': {
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'completed': bool(task[3]),
                'created_at': task[4],
                'updated_at': task[5]
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/tasks', methods=['POST'])
def create_task():
    """Cria uma nova tarefa"""
    try:
        data = request.get_json()
        
        # Validações
        if not data:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado fornecido'
            }), 400
            
        if 'title' not in data:
            return jsonify({
                'success': False,
                'error': 'Campo "title" é obrigatório'
            }), 400
        
        title = data['title'].strip()
        description = data.get('description', '').strip()
        
        if not title:
            return jsonify({
                'success': False,
                'error': 'Título não pode ser vazio'
            }), 400
        
        # Insere no banco
        db = get_db()
        cursor = db.execute(
            'INSERT INTO tasks (title, description) VALUES (?, ?)',
            (title, description)
        )
        db.commit()
        task_id = cursor.lastrowid
        
        # Busca a tarefa criada
        cursor = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        db.close()
        
        return jsonify({
            'success': True,
            'message': 'Tarefa criada com sucesso',
            'task': {
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'completed': bool(task[3]),
                'created_at': task[4],
                'updated_at': task[5]
            }
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Atualiza uma tarefa"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'Nenhum dado fornecido'
            }), 400
        
        db = get_db()
        
        # Verifica se tarefa existe
        cursor = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        if cursor.fetchone() is None:
            db.close()
            return jsonify({
                'success': False,
                'error': 'Tarefa não encontrada'
            }), 404
        
        # Campos que podem ser atualizados
        title = data.get('title')
        description = data.get('description')
        completed = data.get('completed')
        
        # Monta query dinamicamente
        updates = []
        params = []
        
        if title is not None:
            updates.append('title = ?')
            params.append(title.strip())
        
        if description is not None:
            updates.append('description = ?')
            params.append(description.strip())
        
        if completed is not None:
            updates.append('completed = ?')
            params.append(1 if completed else 0)
        
        if not updates:
            db.close()
            return jsonify({
                'success': False,
                'error': 'Nenhum campo válido para atualizar'
            }), 400
        
        # Adiciona timestamp
        updates.append('updated_at = ?')
        params.append(datetime.now().isoformat())
        
        # Adiciona ID no final dos params
        params.append(task_id)
        
        # Executa update
        query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
        db.execute(query, params)
        db.commit()
        
        # Retorna tarefa atualizada
        cursor = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        db.close()
        
        return jsonify({
            'success': True,
            'message': 'Tarefa atualizada com sucesso',
            'task': {
                'id': task[0],
                'title': task[1],
                'description': task[2],
                'completed': bool(task[3]),
                'created_at': task[4],
                'updated_at': task[5]
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Remove uma tarefa"""
    try:
        db = get_db()
        
        # Verifica se tarefa existe
        cursor = db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        if cursor.fetchone() is None:
            db.close()
            return jsonify({
                'success': False,
                'error': 'Tarefa não encontrada'
            }), 404
        
        # Remove
        db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        db.commit()
        db.close()
        
        return jsonify({
            'success': True,
            'message': 'Tarefa removida com sucesso'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== EXECUÇÃO LOCAL ====================

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
