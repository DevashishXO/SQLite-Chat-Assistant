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

