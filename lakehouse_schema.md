# Database Schema Inventory

- **Server:** `77igns4c4tquvpkcugm4f6ldka-fwtjmerwp2aujjmgnbxi2symzq.datawarehouse.fabric.microsoft.com`
- **Database:** `GoldLakehouse`
- **Generated (UTC):** 2025-08-26T12:29:48Z
- **Incomplete:** True

> **Warnings:**
> - Row counts unavailable via sys.dm_db_partition_stats: Execution failed on sql '
    SELECT 
        p.object_id,
        SUM(CASE WHEN p.index_id IN (0,1) THEN p.row_count ELSE 0 END) AS row_count
    FROM sys.dm_db_partition_stats AS p
    GROUP BY p.object_id;
    ': ('42000', "[42000] [Microsoft][ODBC Driver 18 for SQL Server][SQL Server]DMV (Dynamic Management View) 'dm_db_partition_stats' is not supported. (15871) (SQLExecDirectW)")

## Schema Index

### `dbo`
- `dim_coverage` (TABLE)
- `dim_coverage_home` (TABLE)
- `dim_customer` (TABLE)
- `dim_customer_home` (TABLE)
- `dim_date` (TABLE)
- `dim_location` (TABLE)
- `dim_location_home` (TABLE)
- `dim_payment` (TABLE)
- `dim_payment_home` (TABLE)
- `dim_policy_status` (TABLE)
- `dim_policy_status_home` (TABLE)
- `dim_product` (TABLE)
- `dim_property` (TABLE)
- `dim_property_home` (TABLE)
- `dimbroker_auto` (TABLE)
- `dimclaims_auto` (TABLE)
- `dimcustomer_auto` (TABLE)
- `dimfacility_auto` (TABLE)
- `dimpolicy_auto` (TABLE)
- `dimvehicle_auto` (TABLE)
- `fact_policy` (TABLE)
- `factpc_auto` (TABLE)

## Schema: `dbo`

### `dbo.dim_coverage` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `sum_insured_buildings` | `float` | 8 | YES |  |  |  |  |
| 2 | `sum_insured_contents` | `float` | 8 | YES |  |  |  |  |
| 3 | `last_ann_prem_gross` | `float` | 8 | YES |  |  |  |  |
| 4 | `buildings_cover` | `bit` | 1 | YES |  |  |  |  |
| 5 | `contents_cover` | `bit` | 1 | YES |  |  |  |  |
| 6 | `spec_sum_insured` | `float` | 8 | YES |  |  |  |  |
| 7 | `spec_item_prem` | `float` | 8 | YES |  |  |  |  |
| 8 | `unspec_hrp_prem` | `float` | 8 | YES |  |  |  |  |
| 9 | `coverage_key` | `int` | 4 | YES |  |  |  |  |


### `dbo.dim_coverage_home` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `buildings_cover` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `contents_cover` | `varchar` | 8000 | YES |  |  |  |  |
| 3 | `coverage_key` | `bigint` | 8 | YES |  |  |  |  |


### `dbo.dim_customer` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `p1_dob` | `date` | 3 | YES |  |  |  |  |
| 2 | `p1_mar_status` | `varchar` | 8000 | YES |  |  |  |  |
| 3 | `p1_emp_status` | `varchar` | 8000 | YES |  |  |  |  |
| 4 | `p1_pt_emp_status` | `varchar` | 8000 | YES |  |  |  |  |
| 5 | `p1_sex` | `varchar` | 8000 | YES |  |  |  |  |
| 6 | `occ_status` | `varchar` | 8000 | YES |  |  |  |  |
| 7 | `customer_key` | `int` | 4 | YES |  |  |  |  |


### `dbo.dim_customer_home` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `p1_dob` | `date` | 3 | YES |  |  |  |  |
| 2 | `p1_mar_status` | `varchar` | 8000 | YES |  |  |  |  |
| 3 | `p1_sex` | `varchar` | 8000 | YES |  |  |  |  |
| 4 | `customer_key` | `bigint` | 8 | YES |  |  |  |  |


### `dbo.dim_date` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `date_key` | `int` | 4 | YES |  |  |  |  |
| 2 | `full_date` | `date` | 3 | YES |  |  |  |  |
| 3 | `day` | `int` | 4 | YES |  |  |  |  |
| 4 | `month` | `int` | 4 | YES |  |  |  |  |
| 5 | `month_name` | `varchar` | 8000 | YES |  |  |  |  |
| 6 | `quarter` | `int` | 4 | YES |  |  |  |  |
| 7 | `year` | `int` | 4 | YES |  |  |  |  |
| 8 | `is_weekend` | `bit` | 1 | YES |  |  |  |  |


### `dbo.dim_location` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `risk_rated_area_b` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `risk_rated_area_c` | `varchar` | 8000 | YES |  |  |  |  |
| 3 | `location_key` | `int` | 4 | YES |  |  |  |  |


