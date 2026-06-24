# ---- Stage 1: build the runnable jar with Maven ----
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /app
# Copy the build descriptor first to cache dependencies
COPY pom.xml .
RUN mvn -q -e -DskipTests dependency:go-offline || true
# Copy the source and package
COPY src ./src
RUN mvn -q -DskipTests package

# ---- Stage 2: tiny runtime image with just the jar ----
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /app/target/devops-demo.jar app.jar
# The demo HTTP service listens on 8081
ENV PORT=8081
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]
