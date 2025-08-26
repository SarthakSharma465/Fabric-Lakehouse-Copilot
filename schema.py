import os
import json
from datetime import datetime, timezone

import pyodbc
import pandas as pd
from dotenv import load_dotenv

# =========================================================
# Starter: env, connection string, and TestConnection()
# =========================================================
load_dotenv()

SERVER = os.getenv("SERVER")
DATABASE = os.getenv("DATABASE")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
API_KEY = os.getenv("API_KEY")  # not used here, but kept from starter
TENANT_ID = os.getenv("TENANT_ID")

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
        with pyodbc.connect(conn_str, timeout=30) as _cxn:
            cur = _cxn.cursor()
            cur.execute("SELECT 1 AS test_value;")
            r = cur.fetchone()
            return f"Connection Successful! Test Value = {r.test_value}"
    except Exception as e:
        return f"Connection Failed! Error: {e}"


# =========================================================
# Metadata Queries (catalogs/DMVs only)
# =========================================================
def fetch_schemas(conn_str: str) -> pd.DataFrame:
    sql = """
    SELECT s.schema_id, s.name AS schema_name
    FROM sys.schemas AS s
    ORDER BY s.name;
    """
    with pyodbc.connect(conn_str, timeout=30) as cxn:
        return pd.read_sql(sql, cxn)


def fetch_tables_and_views(conn_str: str) -> pd.DataFrame:
    sql = """
    SELECT 
        o.object_id,
        s.name AS schema_name,
        o.name AS object_name,
        CASE WHEN o.type = 'U' THEN 'TABLE'
             WHEN o.type = 'V' THEN 'VIEW'
             ELSE o.type_desc END AS object_type
    FROM sys.objects AS o
    INNER JOIN sys.schemas AS s ON s.schema_id = o.schema_id
    WHERE o.type IN ('U','V') AND ISNULL(o.is_ms_shipped, 0) = 0
    ORDER BY s.name, o.name;
    """
    with pyodbc.connect(conn_str, timeout=30) as cxn:
        return pd.read_sql(sql, cxn)


def fetch_columns(conn_str: str) -> pd.DataFrame:
    sql = """
    SELECT 
        c.object_id,
        c.column_id AS ordinal_position,
        c.name AS column_name,
        t.name AS data_type,
        c.max_length,
        c.is_nullable,
        c.is_computed,
        dc.definition AS default_definition
    FROM sys.columns AS c
    INNER JOIN sys.types AS t
        ON t.user_type_id = c.user_type_id
    INNER JOIN sys.objects AS o
        ON o.object_id = c.object_id
    LEFT JOIN sys.default_constraints AS dc
        ON dc.parent_object_id = c.object_id AND dc.parent_column_id = c.column_id
    WHERE o.type IN ('U','V')
    ORDER BY c.object_id, c.column_id;
    """
    with pyodbc.connect(conn_str, timeout=30) as cxn:
        return pd.read_sql(sql, cxn)


def fetch_primary_keys(conn_str: str) -> pd.DataFrame:
    sql = """
    SELECT 
        k.parent_object_id AS object_id,
        k.name AS constraint_name,
        ic.column_id,
        ic.key_ordinal
    FROM sys.key_constraints AS k
    INNER JOIN sys.index_columns AS ic
        ON ic.object_id = k.parent_object_id
       AND ic.index_id = k.unique_index_id
    WHERE k.type = 'PK'
    ORDER BY k.parent_object_id, ic.key_ordinal;
    """
    with pyodbc.connect(conn_str, timeout=30) as cxn:
        return pd.read_sql(sql, cxn)


def fetch_unique_constraints(conn_str: str) -> pd.DataFrame:
    sql = """
    SELECT 
        k.parent_object_id AS object_id,
        k.name AS constraint_name,
        ic.column_id,
        ic.key_ordinal
    FROM sys.key_constraints AS k
    INNER JOIN sys.index_columns AS ic
        ON ic.object_id = k.parent_object_id
       AND ic.index_id = k.unique_index_id
    WHERE k.type = 'UQ'
    ORDER BY k.parent_object_id, k.name, ic.key_ordinal;
    """
    with pyodbc.connect(conn_str, timeout=30) as cxn:
        return pd.read_sql(sql, cxn)


