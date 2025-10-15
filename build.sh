#!/usr/bin/env bash
set -e

# скачиваем uv
curl -LsSf https://astral.sh/uv/install.sh | sh
# активируем окружение uv на билд-окружении Render
source "$HOME/.local/bin/env"

# ставим зависимости и готовим приложение
make install
make collectstatic
make migrate
