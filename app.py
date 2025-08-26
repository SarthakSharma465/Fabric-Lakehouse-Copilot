import pyodbc
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI
import json 

# from schema_tools import generate_schema, save_schema_artifacts


# --- robust import of local schema_extractor.py -----------------------------
import os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "schema_extractor.py")
spec = importlib.util.spec_from_file_location("schema_extractor", SCHEMA_PATH)
schema_extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(schema_extractor)

# sanity prints (run once; then remove if you like)
print("USING MODULE:", schema_extractor.__file__)
print("HAS generate_schema?", hasattr(schema_extractor, "generate_schema"))
print("HAS save_schema_artifacts?", hasattr(schema_extractor, "save_schema_artifacts"))

# convenient aliases
generate_schema = schema_extractor.generate_schema
save_schema_artifacts = schema_extractor.save_schema_artifacts

# Load environment variables from .env (optional)
load_dotenv()

if "schema_model" not in st.session_state: 
    st.session_state.schema_model = ""

if "schema_json" not in st.session_state:
   st.session_state.schema_json = ""

# Environment Variables
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_KEY = os.getenv("API_KEY")
TENANT_ID = os.getenv("TENANT_ID")
API_KEY = os.getenv("API_KEY")

# Build connection string
conn = (
    "Driver={ODBC Driver 18 for SQL Server};"
    f"Server={SERVER};"
    f"Database={DATABASE};"
    "Authentication=ActiveDirectoryServicePrincipal;"
    f"UID={CLIENT_ID};"
    f"PWD={CLIENT_SECRET};"
    f"Authority Id={TENANT_ID};"
    "Encrypt=yes;TrustServerCertificate=no;"
)

def TestConnection(conn_str):
    """Test the database connection by running a simple query."""
    try:
        with pyodbc.connect(conn_str, timeout=30) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 AS test_value;")
            response = cursor.fetchone()  # Get one row
            return f"Connection Successful! Test Value = {response.test_value}"
    except Exception as e:
        return f"Connection Failed! Error: {e}"
    
def api_call(system, user):
    client = OpenAI(api_key=API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",   # or "gpt-4o", "gpt-3.5-turbo", etc.
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    return response.choices[0].message.content.strip()


# --- Streamlit UI ---
print(TestConnection(conn_str=conn))

st.set_page_config(layout="wide")
st.title("AI Interaction Layer")

col1, col2 = st.columns(2)
# with col1: 
#   if st.button("SQL Connection", key="1"):
#     st.text(TestConnection(conn_str=conn))
with col1:
  if st.button("Extract Schema", key="extract"):
    with st.spinner("Extracting schema..."):
        model, columns_df, warnings = generate_schema(conn, server=SERVER, database=DATABASE)
        # Save locally each run (optional)
        save_schema_artifacts(model)
        
        st.session_state.schema_model = model
        st.session_state.schema_json = json.dumps(model, indent=2)
        
        st.success("Schema extracted.")
        # if warnings:
        #     for w in warnings:
        #         st.warning(w)
        # st.dataframe(columns_df, use_container_width=True, hide_index=True)

# st.text(st.session_state.schema_json)
user_prompt = st.text_area("Enter your prompt:") + st.session_state.schema_json
system_prompt = '''You are PromptOptimizer. Rewrite a raw user query into ONE concise prompt for a downstream LLM
to generate correct, efficient T-SQL for Azure SQL/Fabric. Use ONLY the provided schema_context.
Do not invent tables/columns.

INPUTS:
- user_query: <<<{{user_query}}>>>
- schema_context: <<<{{schema_context}}>>>   # tables/columns and optional human descriptions

SCHEMA HINTS (GoldLakehouse):
- Facts: dbo.fact_policy (home/property), dbo.factpc_auto (auto)
- Home/Property dims: dbo.dim_customer, dbo.dim_property, dbo.dim_location, dbo.dim_payment,
  dbo.dim_coverage, dbo.dim_policy_status, dbo.dim_date, dbo.dim_product (+ *_home variants)
- Auto dims: dbo.dimcustomer_auto, dbo.dimpolicy_auto, dbo.dimvehicle_auto, dbo.dimclaims_auto,
  dbo.dimbroker_auto, dbo.dimfacility_auto
- No enforced FK constraints; infer joins using *_key/id naming.

JOIN HEURISTICS (use when missing in schema):
- fact_policy.customer_key    = dim_customer.customer_key
- fact_policy.property_key    = dim_property.property_key
- fact_policy.location_key    = dim_location.location_key
- fact_policy.payment_key     = dim_payment.payment_key
- fact_policy.coverage_key    = dim_coverage.coverage_key
- fact_policy.policy_status_key = dim_policy_status.status_key
- Date: join fact_policy.cover_start (or quote_date) ↔ dim_date.full_date for grains
- Auto factpc_auto joins:
  - cust_id      ↔ dimcustomer_auto.cust_id
  - chassis_no   ↔ dimvehicle_auto.chassis_no  (or regn ↔ dimvehicle_auto.regn)
  - broker_id    ↔ dimbroker_auto.broker_id
  - facility_id  ↔ dimfacility_auto.facility_id
  - claim_no     ↔ dimclaims_auto.claim_no

YOUR TASK:
Rewrite user_query into a SHORT, schema-aware prompt that the next LLM will follow to produce SQL.
Be decisive. If the user query is ambiguous, make minimal, clearly labeled assumptions.

MUST INCLUDE (in natural, compact prose or bullet list):
1) Line of business: home | auto | mixed | unknown
2) Target output (columns + grain), e.g., “month, policy_count, total_premium”
3) Relevant tables only (subset), with explicit join paths
4) Filters (dates, product/LOB, region/status), mark assumed vs given
5) Measures / aggregations
6) Dialect: “T-SQL for Azure SQL/Fabric”
7) Constraints:
   - Use only listed tables/columns
   - Prefer dim_date for time grouping
   - Avoid SELECT *
   - No full scans beyond necessary joins
   - Add readable aliases

OUTPUT:
Return exactly ONE block starting with:
REFINED_PROMPT:
<the rewritten prompt for the next model to generate SQL>

Do not return JSON. Do not include anything else besides that single block.

EXAMPLES (illustrative):

user_query: “trend of policies and premium by month for last 2 years (home)”
→
REFINED_PROMPT:
Generate T-SQL for Azure SQL/Fabric to return monthly metrics for Home line of business over the last 24 months.
Output columns: month_start, policy_count, total_premium.
Use only these tables/columns and joins:
- dbo.fact_policy(fp): policy_number, premium, cover_start, customer_key, policy_status_key
- dbo.dim_date(dd): full_date, month, year
- dbo.dim_product(dp): lob (assume ‘Home’)
Join rules:
- fp.cover_start = dd.full_date
- (If needed to filter Home) join to dp via product context available to facts; otherwise assume Home filter is not required.
Filters:
- dd.full_date >= DATEADD(MONTH, -24, CAST(GETDATE() AS date))  [assumed]
Measures:
- policy_count = COUNT(DISTINCT fp.policy_number)
- total_premium = SUM(fp.premium)  (remove if column not present)
Constraints:
- Use explicit column lists, readable aliases, and monthly grouping via dim_date.
'''

if st.button("Prompt Optimizer", key="2"):
  refined_prompt = api_call(system=system_prompt, user=user_prompt)
  st.text(refined_prompt)

if st.button("SQL Query Generation", key="3"):
   sql_query = api_call(system="You are an expert in writing efficient T-SQL for Azure SQL/Fabric.",
                        user=refined_prompt)
   st.text(sql_query)