def fetch_foreign_keys(conn_str: str) -> pd.DataFrame:
    sql = """
    SELECT 
        fk.name AS constraint_name,
        fk.parent_object_id AS parent_id,
        fkc.parent_column_id,
        fk.referenced_object_id AS ref_id,
        fkc.referenced_column_id,
        fkc.constraint_column_id
    FROM sys.foreign_keys AS fk
    INNER JOIN sys.foreign_key_columns AS fkc
        ON fkc.constraint_object_id = fk.object_id
    ORDER BY fk.parent_object_id, fk.name, fkc.constraint_column_id;
    """
    with pyodbc.connect(conn_str, timeout=30) as cxn:
        return pd.read_sql(sql, cxn)


def fetch_row_counts(conn_str: str):
    """
    DMV-based approximate row counts.
    Returns (row_counts_df, warning_or_none)
    """
    sql = """
    SELECT 
        p.object_id,
        SUM(CASE WHEN p.index_id IN (0,1) THEN p.row_count ELSE 0 END) AS row_count
    FROM sys.dm_db_partition_stats AS p
    GROUP BY p.object_id;
    """
    try:
        with pyodbc.connect(conn_str, timeout=30) as cxn:
            df = pd.read_sql(sql, cxn)
        return df, None
    except Exception as e:
        warn = f"Row counts unavailable via sys.dm_db_partition_stats: {e}"
        return pd.DataFrame(columns=["object_id", "row_count"]), warn


