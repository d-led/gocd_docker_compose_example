# GoCD Docker Compose Example

A minimal, working [GoCD](https://www.gocd.org/) v25.4.0 setup using **static XML configuration** that runs out of the box.

## Quick Start

```bash
cd static_config
docker-compose up -d
```

Access the UI at: [http://localhost:8153](http://localhost:8153)

The `dont-wait-forever` pipeline is pre-configured in [static_config/config/cruise-config.xml](static_config/config/cruise-config.xml) - it runs real Gradle tests from [this repo](https://github.com/d-led/dont_wait_forever_for_the_tests).

## Demo Contents

- **GoCD Server v25.4.0**: Pre-configured with a real Gradle test pipeline
- **2 Agents**: Alpine-based with OpenJDK 21 pre-installed
- **Static Configuration**: Pure XML config - no external repos, no setup scripts
- **Persistent Storage**: Volumes retain configuration across restarts

## Project Structure

```shell
static_config/
├── docker-compose.yaml      # Orchestration - server + 2 agents
├── Dockerfile.agent         # Custom Alpine agent with JDK 21
├── config/
│   └── cruise-config.xml    # Static pipeline configuration
└── .gitignore               # Ignores GoCD-generated files
```

## How It Works

The demo pipeline is defined directly in `config/cruise-config.xml`. When the server starts, it:

1. Mounts the config directory into the container
2. Reads the pipeline configuration
3. Agents auto-register and connect

No git repositories, no config repos, no setup scripts - just static XML that works.

## Common Commands

```bash
# View status
docker-compose ps

# Follow logs
docker-compose logs -f

# Stop everything
docker-compose down

# Full restart (clean volumes)
docker-compose down -v && docker-compose up -d
```

## Notes

- **Server**: Runs on [http://localhost:8153](http://localhost:8153)
- **Agent Key**: `123456789abcdef` (for auto-registration, for demo purposes only)
- **Volumes**: `godata` and `gohome` persist across restarts
- **JDK**: OpenJDK 21 pre-installed on Alpine-based agents
