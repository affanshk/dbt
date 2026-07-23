This folder contains helpers for generating models from config/sources_config.yml

Usage:
  python3 scripts/generate_models.py --config config/sources_config.yml --out models/silver --gold-out models/gold

The generator will create a staging__{{source}}__{{table}}.sql file for each declared table under models/silver,
and a placeholder gold model under models/gold/marts/ for example.
