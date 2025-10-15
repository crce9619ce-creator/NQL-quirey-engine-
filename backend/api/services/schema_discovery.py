import sqlite3, os, difflib

class SchemaDiscovery:
    def __init__(self, db_path):
        self.db_path = db_path

    def analyze_database(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cur = conn.cursor()
            cur.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
            tables = [r[0] for r in cur.fetchall()]
            schema = {}
            for t in tables:
                cur.execute(f"PRAGMA table_info('{t}')")
                cols = [{'cid':c[0],'name':c[1],'type':c[2]} for c in cur.fetchall()]
                cur.execute(f"SELECT * FROM {t} LIMIT 3")
                rows = cur.fetchall()
                schema[t] = {'columns': cols, 'sample': rows}
            conn.close()
            return schema
        except Exception as e:
            return {'error': str(e)}

    def map_natural_language_to_schema(self, query, schema):
        tokens = [w.strip('.,?') for w in query.lower().split()]
        mapping = {}
        col_names = []
        for t,meta in schema.items():
            col_names.extend([c['name'] for c in meta['columns']])
        for tok in tokens:
            matches = difflib.get_close_matches(tok, col_names, n=1, cutoff=0.6)
            if matches:
                mapping[tok] = matches[0]
        return mapping
