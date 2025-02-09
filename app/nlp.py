from transformers import pipeline
import re
from typing import Dict

class NLPToSQL2:
    def __init__(self):
        self.model = pipeline(
            "text2text-generation",
            model="mrm8488/t5-base-finetuned-wikiSQL",
            tokenizer="t5-base"
        )

    def query_to_sql(self, user_query):
        prompt = (f"Generate a valid SQL query in the correct format based on the following schema:\n"
            f"Table1: Employees\n"
            f"Columns: ID, Name, Department, Salary\n"
            f"Table2: Departments\n"
            f"Columns: Name, Manager\n"
            f"Natural Language: {user_query}"
            f"SQL query:"
                  )
        
        result = self.model(prompt, max_length=200)
        sql = result[0]['generated_text']
                
        return sql
    
class NLPToSQL:
    def __init__(self):
        self.query_patterns: Dict[str, str] = {
            r"show\s+(?:me\s+)?all\s+employees?\s+in\s+(?:the\s+)?(\w+)\s+department": 
                "SELECT * FROM Employees WHERE LOWER(Department) = LOWER('{}')",
            
            r"who\s+is\s+(?:the\s+)?manager\s+of\s+(?:the\s+)?(\w+)\s+department": 
                "SELECT Manager FROM Departments WHERE LOWER(Name) = LOWER('{}')",
            
            r"list\s+(?:all\s+)?employees?\s+hired\s+after\s+(\d{4}-\d{2}-\d{2})":
                "SELECT * FROM Employees WHERE Hire_Date > '{}'",
            
            r"what\s+is\s+(?:the\s+)?total\s+salary\s+(?:expense\s+)?for\s+(?:the\s+)?(\w+)\s+department":
                "SELECT SUM(Salary) as Total_Salary FROM Employees WHERE LOWER(Department) = LOWER('{}')",
            
            r"show\s+(?:me\s+)?(?:the\s+)?salary\s+of\s+(\w+)":
                "SELECT Salary FROM Employees WHERE LOWER(Name) = LOWER('{}')",
            
            r"list\s+(?:all\s+)?employees?\s+with\s+salary\s+(?:greater|more)\s+than\s+(\d+)":
                "SELECT * FROM Employees WHERE Salary > {}",
            
            r"(?:show|list)\s+(?:me\s+)?all\s+departments":
                "SELECT * FROM Departments",
            
            r"(?:show|list)\s+(?:me\s+)?all\s+employees":
                "SELECT * FROM Employees"
        }

    def query_to_sql(self, user_query: str) -> str:
        normalized_query = " ".join(user_query.lower().split())
        
        for pattern, sql_template in self.query_patterns.items():
            match = re.search(pattern, normalized_query, re.IGNORECASE)
            if match:
                if match.groups():
                    return sql_template.format(*match.groups())
                return sql_template
        
        return self._generate_fallback_query(normalized_query)
    
    def _generate_fallback_query(self, query: str) -> str:
        if any(word in query for word in ['department', 'manager']):
            return "SELECT * FROM Departments"
        return "SELECT * FROM Employees"
    
    def sanitize_sql(self, sql: str) -> str:
        sql = re.sub(r'[;"]', '', sql)
        sql = sql.replace("'", "''")
        if not sql.strip().endswith(';'):
            sql = f"{sql};"
        
        return sql