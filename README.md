# recommender-api
Este projeto é uma API RESTful construída com Flask que utiliza dados de compras de usuários para recomendar produtos. Ele simula um sistema de recomendação simples, identificando padrões nas compras realizadas e sugerindo itens que outros usuários adquiriram. 
Para testar  a plicação  basta clonar o  repositório e consultar  a recomendação  via curl:
Exemplo:
curl -X POST http://127.0.0.1:5000/recommend \
-H "Content-Type: application/json" \
-d '{"user_id": 1}'
Resultado:
{
    "purchases": [
        [101, "Laptop"],
        [102, "Mouse"]
    ],
    "recommendations": [
        [103, "Headphones"],
        [104, "Smartphone"]
    ]
}
