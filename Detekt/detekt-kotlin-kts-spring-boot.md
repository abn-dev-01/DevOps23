Setting up Detekt for a Kotlin Spring Boot project involves a few steps, including adding the necessary dependencies, configuring the Detekt plugin, and creating a configuration file for custom rules. Here’s a step-by-step guide to configure Detekt in your Gradle Spring Boot project using Kotlin DSL:

### Step 1: Add Detekt Plugin and Dependencies

First, add the Detekt plugin and dependencies to your `build.gradle.kts` file.

```kotlin
plugins {
    id("org.springframework.boot") version "3.3.0"
    id("io.spring.dependency-management") version "1.1.5"
    id("org.jetbrains.kotlin.jvm") version "1.9.24"
    id("org.jetbrains.kotlin.plugin.spring") version "1.9.24"
    id("io.gitlab.arturbosch.detekt") version "1.23.1"
}

group = "pro.abnjava"
version = "0.0.1-SNAPSHOT"

java {
    toolchain {
        languageVersion.set(JavaLanguageVersion.of(17))
    }
}

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-actuator")
    implementation("org.springframework.boot:spring-boot-starter-hateoas")
    implementation("org.springframework.boot:spring-boot-starter-security")
    implementation("org.springframework.boot:spring-boot-starter-webflux")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")
    implementation("de.codecentric:spring-boot-admin-starter-client")
    implementation("de.codecentric:spring-boot-admin-starter-server")
    implementation("io.projectreactor.kotlin:reactor-kotlin-extensions")
    implementation("org.jetbrains.kotlin:kotlin-reflect")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-reactor")
    implementation("org.springframework.session:spring-session-core")
    compileOnly("org.projectlombok:lombok")
    developmentOnly("org.springframework.boot:spring-boot-devtools")
    developmentOnly("org.springframework.boot:spring-boot-docker-compose")
    runtimeOnly("org.postgresql:postgresql")
    annotationProcessor("org.springframework.boot:spring-boot-configuration-processor")
    annotationProcessor("org.projectlombok:lombok")
    testImplementation("org.springframework.boot:spring-boot-starter-test")
    testImplementation("io.projectreactor:reactor-test")
    testImplementation("org.jetbrains.kotlin:kotlin-test-junit5")
    testImplementation("org.springframework.restdocs:spring-restdocs-webtestclient")
    testImplementation("org.springframework.security:spring-security-test")
    testRuntimeOnly("org.junit.platform:junit-platform-launcher")
}

tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile> {
    kotlinOptions {
        freeCompilerArgs = listOf("-Xjsr305=strict")
    }
}
```

### Step 2: Configure Detekt

Next, configure Detekt in the same `build.gradle.kts` file.

```kotlin
detekt {
    toolVersion = "1.23.1"
    config = files("$rootDir/config/detekt/detekt.yml")
    buildUponDefaultConfig = true
    allRules = false
    ignoreFailures = false
    parallel = true
    reports {
        xml.required.set(true)
        html.required.set(true)
        txt.required.set(false)
        sarif.required.set(false)
    }
}

tasks.withType<Detekt>().configureEach {
    jvmTarget = "17"
}
```

### Step 3: Create Detekt Configuration File

Create a custom configuration file for Detekt at `config/detekt/detekt.yml`. You can use the default configuration as a starting point by copying it from the [Detekt GitHub repository](https://github.com/detekt/detekt/blob/main/config/detekt/detekt.yml).

Here’s a simple example:

```yaml
# config/detekt/detekt.yml

build:
  maxIssues: 0
  weights:
    complexity: 2
    LongParameterList: 1
    style: 1

comments:
  active: true
  CommentOverPrivateMethod: true

complexity:
  active: true
  LongParameterList:
    active: true
    threshold: 6

formatting:
  active: true
  android: false

performance:
  active: true
  ForEachOnRange:
    active: true

style:
  active: true
  MagicNumber:
    active: false
  OptionalUnit:
    active: true
```

### Step 4: Run Detekt

You can now run Detekt using Gradle. Here are some useful commands:

- To analyze your project with Detekt:
  ```sh
  ./gradlew detekt
  ```

- To generate a baseline (useful to exclude current issues and only focus on new ones):
  ```sh
  ./gradlew detektBaseline
  ```

- To check for code formatting issues (if you have the formatting plugin enabled):
  ```sh
  ./gradlew detektFormatting
  ```

### Step 5: (Optional) Integrate Detekt with CI

To integrate Detekt into your Continuous Integration (CI) pipeline, add the `./gradlew detekt` command to your CI configuration file (e.g., `.github/workflows/ci.yml` for GitHub Actions).

Here’s an example for GitHub Actions:

```yaml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up JDK 17
      uses: actions/setup-java@v2
      with:
        java-version: '17'
    - name: Build and Test
      run: ./gradlew build
    - name: Run Detekt
      run: ./gradlew detekt
```

By following these steps, you will have a fully configured Detekt setup for your Kotlin Spring Boot project, including custom rules, and integration with your build and CI processes.