# =========================================================
# Assembly & Writers
# =========================================================
def assemble_model(
    server: str,
    database: str,
    tables_views: pd.DataFrame,
    columns: pd.DataFrame,
    pks: pd.DataFrame,
    uqs: pd.DataFrame,
    fks: pd.DataFrame,
    row_counts: pd.DataFrame,
    warnings: list
) -> dict:
    objects = tables_views.copy().rename(columns={"object_name": "table_name"})
    obj_map = {
        int(r.object_id): {
            "schema_name": r.schema_name,
            "table_name": r.table_name,
            "object_type": r.object_type,
        }
        for _, r in objects.iterrows()
    }

    col_name_map = {
        (int(r.object_id), int(r.ordinal_position)): r.column_name
        for _, r in columns.iterrows()
    }

    # Primary Keys
    pk_map, pk_col_set = {}, set()
    if not pks.empty:
        for oid, grp in pks.groupby("object_id", sort=True):
            grp_sorted = grp.sort_values("key_ordinal")
            cols = [col_name_map.get((int(oid), int(x.column_id))) for _, x in grp_sorted.iterrows()]
            pk_map[int(oid)] = [c for c in cols if c is not None]
            for _, x in grp_sorted.iterrows():
                pk_col_set.add((int(oid), int(x.column_id)))

    # Unique Constraints
    uq_constraints_map, uq_col_set = {}, set()
    if not uqs.empty:
        for (oid, cname), grp in uqs.groupby(["object_id", "constraint_name"], sort=True):
            grp_sorted = grp.sort_values("key_ordinal")
            cols = [col_name_map.get((int(oid), int(x.column_id))) for _, x in grp_sorted.iterrows()]
            uq_constraints_map.setdefault(int(oid), []).append([c for c in cols if c is not None])
            for _, x in grp_sorted.iterrows():
                uq_col_set.add((int(oid), int(x.column_id)))

    # Foreign Keys
    fk_map = {}
    if not fks.empty:
        for (parent_id, cname), grp in fks.groupby(["parent_id", "constraint_name"], sort=True):
            grp_sorted = grp.sort_values("constraint_column_id")
            parent_cols = [col_name_map.get((int(parent_id), int(x.parent_column_id))) for _, x in grp_sorted.iterrows()]
            ref_id = int(grp_sorted.iloc[0]["ref_id"]) if not grp_sorted.empty else None
            ref_obj = obj_map.get(ref_id)
            ref_schema = ref_obj["schema_name"] if ref_obj else None
            ref_table = ref_obj["table_name"] if ref_obj else None
            ref_cols = [col_name_map.get((ref_id, int(x.referenced_column_id))) for _, x in grp_sorted.iterrows()]
            fk_map.setdefault(int(parent_id), []).append({
                "constraint_name": cname,
                "column_names": [c for c in parent_cols if c is not None],
                "references": {
                    "schema": ref_schema,
                    "table": ref_table,
                    "columns": [c for c in ref_cols if c is not None]
                }
            })

    # Row counts
    row_count_map = {int(r.object_id): int(r.row_count) for _, r in row_counts.iterrows() if pd.notna(r.row_count)}

    # Build schema -> tables
    schemas_order = sorted(objects["schema_name"].unique().tolist())
    schema_objs = []
    for sname in schemas_order:
        objs = objects[objects["schema_name"] == sname].sort_values("table_name", kind="mergesort")
        table_list = []
        for _, o in objs.iterrows():
            oid = int(o.object_id)
            tname = o.table_name
            otype = o.object_type

            cold = columns[columns["object_id"] == oid].sort_values("ordinal_position", kind="mergesort")
            cols_payload = []
            for _, c in cold.iterrows():
                col_id = int(c.ordinal_position)
                cols_payload.append({
                    "column_name": c.column_name,
                    "data_type": c.data_type,
                    "max_length": int(c.max_length) if pd.notna(c.max_length) else None,
                    "is_nullable": bool(c.is_nullable),
                    "ordinal_position": int(c.ordinal_position),
                    "is_primary_key": (oid, col_id) in pk_col_set,
                    "is_unique": (oid, col_id) in uq_col_set,
                    "is_computed": bool(c.is_computed),
                    "default_definition": str(c.default_definition) if pd.notna(c.default_definition) else None
                })

            rc_val = None if otype == "VIEW" else row_count_map.get(oid)
            table_list.append({
                "table_name": tname,
                "object_type": otype,
                "row_count": rc_val,
                "columns": cols_payload,
                "primary_key": pk_map.get(oid, []),
                "unique_constraints": uq_constraints_map.get(oid, []),
                "foreign_keys": fk_map.get(oid, [])
            })

        schema_objs.append({"schema_name": sname, "tables": table_list})

    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "generated_at_utc": generated,
        "server": server or "",
        "database": database or "",
        "incomplete": len(warnings) > 0,
        "warnings": warnings,
        "schemas": schema_objs
    }


