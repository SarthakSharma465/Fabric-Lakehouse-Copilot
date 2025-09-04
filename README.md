# Datasonic Lakehouse Copilot

This project provides a **Data Agent** built on top of a **Fabric Lakehouse**, enabling **natural language querying** for both business and technical users. By combining **SQLAlchemy**, **LangChain Agents**, and the **OpenAI API**, the solution allows users to ask questions in plain English and get meaningful SQL-driven answers from their data.

Two versions of the application are included, with the same core functionality but differing in **UI chat history retention**.

---

## 🚀 Features

* **Natural Language to SQL**: Query the Lakehouse without writing SQL manually.
* **LangChain SQL Agent**: Uses LangChain’s agent toolkit to translate queries into SQL.
* **SQLAlchemy Integration**: Provides reliable connections to SQL Server with `pyodbc`.
* **Schema Extraction Tool**: Includes a `schema_extractor.py` utility to generate schema metadata (`JSON`, `Markdown`, and `CSV`).
* **Streamlit UI**: Simple web interface for user interaction.
* **Conversation History**:

  * `SQL_Alchemy_Langchain_Approach.py` → Basic version, no persistent chat history.
  * `sql_alchemy_v2.py` → Enhanced version with retained chat history for contextual conversations.

---

## 📂 Repository Structure

```
.
├── SQL_Alchemy_Langchain_Approach.py   # Initial version (no chat history retention)
├── sql_alchemy_v2.py                   # Enhanced UI with chat history
├── schema_extractor.py                 # Utility for schema extraction & documentation
```

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone <repo-url>
cd <repo-name>
```

### 2. Install Dependencies

Ensure Python 3.9+ is installed.

```bash
pip install -r requirements.txt
```

**Example requirements** (adjust as needed):

```text
sqlalchemy
pyodbc
streamlit
langchain
langchain-openai
python-dotenv
pandas
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

### Run the Lakehouse Copilot

```bash
streamlit run sql_alchemy_v2.py
```

or

```bash
streamlit run SQL_Alchemy_Langchain_Approach.py
```

* Enter a **natural language query** in the UI.
* The agent translates it into SQL, executes it, and returns the result.
* The **v2 version** keeps chat history for context-aware Q\&A.

### Run the Schema Extractor

```bash
python schema_extractor.py
```

This generates:

* `schema.json` – Full schema metadata.
* `schema.md` – Human-readable Markdown report.
* `columns.csv` – Flattened column inventory.

---

## 📊 Example Queries

* *"Show me the top 10 customers by policy count"*
* *"List claims from last month grouped by broker"*
* *"Get the row count of the customer table"*

---

## 🛠️ Tech Stack

* **[SQLAlchemy](https://www.sqlalchemy.org/)** – Database connection and query execution.
* **[LangChain](https://www.langchain.com/)** – LLM orchestration and SQL Agent.
* **[OpenAI API](https://platform.openai.com/)** – Natural language processing.
* **[Streamlit](https://streamlit.io/)** – Lightweight UI.
* **[PyODBC](https://github.com/mkleehammer/pyodbc)** – SQL Server connectivity.

---

## 🔮 Future Enhancements

* Add role-based access controls for queries.
* Integrate with other Lakehouse engines (e.g., Delta, Fabric native).
* Expand to support multimodal outputs (charts, tables, summaries).

---

## 📜 License

This project is licensed under the MIT License.

---

Would you like me to also create a **ready-to-use `requirements.txt`** file from your uploaded code so you don’t have to manually compile dependencies?
