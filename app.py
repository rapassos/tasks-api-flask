from flask import Flask, request, jsonify
from flask_cors import CORS
from database import init_db, get_db
from datetime import datetime
import sqlite3

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

# Inicializa o banco de dados
init_db()

# ==================== ROTAS ====================

@app.route('/', methods=['GET'])
def home():
    """Rota principal - informações da API"""
    return jsonify({
        'message': 'Tasks API - Gerenciador de Tarefas',
        'version': '1.0.0',
        'author': 'Rafael Passos',
        'endpoints': {
            'GET /tasks': 'Lista todas as tarefas',
            'GET /tasks/<id>': 'Retorna uma tarefa específica',
            'POST /tasks': 'Cria nova tarefa',
            'PUT /tasks/<id>': 'Atualiza tarefa',
            'DELETE /tasks/<id>': 'Remove tarefa'
        }
    })

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Lista todas as tarefas"""
    try:
        db = get_db()
        cursor = db.execute('SELECT * FROM tasks ORDER BY created_at DESC')
        tasks = cursor.fetchall()
        
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
        if not data or 'title' not in data:
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
            return jsonify({
                'success': False,
                'error': 'Tarefa não encontrada'
            }), 404
        
        # Remove
        db.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tarefa removida com sucesso'
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==================== EXECUÇÃO ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