def write_json(path: str, obj: dict):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def write_markdown(path: str, model: dict):
    lines = []
    lines.append("# Database Schema Inventory\n")
    lines.append(f"- **Server:** `{model.get('server')}`")
    lines.append(f"- **Database:** `{model.get('database')}`")
    lines.append(f"- **Generated (UTC):** {model.get('generated_at_utc')}")
    lines.append(f"- **Incomplete:** {model.get('incomplete')}\n")
    if model.get("warnings"):
        lines.append("> **Warnings:**")
        for w in model["warnings"]:
            lines.append(f"> - {w}")
        lines.append("")

    # Index
    lines.append("## Schema Index\n")
    for sch in model["schemas"]:
        lines.append(f"### `{sch['schema_name']}`")
        if not sch["tables"]:
            lines.append("- _No objects_")
        else:
            for obj in sch["tables"]:
                lines.append(f"- `{obj['table_name']}` ({obj['object_type']})")
        lines.append("")

    # Details
    for sch in model["schemas"]:
        lines.append(f"## Schema: `{sch['schema_name']}`")
        for obj in sch["tables"]:
            fq = f"{sch['schema_name']}.{obj['table_name']}"
            lines.append(f"\n### `{fq}` — {obj['object_type']}")
            rc = obj.get("row_count")
            lines.append(f"- **Approx Row Count:** {rc if rc is not None else 'N/A'}")
            pk = obj.get("primary_key") or []
            lines.append(f"- **Primary Key:** {', '.join(pk) if pk else 'None'}")
            uqs = obj.get("unique_constraints") or []
            lines.append(f"- **Unique Constraints:** {('; '.join([', '.join(x) for x in uqs])) if uqs else 'None'}")
            fks = obj.get("foreign_keys") or []
            if fks:
                lines.append("- **Foreign Keys:**")
                for fk in fks:
                    ref = fk["references"]
                    ref_cols = ", ".join(ref["columns"]) if ref["columns"] else ""
                    lines.append(
                        f"  - `{fk['constraint_name']}`: ({', '.join(fk['column_names'])}) "
                        f"→ `{ref.get('schema')}.{ref.get('table')}` ({ref_cols})"
                    )
            else:
                lines.append("- **Foreign Keys:** None")

            # Columns
            lines.append("\n| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |")
            lines.append("|---:|---|---|---:|:--:|:--:|:--:|:--:|---|")
            for col in sorted(obj["columns"], key=lambda c: c["ordinal_position"]):
                lines.append(
                    f"| {col['ordinal_position']} "
                    f"| `{col['column_name']}` "
                    f"| `{col['data_type']}` "
                    f"| {col['max_length'] if col['max_length'] is not None else ''} "
                    f"| {'YES' if col['is_nullable'] else 'NO'} "
                    f"| {'✓' if col['is_primary_key'] else ''} "
                    f"| {'✓' if col['is_unique'] else ''} "
                    f"| {'✓' if col['is_computed'] else ''} "
                    f"| {('`'+str(col['default_definition'])+'`') if col['default_definition'] else ''} |"
                )
            lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# =========================================================
# Driver: run extraction and store locally on each run
# =========================================================
def extract_and_store(conn_str: str, out_json="lakehouse_schema.json", out_md="lakehouse_schema.md"):
    warnings = []
    # Fetch
    tv = fetch_tables_and_views(conn_str)
    cols = fetch_columns(conn_str)
    pks = fetch_primary_keys(conn_str)
    uqs = fetch_unique_constraints(conn_str)
    fks = fetch_foreign_keys(conn_str)
    rc_df, warn = fetch_row_counts(conn_str)
    if warn:
        warnings.append(warn)

    # Assemble
    model = assemble_model(
        server=SERVER,
        database=DATABASE,
        tables_views=tv,
        columns=cols,
        pks=pks,
        uqs=uqs,
        fks=fks,
        row_counts=rc_df,
        warnings=warnings
    )

    # Write artifacts
    write_json(out_json, model)
    write_markdown(out_md, model)

    # Summary
    schema_cnt = len(model.get("schemas", []))
    table_cnt = sum(len(s.get("tables", [])) for s in model.get("schemas", []))
    col_cnt = sum(len(t.get("columns", [])) for s in model.get("schemas", []) for t in s.get("tables", []))

    print(f"Wrote: {os.path.abspath(out_json)}")
    print(f"Wrote: {os.path.abspath(out_md)}")
    print(f"SUMMARY: {schema_cnt} schemas, {table_cnt} tables, {col_cnt} columns")


if __name__ == "__main__":
    # Optional quick connectivity check
    print(TestConnection(conn_str=conn))

    try:
        extract_and_store(conn)
    except Exception as e:
        # If something fails, still emit a minimal incomplete JSON for traceability.
        generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        fallback = {
            "generated_at_utc": generated,
            "server": SERVER or "",
            "database": DATABASE or "",
            "incomplete": True,
            "warnings": [f"Extraction failed: {e}"],
            "schemas": []
        }
        write_json("lakehouse_schema.json", fallback)
        write_markdown("lakehouse_schema.md", fallback)
        print("Extraction failed; wrote incomplete artifacts.")
        print("SUMMARY: 0 schemas, 0 tables, 0 columns")
