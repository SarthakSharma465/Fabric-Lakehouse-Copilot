# Datasonic Lakehouse Copilot

This repository provides multiple approaches for building a **Data Agent on top of a Fabric Lakehouse**, enabling **natural language querying** for both business and technical users. By combining **SQLAlchemy**, **LangChain Agents**, **OpenAI API**, and direct `pyodbc` calls, users can ask questions in plain English and get SQL-driven answers from their data.

---

## 🚀 Features

* **Natural Language to SQL**: Query the Lakehouse without writing SQL manually.
* **Two paradigms supported**:

  1. **LangChain-based SQL Agent** (`SQLAlchemy` + `LangChain`).
  2. **Direct OpenAI Orchestration** (`pyodbc` + `openai`).
* **Schema Extraction**: Extract schema metadata and generate JSON/Markdown/CSV artifacts.
* **Streamlit UI** for interactive querying.
* **Conversation History Support** in the v2 LangChain version.

---

## 📂 Repository Structure

```
.
├── SQL_Alchemy_Langchain_Approach.py   # LangChain + SQLAlchemy (basic, no history)
├── sql_alchemy_v2.py                   # LangChain + SQLAlchemy (chat history enabled)
├── Pyodbc_OpenAI_ApproachV1.py         # Direct pyodbc + OpenAI (prompt-driven pipeline)
├── schema_extractor.py                 # Schema extraction + documentation tool
├── requirements.txt                    # Python dependencies
```

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd <repo-name>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt**

```text
python-dotenv
langchain-community
langchain-openai
pandas
pyodbc
SQLAlchemy
streamlit
openai
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
SERVER=your_sql_server
DATABASE=your_database
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
TENANT_ID=your_tenant_id
API_KEY=your_openai_api_key
```

---

## ▶️ Usage

### Run the LangChain Copilot

```bash
streamlit run SQL_Alchemy_Langchain_Approach.py
```

or

```bash
streamlit run sql_alchemy_v2.py
```

* Enter a **natural language query** in the Streamlit UI.
* The agent translates it into SQL, executes it, and returns the result.
* The **v2 version** retains conversation history for context-aware Q\&A.

### Run the PyODBC + OpenAI Approach

```bash
streamlit run Pyodbc_OpenAI_ApproachV1.py
```

This version follows a **multi-step pipeline**:

1. **Prompt Optimizer** → Refines the raw query.
2. **SQL Generator** → Produces optimized T-SQL.
3. **Executor** → Runs the query via `pyodbc`.
4. **Answer Composer** → Converts raw results into a business-friendly summary.

### Run the Schema Extractor

```bash
python schema_extractor.py
```

Outputs:

* `schema.json` – Machine-readable schema.
* `schema.md` – Human-readable schema report.
* `columns.csv` – Flattened column inventory.

---

## 📊 Example Queries

* *"Show me the top 10 customers by policy count"*
* *"List claims from last month grouped by broker"*
* *"Get the row count of the customer table"*

---

## 🛠️ Tech Stack

* **LangChain** (SQL Agent orchestration).
* **SQLAlchemy** + **PyODBC** (SQL Server connectivity).
* **OpenAI API** (LLM reasoning).
* **Streamlit** (UI).
* **Pandas** (schema & data handling).

---

## 🔮 Future Enhancements

* Unified orchestration between LangChain and PyODBC approaches.
* Role-based query authorization.
* Native Fabric Lakehouse connectors.
* Multimodal outputs (tables + charts).

---

## 📜 License

This project is licensed under the MIT License.

---
