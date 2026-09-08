#!/bin/sh
# Pontos quentes via git nos ultimos 6 meses.
SINCE="6 months ago"
OUT=discovery/data
mkdir -p "$OUT"
{
echo "# Historico git (desde $SINCE)"
echo
echo "## Top 20 arquivos mais alterados"
echo
echo '| commits | arquivo |'
echo '|---:|---|'
git log --since="$SINCE" --pretty=format: --name-only | grep -v '^$' | sort | uniq -c | sort -rn | head -20 | sed 's/^ *\([0-9]*\) \(.*\)/| \1 | `\2` |/'
echo
echo "## Commits por modulo de topo"
echo
echo '| commits(arquivos-tocados) | modulo |'
echo '|---:|---|'
git log --since="$SINCE" --pretty=format: --name-only | grep -v '^$' | cut -d/ -f1-2 | sort | uniq -c | sort -rn | head -25 | sed 's/^ *\([0-9]*\) \(.*\)/| \1 | `\2` |/'
echo
echo "## Convencao de mensagem de commit (prefixo, ultimos 6 meses)"
echo
echo '| ocorrencias | prefixo |'
echo '|---:|---|'
git log --since="$SINCE" --pretty=format:%s | sed -n 's/^\([a-z]*\)(\?\([A-Za-z0-9-]*\))\?:.*/\1/p' | sort | uniq -c | sort -rn | sed 's/^ *\([0-9]*\) \(.*\)/| \1 | `\2` |/'
echo
echo "## Referencia a ticket (REP-nnn) nas mensagens"
TOT=$(git log --since="$SINCE" --pretty=format:%s | wc -l)
WITH=$(git log --since="$SINCE" --pretty=format:%s | grep -cE 'REP-[0-9]+')
echo
echo "- total de commits: $TOT"
echo "- com REP-nnn: $WITH"
echo
echo "## Total de commits e autores"
git shortlog -sn --since="$SINCE" --all | sed 's/^/    /'
} > "$OUT/git-hotspots.md"
wc -l "$OUT/git-hotspots.md"
