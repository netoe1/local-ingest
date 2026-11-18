#!/usr/bin/env bash
set -e

echo "🧹 Iniciando limpeza do repositório para o local-ingest..."

# 1. Camada Web, Frontend e Infraestrutura
rm -rf src/server \
       src/static \
       .docker \
       Dockerfile \
       .dockerignore \
       compose.yml \
       eslint.config.cjs \
       .env.example

# 2. Automação e Metadados do Repositório Original
rm -rf .github \
       release-please-config.json \
       .release-please-manifest.json \
       renovate.json \
       CHANGELOG.md \
       CODE_OF_CONDUCT.md \
       CONTRIBUTING.md \
       SECURITY.md

# 3. Módulos de Clonagem Remota e Git
# Remote Git modules were removed when the project became fully local.

# 4. Testes Obsoletos (Servidor e Git Remoto)
rm -rf tests/server \
       tests/test_clone.py \
       tests/test_git_utils.py \
       tests/test_summary.py \
       tests/query_parser/test_git_host_agnostic.py

echo "✅ Arquivos removidos com sucesso!"
echo "✅ Limpeza concluída."