### `dbo.dim_location_home` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `risk_rated_area_b` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `risk_rated_area_c` | `varchar` | 8000 | YES |  |  |  |  |
| 3 | `location_key` | `bigint` | 8 | YES |  |  |  |  |


### `dbo.dim_payment` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `payment_method` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `is_constant_payment_frequency` | `bit` | 1 | YES |  |  |  |  |
| 3 | `payment_key` | `int` | 4 | YES |  |  |  |  |


### `dbo.dim_payment_home` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `payment_method` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `payment_key` | `bigint` | 8 | YES |  |  |  |  |


### `dbo.dim_policy_status` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `pol_status` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `status_key` | `int` | 4 | YES |  |  |  |  |


### `dbo.dim_policy_status_home` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `pol_status` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `policy_status_key` | `bigint` | 8 | YES |  |  |  |  |


### `dbo.dim_product` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `product_key` | `int` | 4 | YES |  |  |  |  |
| 2 | `lob` | `varchar` | 8000 | YES |  |  |  |  |
| 3 | `product_name` | `varchar` | 8000 | YES |  |  |  |  |
| 4 | `policy_type` | `varchar` | 8000 | YES |  |  |  |  |
| 5 | `product_code` | `varchar` | 8000 | YES |  |  |  |  |


### `dbo.dim_property` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `prop_type` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `yearbuilt` | `int` | 4 | YES |  |  |  |  |
| 3 | `ownership_type` | `varchar` | 8000 | YES |  |  |  |  |
| 4 | `bedrooms` | `varchar` | 8000 | YES |  |  |  |  |
| 5 | `roof_construction` | `varchar` | 8000 | YES |  |  |  |  |
| 6 | `wall_construction` | `varchar` | 8000 | YES |  |  |  |  |
| 7 | `max_days_unocc` | `varchar` | 8000 | YES |  |  |  |  |
| 8 | `property_key` | `int` | 4 | YES |  |  |  |  |


### `dbo.dim_property_home` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `bedrooms` | `int` | 4 | YES |  |  |  |  |
| 2 | `yearbuilt` | `int` | 4 | YES |  |  |  |  |
| 3 | `roof_construction` | `varchar` | 8000 | YES |  |  |  |  |
| 4 | `wall_construction` | `varchar` | 8000 | YES |  |  |  |  |
| 5 | `prop_type` | `varchar` | 8000 | YES |  |  |  |  |
| 6 | `property_key` | `bigint` | 8 | YES |  |  |  |  |


### `dbo.dimbroker_auto` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `broker_id` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `broker_name` | `varchar` | 8000 | YES |  |  |  |  |
| 3 | `modified_date` | `datetime2` | 8 | YES |  |  |  |  |


### `dbo.dimclaims_auto` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `claim_no` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `account_code` | `smallint` | 2 | YES |  |  |  |  |
| 3 | `date_of_intimation` | `datetime2` | 8 | YES |  |  |  |  |
| 4 | `date_of_accident` | `datetime2` | 8 | YES |  |  |  |  |
| 5 | `place_of_loss` | `varchar` | 8000 | YES |  |  |  |  |
| 6 | `claim_type` | `varchar` | 8000 | YES |  |  |  |  |
| 7 | `intimated_amount` | `int` | 4 | YES |  |  |  |  |
| 8 | `intimated_sf` | `varchar` | 8000 | YES |  |  |  |  |
| 9 | `product` | `varchar` | 8000 | YES |  |  |  |  |
| 10 | `policy_type` | `varchar` | 8000 | YES |  |  |  |  |
| 11 | `claim_stage` | `varchar` | 8000 | YES |  |  |  |  |
| 12 | `claim_status` | `varchar` | 8000 | YES |  |  |  |  |
| 13 | `final_settlement_amount` | `float` | 8 | YES |  |  |  |  |
| 14 | `update_date` | `datetime2` | 8 | YES |  |  |  |  |


### `dbo.dimcustomer_auto` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `cust_id` | `int` | 4 | YES |  |  |  |  |
| 2 | `drv_dob` | `date` | 3 | YES |  |  |  |  |
| 3 | `drv_dli` | `date` | 3 | YES |  |  |  |  |
| 4 | `nationality` | `varchar` | 8000 | YES |  |  |  |  |
| 5 | `modified_date` | `datetime2` | 8 | YES |  |  |  |  |


### `dbo.dimfacility_auto` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `facility_id` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `facility_name` | `varchar` | 8000 | YES |  |  |  |  |
| 3 | `modified_date` | `datetime2` | 8 | YES |  |  |  |  |


