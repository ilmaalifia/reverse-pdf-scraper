# Reverse PDF Scraper

> This code is part of master thesis titled "Accelerating Business Case Development with Context-Aware AI: A Question Answering System Integrating PDF Corpora and Web Retrieval"

`reverse-pdf-scraper` is a web scraping tool built using [Scrapy](https://scrapy.org/) which is designed to trace backward references in documents. It reads a given PDF file, extracts all the URLs cited within it, and then crawls those web pages to retrieve their contents. These contents will be assessed if it is relevant with given topic, vectorised, and saved in Milvus vector database.

## 🖥️ Tested Machine Specs

This project has been tested on the following systems:

| OS       | CPU      | RAM  | Python Version |
| -------- | -------- | ---- | -------------- |
| macOS 15 | Apple M2 | 8 GB | 3.13           |

## ⚙️ Setup Instructions

You can set up the environment using either **Conda/Miniconda** or **Python venv**.

### 📦 Option 1: Using Conda/Miniconda

1. Create and activate a new environment:

   ```bash
   conda create -n reverse_pdf_env python=3.13 -y
   conda activate reverse_pdf_env
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

### 🐍 Option 2: Using Python Virtualenv

1. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   .\venv\Scripts\activate    # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

### 🔐 Setup Credential File and Update USER_AGENT

1. Copy the example file `.env.example` as `.env`:

```bash
cp .env.example .env          # macOS/Linux
copy .env.example .env        # Windows
```

2. Open the `.env` file in a text editor and fill in the required values, for example:

```env
...
MILVUS_URI=your-milvus-uri
MILVUS_TOKEN=your-milvus-token
...
```

3. Save the file. The system will automatically load variables from `.env` during execution.

4. Update `USER_AGENT` in `app/settings.py` with your email.

5. [OPTIONAL] You can adjust other Scrapy settings (e.g. depth limit, etc.) in `app/settings.py` based on [Scrapy settings documentation](https://docs.scrapy.org/en/latest/topics/settings.html).

## 🚀 How to Run

Run the Scrapy spider using the following command:

```bash
scrapy crawl reverse_pdf_spider \
  -a topic="example topic" \
  -a document_path="example/path/to/document.pdf"
```
