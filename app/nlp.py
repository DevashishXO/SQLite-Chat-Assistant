from transformers import pipeline

class NLPToSQL:
    def __init__(self):
        self.model = pipeline(
            "text2text-generation",
            model="mrm8488/t5-base-finetuned-wikiSQL",
            tokenizer="t5-base"
        )

    def query_to_sql(self, user_query):
        prompt = f"translate English to SQL: {user_query}"
        result = self.model(prompt, max_length=200)
        return result[0]['generated_text']