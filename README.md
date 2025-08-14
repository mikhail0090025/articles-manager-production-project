1. Copy .env.example to .env
2. Replace data in .env by your real data

curl -X POST http://localhost:8001/search -H 'Content-Type: application/json' -d '{\"query\": \"Что такое машинное обучение?\", \"top_k\": 3}'