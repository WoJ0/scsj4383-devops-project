# SCSJ4383 DevOps Demo (Part A)

Sample Java service used to demonstrate the full DevOps pipeline for **Software
Construction Project 1, Part A**: Jira → GitHub → Jenkins → JMeter → Docker Hub.

**Team:** Ara Azad, Yaran Akram, Hanar Rebwar, Hedi Jafar

## What it is

A tiny REST API built with **plain Java + Maven** (no external runtime
dependencies — it uses the JDK's built-in HTTP server). This keeps the Docker
image small and the build fast and reliable.

### Endpoints

| Method | Path | Example | Response |
|--------|------|---------|----------|
| GET | `/health` | `/health` | `{"status":"UP"}` |
| GET | `/api/add` | `/api/add?a=2&b=3` | `{"result":5}` |
| GET | `/api/subtract` | `/api/subtract?a=5&b=2` | `{"result":3}` |
| GET | `/api/multiply` | `/api/multiply?a=4&b=6` | `{"result":24}` |
| GET | `/api/divide` | `/api/divide?a=5&b=2` | `{"result":2.5}` |
| GET | `/api/prime` | `/api/prime?n=13` | `{"n":13,"prime":true}` |
| GET | `/api/fib` | `/api/fib?n=10` | `{"n":10,"fibonacci":55}` |

The app listens on **port 8081** (Jenkins uses 8080, so this avoids a clash).

## Build & run locally

```bash
# Build a runnable jar (runs unit tests too)
mvn clean package

# Run it
java -jar target/devops-demo.jar
# -> SCSJ4383 DevOps Demo started on http://localhost:8081

# Try it
curl "http://localhost:8081/api/add?a=2&b=3"
```

## Run the unit tests only

```bash
mvn test
```

## Build & run with Docker

```bash
docker build -t scsj4383-devops-demo .
docker run -p 8081:8081 scsj4383-devops-demo
```

## Performance test with JMeter

Start the app first, then:

```bash
jmeter -n -t jmeter/test-plan.jmx -l results.jtl -e -o jmeter-report
# open jmeter-report/index.html for the dashboard
```

## CI/CD

The `Jenkinsfile` defines the pipeline: Checkout → Build → Unit Test →
Performance Test (JMeter) → Docker Build & Push. See the project runbook for the
one-time Jenkins setup (plugins, tools, and credentials).
