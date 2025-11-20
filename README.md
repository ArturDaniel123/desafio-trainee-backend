# desafio-trainee-backend
📌 README.md — PROJETO DE API DE RESTAURANTE
🍽️ API de Pedidos de Restaurante (Django REST Framework)

Esta é uma API completa para gerenciamento de cardápio, pedidos, itens do pedido, usuários e métodos de pagamento, construída com:

1. Django

2. Django REST Framework

3. JWT Authentication

4. drf-spectacular (Swagger)

1. Funcionalidades
- Autenticação
-Registro de usuários
- Login com JWT
- Permissões para usuários comuns e administradores

2. Cardápio
- Listar pratos (público)
- Buscar pratos por nome
- Criar/editar/remover pratos (admin)

3. Pedidos
- Criar pedido (usuário logado)
- Listar apenas pedidos do usuário
- Adicionar itens ao pedido
- Finalizar pedido (controle de estoque)
- Ver total de itens e valor

4. Métodos de Pagamento
- Listar (usuários logados)
- Criar/editar/deletar (admin)

5. Faturamento (Admin)
- Consultar faturamento entre datas

6. Instalação
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver

7. Rotas
- cardapio/
  (GET: Lista de pratos)
  (POST: Cria prato (admin)
- pedido/
    (POST: Cria pedido)
- pedido/id/adicionar_item/
- pedido/id/finalizar/
- metodos-pagamento/
- login/
- api/docs/
