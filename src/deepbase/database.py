# src/deepbase/database.py
"""
Database context extraction module for DeepBase.
Handles SQLite databases to provide structured context about schema and tables.
"""

import sqlite3
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ColumnInfo:
    name: str
    data_type: str
    nullable: bool
    default: Optional[str]
    primary_key: bool


@dataclass
class TableInfo:
    name: str
    columns: List[ColumnInfo]
    foreign_keys: List[Dict[str, str]]
    indexes: List[Dict[str, Any]]
    row_count: int


@dataclass
class DatabaseSchema:
    tables: List[TableInfo]
    total_size_bytes: int
    total_tables: int
    total_rows: int


def get_database_schema(db_path: str) -> DatabaseSchema:
    """
    Extract complete schema information from SQLite database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get database size
    total_size = os.path.getsize(db_path)
    
    # Get all tables (excluding sqlite internal tables)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    table_names = [row[0] for row in cursor.fetchall()]
    
    tables = []
    total_rows = 0
    
    for table_name in table_names:
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        row_count = cursor.fetchone()[0]
        total_rows += row_count
        
        # Get column info using PRAGMA
        cursor.execute(f"PRAGMA table_info(`{table_name}`)")
        columns = []
        for row in cursor.fetchall():
            col = ColumnInfo(
                name=row[1],
                data_type=row[2],
                nullable=not row[3],  # notnull column: 0=true, 1=false
                default=row[4],
                primary_key=bool(row[5])
            )
            columns.append(col)
        
        # Get foreign keys
        cursor.execute(f"PRAGMA foreign_key_list(`{table_name}`)")
        foreign_keys = []
        for row in cursor.fetchall():
            fk = {
                "id": row[0],
                "seq": row[1],
                "table": row[2],
                "from": row[3],
                "to": row[4],
                "on_update": row[5],
                "on_delete": row[6]
            }
            foreign_keys.append(fk)
        
        # Get indexes
        cursor.execute(f"PRAGMA index_list(`{table_name}`)")
        indexes = []
        for row in cursor.fetchall():
            index_name = row[1]
            cursor.execute(f"PRAGMA index_info(`{index_name}`)")
            index_columns = [r[2] for r in cursor.fetchall()]
            indexes.append({
                "name": index_name,
                "unique": row[2],
                "columns": index_columns
            })
        
        table_info = TableInfo(
            name=table_name,
            columns=columns,
            foreign_keys=foreign_keys,
            indexes=indexes,
            row_count=row_count
        )
        tables.append(table_info)
    
    conn.close()
    
    return DatabaseSchema(
        tables=tables,
        total_size_bytes=total_size,
        total_tables=len(tables),
        total_rows=total_rows
    )


def generate_database_context_full(schema: DatabaseSchema, db_name: str) -> str:
    """
    Generate full detailed context for --all mode.
    Includes complete schema, relationships, and sample data hints.
    """
    lines = [
        f"# Database: {db_name}",
        f"## Overview",
        f"- Total Tables: {schema.total_tables}",
        f"- Total Rows: {schema.total_rows:,}",
        f"- File Size: {schema.total_size_bytes:,} bytes ({schema.total_size_bytes / 1024:.2f} KB)",
        "",
        "## Schema Details",
        ""
    ]
    
    for table in schema.tables:
        lines.extend([
            f"### Table: `{table.name}`",
            f"- Rows: {table.row_count:,}",
            ""
        ])
        
        # Columns
        lines.append("#### Columns:")
        lines.append("| Column | Type | Nullable | Default | PK |")
        lines.append("|--------|------|----------|---------|-----|")
        for col in table.columns:
            pk_mark = "✓" if col.primary_key else ""
            null_mark = "✓" if col.nullable else "NOT NULL"
            default_val = col.default if col.default else "-"
            lines.append(f"| `{col.name}` | {col.data_type} | {null_mark} | {default_val} | {pk_mark} |")
        lines.append("")
        
        # Foreign Keys
        if table.foreign_keys:
            lines.append("#### Foreign Keys:")
            for fk in table.foreign_keys:
                lines.append(f"- `{fk['from']}` → `{fk['table']}`.`{fk['to']}` (ON UPDATE: {fk['on_update']}, ON DELETE: {fk['on_delete']})")
            lines.append("")
        
        # Indexes
        if table.indexes:
            lines.append("#### Indexes:")
            for idx in table.indexes:
                unique_str = "UNIQUE " if idx['unique'] else ""
                lines.append(f"- {unique_str}`{idx['name']}` on ({', '.join(f'`{c}`' for c in idx['columns'])})")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    return "\n".join(lines)


def generate_database_context_toon(schema: DatabaseSchema, db_name: str) -> str:
    """
    Generate minimal TOON-style context (skeleton only).
    Best for large databases where token efficiency matters.
    """
    lines = [
        f"DB: {db_name}",
        f"Tables: {schema.total_tables} | Rows: {schema.total_rows:,}",
        ""
    ]
    
    for table in schema.tables:
        # Compact representation: Table(columns) [FKs]
        col_defs = []
        for col in table.columns:
            flags = []
            if col.primary_key:
                flags.append("PK")
            if not col.nullable:
                flags.append("NN")
            flag_str = f"[{','.join(flags)}]" if flags else ""
            col_defs.append(f"{col.name}:{col.data_type}{flag_str}")
        
        fk_refs = []
        for fk in table.foreign_keys:
            fk_refs.append(f"{fk['from']}→{fk['table']}.{fk['to']}")
        
        fk_str = f" | FK: {', '.join(fk_refs)}" if fk_refs else ""
        lines.append(f"T: {table.name}({', '.join(col_defs)}){fk_str}")
    
    return "\n".join(lines)


def generate_database_context_hybrid(schema: DatabaseSchema, db_name: str, focused_tables: List[str]) -> str:
    """
    Generate hybrid context: TOON for all, full detail for focused tables.
    """
    lines = [
        f"# Database: {db_name}",
        f"## Overview",
        f"- Total Tables: {schema.total_tables}",
        f"- Total Rows: {schema.total_rows:,}",
        "",
        "## Schema (TOON + Focus)",
        ""
    ]
    
    for table in schema.tables:
        is_focused = table.name in focused_tables or any(f in table.name for f in focused_tables)
        
        if is_focused:
            # Full detail for focused tables
            lines.extend([
                f"### [FOCUSED] Table: `{table.name}` ⭐",
                f"- Rows: {table.row_count:,}",
                ""
            ])
            
            lines.append("#### Columns:")
            lines.append("| Column | Type | Nullable | Default | PK |")
            lines.append("|--------|------|----------|---------|-----|")
            for col in table.columns:
                pk_mark = "✓" if col.primary_key else ""
                null_mark = "✓" if col.nullable else "NOT NULL"
                default_val = col.default if col.default else "-"
                lines.append(f"| `{col.name}` | {col.data_type} | {null_mark} | {default_val} | {pk_mark} |")
            lines.append("")
            
            if table.foreign_keys:
                lines.append("#### Foreign Keys:")
                for fk in table.foreign_keys:
                    lines.append(f"- `{fk['from']}` → `{fk['table']}`.`{fk['to']}`")
                lines.append("")
        else:
            # TOON style for non-focused
            col_names = [f"{col.name}:{col.data_type}" + ("(PK)" if col.primary_key else "") 
                        for col in table.columns]
            lines.append(f"- `{table.name}`: {', '.join(col_names)}")
    
    return "\n".join(lines)


def is_sqlite_database(file_path: str) -> bool:
    """
    Check if file is a valid SQLite database by reading magic bytes.
    """
    try:
        with open(file_path, 'rb') as f:
            header = f.read(16)
            return header[:16] == b'SQLite format 3\x00'
    except:
        return False