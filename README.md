# Reverse PDF Scraper

> This code is part of master thesis titled "Accelerating Business Case Development with Context-Aware AI: A Question Answering System Integrating PDF Corpora and Web Retrieval"

`reverse-pdf-scraper` is a web scraping tool designed to trace backward references in documents. It reads a given PDF file, extracts all the URLs cited within it, and then crawls those web pages to retrieve their contents. These contents will be assessed if it is relevant with given context term, vectorised, and saved in Milvus vector store. Built using [Scrapy](https://scrapy.org/).

## 🖥️ Requirements

### ✅ Supported Systems

This project has been tested on the following system configuration:

| Operating System | Chip                              | RAM  | Python Version |
| ---------------- | --------------------------------- | ---- | -------------- |
| macOS 15         | Apple M2 (8-Core CPU, 8-Core GPU) | 8 GB | 3.13           |
| Windows 11       | Intel Core i7-1165G7 (4-Core CPU) | 16 GB | 3.13           |

> ℹ️ Other systems may work but have not been officially tested.

### 📦 External Dependencies

1. **Milvus** – Ensure you have a Milvus instance running. You can host it locally using Docker or connect to a remote instance. Refer to the Milvus documentation for setup instructions.

## ⚙️ Setup Python Environment

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
scrapy crawl reverse-pdf-scraper -a context="example context" -a reference_document="example/path/to/document.pdf"
```
