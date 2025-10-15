import sqlite3, time

class QueryCache:
    def __init__(self):
        self.store={}

    def get(self,k): return self.store.get(k)
    def set(self,k,v): self.store[k]=v

class QueryEngine:
    def __init__(self, db_path, schema_discovery, document_processor):
        self.db_path = db_path
        self.schema_discovery = schema_discovery
        self.doc_processor = document_processor
        self.cache = QueryCache()

    def classify_query(self, q):
        ql = q.lower()
        if any(w in ql for w in ['how many','count','average','salary','employees','top']):
            return 'sql'
        if any(w in ql for w in ['resume','document','find in documents','who has']):
            return 'document'
        return 'hybrid'

    def process_query(self, q):
        start = time.time()
        cached = self.cache.get(q)
        if cached:
            return {'query': q, 'from_cache': True, 'result': cached, 'time_ms': 0}
        qtype = self.classify_query(q)
        schema = self.schema_discovery.analyze_database()
        res = {}
        try:
            if qtype=='sql':
                res = self._handle_sql(q, schema)
            elif qtype=='document':
                res = {'documents': self.doc_processor.search(q)}
            else:
                res = {'documents': self.doc_processor.search(q), 'structured': self._handle_sql(q, schema)}
        except Exception as e:
            res = {'error': str(e)}
        elapsed = int((time.time()-start)*1000)
        self.cache.set(q,res)
        return {'query': q, 'query_type': qtype, 'result': res, 'time_ms': elapsed}

    def _handle_sql(self, q, schema):
        ql = q.lower()
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        if 'how many' in ql or 'count' in ql:
            table = self._find_table_like(['employee','staff','person'], schema)
            if table:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                r = cur.fetchone()[0]
                conn.close()
                return {'count': r, 'table': table}
        if 'average' in ql:
            table = self._find_table_like(['employee','staff','person'], schema)
            if table:
                cols = [c['name'] for c in schema[table]['columns']]
                salary_col = next((c for c in cols if 'salary' in c or 'pay' in c), None)
                dept_col = next((c for c in cols if 'dept' in c), None)
                if salary_col and dept_col:
                    cur.execute(f"SELECT {dept_col}, AVG({salary_col}) FROM {table} GROUP BY {dept_col} LIMIT 50")
                    rows = cur.fetchall()
                    conn.close()
                    return {'aggregation': rows}
        first = list(schema.keys())[0]
        cur.execute(f"SELECT * FROM {first} LIMIT 10")
        rows = cur.fetchall()
        conn.close()
        return {'sample_rows_from': first, 'rows': rows}

    def _find_table_like(self, candidates, schema):
        lower = {t.lower(): t for t in schema.keys()}
        for c in candidates:
            for t in lower:
                if c in t:
                    return lower[t]
        return list(schema.keys())[0]
