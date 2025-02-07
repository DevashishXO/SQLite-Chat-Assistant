import re

def validate_sql(sql):
    # Allowing only SELECT queries
    if not re.match(r'^SELECT\s.+',sql, re.IGNORECASE):
        return False
    # Blocking forbidden keywords
    forbidden_keywords = ['DROP', 'DELETE', 'UPDATE', 'INSERT', 'CREATE', 'ALTER', 'TRUNCATE']
    for keyword in forbidden_keywords:
        if re.search(r'\b{}\b'.format(keyword), sql, re.IGNORECASE):
            return False
    return True