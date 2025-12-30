#!/bin/bash
echo "Testing Groq (9080)..."
curl -s -X POST http://127.0.0.1:9080/query -H "Content-Type: application/json" -d '{"query": "ping"}' || echo "Groq Failed"
echo ""

echo "Testing OpenAI (9081)..."
curl -s -X POST http://127.0.0.1:9081/query -H "Content-Type: application/json" -d '{"query": "ping"}' || echo "OpenAI Failed"
echo ""

echo "Testing Claude (9082)..."
curl -s -X POST http://127.0.0.1:9082/query -H "Content-Type: application/json" -d '{"query": "ping"}' || echo "Claude Failed"
echo ""

echo "Testing Gemini (9083)..."
curl -s -X POST http://127.0.0.1:9083/query -H "Content-Type: application/json" -d '{"query": "ping"}' || echo "Gemini Failed"
echo ""