### `dbo.dimpolicy_auto` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `policy_number` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `customer_id` | `int` | 4 | YES |  |  |  |  |
| 3 | `executive` | `varchar` | 8000 | YES |  |  |  |  |
| 4 | `body` | `varchar` | 8000 | YES |  |  |  |  |
| 5 | `make` | `varchar` | 8000 | YES |  |  |  |  |
| 6 | `model` | `varchar` | 8000 | YES |  |  |  |  |
| 7 | `use_of_vehicle` | `varchar` | 8000 | YES |  |  |  |  |
| 8 | `model_year` | `int` | 4 | YES |  |  |  |  |
| 9 | `chassis_no` | `varchar` | 8000 | YES |  |  |  |  |
| 10 | `region` | `varchar` | 8000 | YES |  |  |  |  |
| 11 | `policy_effective_date` | `datetime2` | 8 | YES |  |  |  |  |
| 12 | `policy_expiry_date` | `datetime2` | 8 | YES |  |  |  |  |
| 13 | `sum_insured` | `float` | 8 | YES |  |  |  |  |
| 14 | `policy_issue_date` | `datetime2` | 8 | YES |  |  |  |  |
| 15 | `premium` | `int` | 4 | YES |  |  |  |  |
| 16 | `product` | `varchar` | 8000 | YES |  |  |  |  |
| 17 | `policy_type` | `varchar` | 8000 | YES |  |  |  |  |
| 18 | `broker_id` | `varchar` | 8000 | YES |  |  |  |  |
| 19 | `broker_name` | `varchar` | 8000 | YES |  |  |  |  |
| 20 | `facility_id` | `varchar` | 8000 | YES |  |  |  |  |
| 21 | `facility_name` | `varchar` | 8000 | YES |  |  |  |  |


### `dbo.dimvehicle_auto` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `chassis_no` | `varchar` | 8000 | YES |  |  |  |  |
| 2 | `body` | `varchar` | 8000 | YES |  |  |  |  |
| 3 | `make` | `varchar` | 8000 | YES |  |  |  |  |
| 4 | `model` | `varchar` | 8000 | YES |  |  |  |  |
| 5 | `model_year` | `int` | 4 | YES |  |  |  |  |
| 6 | `regn` | `varchar` | 8000 | YES |  |  |  |  |
| 7 | `use_of_vehicle` | `varchar` | 8000 | YES |  |  |  |  |
| 8 | `veh_seats` | `int` | 4 | YES |  |  |  |  |
| 9 | `modified_date` | `datetime2` | 8 | YES |  |  |  |  |


### `dbo.fact_policy` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `quote_date` | `date` | 3 | YES |  |  |  |  |
| 2 | `cover_start` | `date` | 3 | YES |  |  |  |  |
| 3 | `policy_number` | `varchar` | 8000 | YES |  |  |  |  |
| 4 | `policy_duration_days` | `int` | 4 | YES |  |  |  |  |
| 5 | `customer_key` | `int` | 4 | YES |  |  |  |  |
| 6 | `property_key` | `int` | 4 | YES |  |  |  |  |
| 7 | `location_key` | `int` | 4 | YES |  |  |  |  |
| 8 | `payment_key` | `int` | 4 | YES |  |  |  |  |
| 9 | `coverage_key` | `int` | 4 | YES |  |  |  |  |
| 10 | `policy_status_key` | `int` | 4 | YES |  |  |  |  |


### `dbo.factpc_auto` — TABLE
- **Approx Row Count:** N/A
- **Primary Key:** None
- **Unique Constraints:** None
- **Foreign Keys:** None

| # | Column | Type | MaxLen | Nullable | PK | Unique | Computed | Default |
|---:|---|---|---:|:--:|:--:|:--:|:--:|---|
| 1 | `entity_id` | `bigint` | 8 | YES |  |  |  |  |
| 2 | `cust_id` | `int` | 4 | YES |  |  |  |  |
| 3 | `make` | `varchar` | 8000 | YES |  |  |  |  |
| 4 | `model` | `varchar` | 8000 | YES |  |  |  |  |
| 5 | `chassis_no` | `varchar` | 8000 | YES |  |  |  |  |
| 6 | `premium` | `int` | 4 | YES |  |  |  |  |
| 7 | `regn` | `varchar` | 8000 | YES |  |  |  |  |
| 8 | `policy_no` | `varchar` | 8000 | YES |  |  |  |  |
| 9 | `sum_insured` | `float` | 8 | YES |  |  |  |  |
| 10 | `product` | `varchar` | 8000 | YES |  |  |  |  |
| 11 | `policytype` | `varchar` | 8000 | YES |  |  |  |  |
| 12 | `broker_id` | `varchar` | 8000 | YES |  |  |  |  |
| 13 | `broker_name` | `varchar` | 8000 | YES |  |  |  |  |
| 14 | `facility_id` | `varchar` | 8000 | YES |  |  |  |  |
| 15 | `facility_name` | `varchar` | 8000 | YES |  |  |  |  |
| 16 | `account_code` | `smallint` | 2 | YES |  |  |  |  |
| 17 | `claim_no` | `varchar` | 8000 | YES |  |  |  |  |
