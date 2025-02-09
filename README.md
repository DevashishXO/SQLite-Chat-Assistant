---
title: nlp-to-sql-chat-assistant
emoji: 🚀
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 5.15.0
app_file: app/app.py
pinned: false
---

# SQL Chat Assistant

## Public Testing

```sh
https://huggingface.co/spaces/DevashishNagpal/nlp-to-sql-chat-assistant

```
**Note:** If the model fails to understand the user query, it generates a fallback query according based on the input.:

```sql
SELECT * FROM employees;
SELECT * FROM DEPARTMENTS;
```

Please note that this project is still under development, and the model may not work as expected for all queries. Feel free to test it out and provide feedback for improvements. 

Example queries:
- "Show me all the employees"
- "Show me the employees who are managers"
- "Who is the manager of Marketing department?"


## Overview

This project is a Flask-based chat assistant that converts natural language queries into SQL statements using state-of-the-art NLP models. The system leverages Hugging Face transformer models, sentence embedding techniques, and fine-tuning approaches to generate accurate SQL queries for an SQLite database.

The primary goal of this project is to enable users to interact with structured data using conversational language, making database queries accessible to non-technical users.

## Approach

### 1. Pretrained Transformer Models (Hugging Face)

Initially, multiple Hugging Face models were tested to generate SQL queries from natural language inputs. However, most of them produced inconsistent results due to their general training data.

### 2. Sentence Transformers + Cosine Similarity + Parameter Extraction

To improve query generation, I experimented with an approach that captures the semantic meaning of user queries and maps them to predefined SQL templates using:

- **Sentence embeddings**: Extracting vector representations of queries.
- **Cosine similarity**: Matching user queries with predefined SQL structures.
- **Regular expression templates**: Extracting SQL parameters dynamically to refine query formation.

### 3. Fine-Tuning T5-Small with ONNX Quantization

To enhance accuracy, I fine-tuned the t5-small model using a custom dataset based on the structure of my SQLite database.

ONNX quantization was applied to reduce the model size and improve deployment efficiency while staying within hosting constraints.

## Installation Guide

### 1. Clone the Repository

```sh
git clone https://github.com/DevashishXO/SQLite-Chat-Assistant.git
cd SQLite-Chat-Assistant
```

### 2. Install Dependencies

```sh
pip install -r requirements.txt
```

### 3. Set up the SQLite Database

```sh
python data/initialize_db.py
```


### 4. Run the Flask App

```sh
$env:FLASK_APP="app.main:app"
flask run
```

## Models Explored for the Project

I experimented with multiple models before settling on the fine-tuned t5-small model with ONNX quantization.

## Models Explored and Rejected

| Model                                      | Reason for Rejection                                                                 |
|--------------------------------------------|--------------------------------------------------------------------------------------|
| mrm8488/t5-base-finetuned-wikiSQL          | Produced incorrect table references due to its focus on WikiSQL datasets.            |
| tscholak/cxmefzzi                          | Large model size, requiring high computational resources for inference.              |
| HridaAI/Hrida-T2SQL-3B-V0.2                | Optimized for Spider dataset, failing on custom schemas.                             |
| cssupport/t5-small-awesome-text-to-sql     | Limited accuracy without schema-specific fine-tuning.                                |
| hasibzunair/t5-small-spider-sql            | Required significant schema customization.                                           |
| hkunlp/text2sql-t5-small                   | Generated incomplete queries.                                                        |
| szarnyasg/transformer-text2sql             | Poor generalization on varied SQL queries.                                           |
| jimypbr/gpt2-finetuned-wikitext2           | GPT-2 was not suited for structured SQL generation.                                  |

## Future Improvements

- Enhance dataset for fine-tuning.
- Implement caching for faster response times.
- Deploy the model using Hugging Face Spaces or an optimized cloud server.

## Author
Devashish Nagpal

### GitHub: github.com/DevashishXO
### LinkedIn: linkedin.com/in/devashishnagpal

## License
This project is open-source under the MIT License.
