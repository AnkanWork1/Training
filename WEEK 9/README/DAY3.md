# DAY 3 — TOOL-CALLING AGENTS

**(Code Execution, Files, Database, Search Tools)**

---

# 📌 Overview

Day 3 introduces **tool-using agents**, where AI agents interact with real system tools such as:

* Python code execution
* File systems
* Databases
* Local search utilities

Unlike pure LLM reasoning, tool-calling agents allow the system to **execute real operations** and return **verifiable results**.

This architecture is commonly used in modern agent frameworks like **AutoGen, LangGraph, and CrewAI**.

---

# 🎯 Learning Outcomes

After completing this module you will understand:

* How agents interact with **external tools**
* How to implement **function calling without external APIs**
* How to build **system-to-tool execution pipelines**
* How multiple agents collaborate to solve real tasks

Key abilities gained:

* Agents executing Python code
* Agents querying databases
* Agents reading and writing files
* Agents performing local search operations

---

# 🧠 Core Concepts

## 1. Tool-Calling Agents

Tool-calling agents are AI agents capable of executing **external programs or system tools**.

Instead of only generating text, they can:

* Run Python scripts
* Query databases
* Read or write files
* Execute shell commands

Example workflow:

```
User Query
    ↓
Orchestrator
    ↓
Agent selects tool
    ↓
Tool execution
    ↓
Result returned to agent
    ↓
Final response
```

---

## 2. Python Tool Calling

Agents can run Python code dynamically to perform tasks such as:

* data analysis
* mathematical computation
* automation
* file processing

Example use cases:

* dataset analysis
* generating reports
* running scripts
* executing algorithms

---

## 3. Shell Command Tools

Agents can execute shell commands to interact with the operating system.

Example commands:

```
ls
grep
wc
cat
```

Possible applications:

* searching files
* system inspection
* log analysis
* automation pipelines

---

## 4. SQLite / CSV Querying

Agents can interact with structured datasets using:

* SQL queries
* CSV parsing

This enables the system to perform:

* data aggregation
* filtering
* statistical analysis
* business insights

Example:

```
SELECT product, SUM(sales)
FROM sales
GROUP BY product
ORDER BY SUM(sales) DESC
LIMIT 5;
```

---

## 5. File Reading and Writing

Agents can access files directly from the filesystem.

Supported operations:

* read `.txt` files
* parse `.csv` files
* write reports
* generate outputs

Example tasks:

* summarize documents
* analyze datasets
* generate reports

---

## 6. Local Search Engine

Agents can perform local information retrieval from files.

Example tasks:

* searching project documentation
* retrieving relevant content
* indexing text files

Possible implementations:

* keyword search
* BM25 retrieval
* embedding-based search

---

# ⚙️ System Architecture

The tool-calling architecture extends the previous **multi-agent orchestration system**.

```
User Query
     ↓
Orchestrator
     ↓
Task Planning
     ↓
Tool-Using Agents
 ┌───────────────┬───────────────┬───────────────┐
 │ Code Agent    │ DB Agent      │ File Agent    │
 │ Python Tools  │ SQL Queries   │ File System   │
 └───────────────┴───────────────┴───────────────┘
     ↓
Tool Execution
     ↓
Results Aggregation
     ↓
Final Answer
```

---

# 🧪 Exercise

## Build Tool-Using Agents

Implement **three specialized agents** that interact with system tools.

| Agent      | Tool                         |
| ---------- | ---------------------------- |
| Code Agent | Python execution             |
| DB Agent   | SQLite + SQL queries         |
| File Agent | Read/write `.txt` and `.csv` |

---

# 💡 Example Scenario

### User Request

```
Analyze sales.csv and generate top 5 insights
```

### System Execution

```
User Query
    ↓
Orchestrator
    ↓
File Agent → reads sales.csv
    ↓
Code Agent → analyzes dataset
    ↓
Analysis Agent → generates insights
    ↓
Final Output
```

### Expected Output

Example insights:

* Top performing product
* Highest revenue region
* Monthly growth trend
* Best sales channel
* Profit contribution by category

---

# 📂 Project Structure

```
project/
│
├── tools/
│   ├── code_executor.py
│   ├── db_agent.py
│   └── file_agent.py
│
├── data/
│   └── sales.csv
│
└── TOOL-CHAIN.md
```

---

# 📦 Deliverables

Students must implement the following components:

### 1. Code Execution Tool

```
/tools/code_executor.py
```

Responsibilities:

* execute Python code
* return execution output
* handle runtime errors safely

---

### 2. Database Agent

```
/tools/db_agent.py
```

Responsibilities:

* connect to SQLite database
* execute SQL queries
* return structured results

---

### 3. File Agent

```
/tools/file_agent.py
```

Responsibilities:

* read `.txt` files
* read `.csv` datasets
* write output files

---

### 4. Tool Chain Documentation

```
TOOL-CHAIN.md
```

Should include:

* tool architecture
* execution flow
* agent responsibilities
* example use cases

---

# 🔄 End-to-End Workflow

```
User Query
   ↓
Orchestrator
   ↓
Task Decomposition
   ↓
Agent Selection
   ↓
Tool Execution
   ↓
Results Aggregation
   ↓
Final Response
```

---

# 🚀 Outcome

After completing Day 3, you will have built a **functional tool-calling agent system** capable of:

* executing Python code
* querying databases
* analyzing datasets
* reading and writing files
* generating insights automatically

This represents a major step toward **fully autonomous AI systems** capable of interacting with real environments.
