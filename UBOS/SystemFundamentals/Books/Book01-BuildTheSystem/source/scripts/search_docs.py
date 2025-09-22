#!/usr/bin/env python3
import json, argparse, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parents[1]
index_path = root/'docs/meta/search_index.json'
man_path = root/'docs/meta/manifest.json'

if not index_path.exists():
    print('search_index.json not found. Build it first.', file=sys.stderr)
    sys.exit(2)

index = json.loads(index_path.read_text())
postings = index['postings']
docs = {d['id']: d for d in index['docs']}

word_re = re.compile(r"[a-z0-9']+")

def tokenize(q: str):
    return [w for w in word_re.findall(q.lower()) if w]

def ngrams(tokens, n):
    return [' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def score_query(query: str, top_k: int = 10):
    tokens = tokenize(query)
    terms = set(tokens)
    terms.update(ngrams(tokens, 2))
    terms.update(ngrams(tokens, 3))
    # simple tf-like scoring by term matches; prefer longer ngrams by weight
    weights = {}
    for t in terms:
        weights[t] = 3 if len(t.split())==3 else (2 if len(t.split())==2 else 1)
    scores = {}
    for t, w in weights.items():
        for did in postings.get(t, []):
            scores[did] = scores.get(did, 0) + w
    ranked = sorted(scores.items(), key=lambda x: (-x[1], x[0]))[:top_k]
    return [(docs[did]['title'], docs[did]['path'], s) for did, s in ranked]

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='Search BuildTheSystem docs')
    ap.add_argument('query', nargs='+', help='query terms')
    ap.add_argument('--k', type=int, default=10, help='top K results')
    args = ap.parse_args()
    query = ' '.join(args.query)
    results = score_query(query, args.k)
    for title, path, score in results:
        print(f'{score:>3}  {title}  ->  {path}')
