# SCSJ4383 / SCJ4383 — Software Construction · Project 1

**Team:** Ara Azad · Yaran Akram · Hanar Rebwar · Hedi Jafar

This repository contains both parts of Project 1.

## Part A — DevOps  (`part-a-app/`)

A small Java + Maven REST service used to demonstrate the full DevOps pipeline:
**Jira → GitHub → Jenkins → JMeter → Docker Hub**.

| File | Purpose |
|------|---------|
| `part-a-app/src/...` | The application source + JUnit tests |
| `part-a-app/pom.xml` | Maven build (produces a runnable jar) |
| `part-a-app/Jenkinsfile` | The CI/CD pipeline (build → test → JMeter → Docker push) |
| `part-a-app/Dockerfile` | Builds the Docker image |
| `part-a-app/jmeter/test-plan.jmx` | JMeter performance test plan |
| `part-a-app/README.md` | How to build, run, test, dockerize |

> Follow **`PartA_DevOps_Runbook.docx`** for the exact click-by-click steps to
> perform and record items 1–8, and add your screenshots to
> **`PartA_Presentation.pptx`**.

Quick start:

```bash
cd part-a-app
mvn clean package          # builds + runs unit tests
java -jar target/devops-demo.jar
curl "http://localhost:8081/api/add?a=2&b=3"
```

## Part B — Code Smells & Refactoring  (`part-b/`)

A standalone sales-report program in two versions, used to study code smells.

| File | Purpose |
|------|---------|
| `part-b/before/sales_report.py` | Original ("smelly") version |
| `part-b/after/sales_report.py` | Refactored ("clean") version |
| `part-b/test_equivalence.py` | Proves the refactor preserves behaviour (50 datasets) |
| `part-b/benchmark.py` | Performance comparison (bonus task) |
| `PartB_CodeSmells_and_Refactoring.pdf` | The full documentation deliverable |

Run it:

```bash
cd part-b
python test_equivalence.py     # PASS on 50 datasets
python benchmark.py            # ~106x faster after refactoring, identical output
```

**Result:** the refactoring removed 4 code smells and made the program about
**106× faster** (1641 ms → 15.5 ms) while producing identical output.
