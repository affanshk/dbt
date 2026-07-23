#!/usr/bin/env python3
"""Generator: create model files from config/sources_config.yml
"""
import os
import argparse
import yaml

TEMPLATE_SILVER = '''-- GENERATED: staging__{source}__{table}
-- Cleaning-only model
with raw as (
  select * from {{{{ source('{source}', '{table}') }}}}
)

select *
from raw
where 1=1
'''

TEMPLATE_GOLD = '''-- GENERATED: gold mart for {table}
select * from {{{{ ref('staging__{source}__{table}') }}}}
'''


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config/sources_config.yml')
    parser.add_argument('--out', default='models/silver')
    parser.add_argument('--gold-out', default='models/gold/marts')
    args = parser.parse_args()

    with open(args.config) as fh:
        cfg = yaml.safe_load(fh)

    sources = cfg.get('sources', [])
    ensure_dir(args.out)
    ensure_dir(args.gold_out)

    for src in sources:
        sname = src['name']
        for tbl in src.get('tables', []):
            tname = tbl['name']
            fname = f'staging__{sname}__{tname}.sql'
            fpath = os.path.join(args.out, fname)
            if not os.path.exists(fpath):
                with open(fpath, 'w', encoding='utf-8') as fh:
                    fh.write(TEMPLATE_SILVER.format(source=sname, table=tname))
            # gold placeholder
            gname = f'business__{tname}.sql'
            gpath = os.path.join(args.gold_out, gname)
            if not os.path.exists(gpath):
                with open(gpath, 'w', encoding='utf-8') as fh:
                    fh.write(TEMPLATE_GOLD.format(source=sname, table=tname))

    print('Generated models for', len(sources), 'sources')

if __name__ == '__main__':
    main()
