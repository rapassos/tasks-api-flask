"""
Testes unitários para Tasks API
Execução: python app.py
"""

import sys
import json

def test_imports():
    """Teste 1: Importações"""
    print("🧪 Teste 1: Importando módulos...")
    try:
        from flask import Flask
        from flask_cors import CORS
        import sqlite3
        print("✓ Todas as dependências importadas com sucesso")
        return True
    except ImportError as e:
        print(f"✗ Erro ao importar: {e}")
        return False

def test_app_creation():
    """Teste 2: Criação da aplicação"""
    print("\n🧪 Teste 2: Criando aplicação Flask...")
    try:
        import app as app_module
        app = app_module.app
        print(f"✓ Aplicação criada: {app}")
        print(f"✓ Nome da aplicação: {app.name}")
        return True
    except Exception as e:
        print(f"✗ Erro ao criar aplicação: {e}")
        return False

def test_database():
    """Teste 3: Banco de dados"""
    print("\n🧪 Teste 3: Testando banco de dados...")
    try:
        import app as app_module
        
        # Testa inicialização
        result = app_module.init_db()
        if not result:
            print("✗ Falha ao inicializar banco")
            return False
        print("✓ Banco inicializado")
        
        # Testa conexão
        db = app_module.get_db()
        cursor = db.execute('SELECT name FROM sqlite_master WHERE type="table"')
        tables = cursor.fetchall()
        db.close()
        
        if len(tables) > 0:
            print(f"✓ Tabelas encontradas: {[t[0] for t in tables]}")
            return True
        else:
            print("✗ Nenhuma tabela criada")
            return False
    except Exception as e:
        print(f"✗ Erro no banco: {e}")
        return False

def test_routes():
    """Teste 4: Rotas da API"""
    print("\n🧪 Teste 4: Testando rotas...")
    try:
        import app as app_module
        app = app_module.app
        
        routes = []
        for rule in app.url_map.iter_rules():
            routes.append(f"{','.join(rule.methods)} {rule.rule}")
        
        print(f"✓ {len(routes)} rotas registradas:")
        for route in routes:
            if 'GET' in route or 'POST' in route or 'PUT' in route or 'DELETE' in route:
                print(f"  - {route}")
        
        return True
    except Exception as e:
        print(f"✗ Erro ao listar rotas: {e}")
        return False

def test_endpoints():
    """Teste 5: Endpoints funcionais"""
    print("\n🧪 Teste 5: Testando endpoints...")
    try:
        import app as app_module
        app = app_module.app
        client = app.test_client()
        
        # Teste GET /
        print("  Testando GET /...")
        response = client.get('/')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        print(f"  ✓ GET / retornou: {data['message']}")
        
        # Teste GET /health
        print("  Testando GET /health...")
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        print(f"  ✓ GET /health: {data['status']}")
        
        # Teste GET /tasks (lista vazia)
        print("  Testando GET /tasks...")
        response = client.get('/tasks')
        assert response.status_code == 200
        data = json.loads(response.data)
        print(f"  ✓ GET /tasks retornou {data['count']} tarefas")
        
        # Teste POST /tasks
        print("  Testando POST /tasks...")
        response = client.post('/tasks',
            data=json.dumps({'title': 'Teste', 'description': 'Descrição teste'}),
            content_type='application/json'
        )
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True
        task_id = data['task']['id']
        print(f"  ✓ POST /tasks criou tarefa ID: {task_id}")
        
        # Teste GET /tasks/<id>
        print(f"  Testando GET /tasks/{task_id}...")
        response = client.get(f'/tasks/{task_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['task']['title'] == 'Teste'
        print(f"  ✓ GET /tasks/{task_id} retornou: {data['task']['title']}")
        
        # Teste PUT /tasks/<id>
        print(f"  Testando PUT /tasks/{task_id}...")
        response = client.put(f'/tasks/{task_id}',
            data=json.dumps({'completed': True}),
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['task']['completed'] == True
        print(f"  ✓ PUT /tasks/{task_id} atualizou para completed=True")
        
        # Teste DELETE /tasks/<id>
        print(f"  Testando DELETE /tasks/{task_id}...")
        response = client.delete(f'/tasks/{task_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] == True
        print(f"  ✓ DELETE /tasks/{task_id} removeu a tarefa")
        
        print("\n✓ Todos os endpoints funcionando corretamente!")
        return True
        
    except AssertionError as e:
        print(f"✗ Falha em assertion: {e}")
        return False
    except Exception as e:
        print(f"✗ Erro ao testar endpoints: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_validations():
    """Teste 6: Validações"""
    print("\n🧪 Teste 6: Testando validações...")
    try:
        import app as app_module
        app = app_module.app
        client = app.test_client()
        
        # POST sem title
        print("  Testando POST sem title...")
        response = client.post('/tasks',
            data=json.dumps({'description': 'Sem título'}),
            content_type='application/json'
        )
        assert response.status_code == 400
        print("  ✓ Rejeitou POST sem title (400)")
        
        # POST com title vazio
        print("  Testando POST com title vazio...")
        response = client.post('/tasks',
            data=json.dumps({'title': '   '}),
            content_type='application/json'
        )
        assert response.status_code == 400
        print("  ✓ Rejeitou POST com title vazio (400)")
        
        # GET de tarefa inexistente
        print("  Testando GET de tarefa inexistente...")
        response = client.get('/tasks/99999')
        assert response.status_code == 404
        print("  ✓ Retornou 404 para tarefa inexistente")
        
        # DELETE de tarefa inexistente
        print("  Testando DELETE de tarefa inexistente...")
        response = client.delete('/tasks/99999')
        assert response.status_code == 404
        print("  ✓ Retornou 404 para DELETE inexistente")
        
        print("\n✓ Todas as validações funcionando!")
        return True
        
    except AssertionError as e:
        print(f"✗ Falha em validation: {e}")
        return False
    except Exception as e:
        print(f"✗ Erro ao testar validações: {e}")
        return False

def run_all_tests():
    """Executa todos os testes"""
    print("="*70)
    print("TESTE UNITÁRIO - TASKS API")
    print("="*70)
    
    tests = [
        test_imports,
        test_app_creation,
        test_database,
        test_routes,
        test_endpoints,
        test_validations
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Exceção no teste: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print("RESULTADO FINAL")
    print("="*70)
    print(f"✓ Passou: {passed}/{len(tests)}")
    print(f"✗ Falhou: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM! API PRONTA PARA DEPLOY!")
        return True
    else:
        print("\n⚠️  ALGUNS TESTES FALHARAM. CORRIJA ANTES DO DEPLOY.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
