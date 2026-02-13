import sqlite3
from datetime import datetime

DATABASE = 'tasks.db'

def get_db():
    """Retorna conexão com o banco de dados"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Inicializa o banco de dados"""
    db = get_db()
    
    # Cria tabela se não existir
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
    print("✓ Banco de dados inicializado")

def seed_db():
    """Popula banco com dados de exemplo (opcional)"""
    db = get_db()
    
    # Verifica se já tem dados
    cursor = db.execute('SELECT COUNT(*) FROM tasks')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insere dados de exemplo
        tasks = [
            ('Estudar Flask', 'Aprender a criar APIs REST com Flask'),
            ('Criar projeto portfolio', 'Desenvolver API de tarefas'),
            ('Deploy no Railway', 'Fazer deploy da API em produção'),
        ]
        
        for title, description in tasks:
            db.execute(
                'INSERT INTO tasks (title, description) VALUES (?, ?)',
                (title, description)
            )
        
        db.commit()
        print(f"✓ {len(tasks)} tarefas de exemplo criadas")
    else:
        print(f"✓ Banco já contém {count} tarefas")

if __name__ == '__main__':
    init_db()
    seed_db()
