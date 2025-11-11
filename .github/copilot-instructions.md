# Copilot Project Instructions: org-mcp-demo

Purpose: This repo is a reference + examples for configuring organization-level GitHub Copilot custom agents that integrate with the Neo4j MCP Cypher Server. It does NOT contain runnable agent code; actual agents live in the private org repo `.github-private`.

## Big Picture
- Two execution modes for the Neo4j MCP server are illustrated: Docker (`docker run mcp/neo4j-cypher:latest`) vs local Python (`mcp-neo4j-cypher`).
- Agents consume Neo4j via MCP tools: schema introspection (`get_neo4j_schema`), read (`read_neo4j_cypher`), write (`write_neo4j_cypher`). Generated clients emphasize Pydantic models, repository pattern, parameterized Cypher, and minimal CRUD.
- Environment variable strategy: Org-level + repository-level environment named `copilot` both define identical `COPILOT_MCP_*` variables to ensure availability inside agent execution.

## Key Files & Their Roles
- `README.md` – Architectural rationale, org-level setup requirements, workflow testing steps, environment variable duplication pattern.
- `org-setup-files/agents/neo4j-docker-client-generator.md` – Example agent invoking MCP server through Docker; shows YAML front matter with `command: docker` and explicit `-e VAR` flags in `args`.
- `org-setup-files/agents/neo4j-local-client-generator.md` – Example agent using direct Python command `mcp-neo4j-cypher` with `--transport stdio` and `--namespace` arguments.
- `sample-mcp-config/neo4j-mcp-docker-config.json` – JSON form of Docker-based MCP server config; embeds env mapping and explicit container arguments.
- `sample-mcp-config/neo4j-mcp-local-config.json` – JSON form of local Python MCP server config; simpler argument list.

## Conventions & Patterns
- Agent definition front matter: `name`, `description`, `tools`, then `mcp-servers` block with per-server `type`, `command`, `args`, `env`, `tools`.
- All Neo4j connection variables are referenced indirectly: `${COPILOT_MCP_NEO4J_*}` in agent Markdown OR plain `COPILOT_MCP_NEO4J_*` in JSON `env` values.
- Use namespace pattern: `neo4j-local` or `neo4j-python` to scope tools; transported via `NEO4J_NAMESPACE` or `--namespace`.
- Tools wildcard: `tools: ["*"]` grants full MCP server tool surface; narrow only if necessary.
- Query safety: ALWAYS parameterize Cypher; never interpolate strings or f-strings (reinforced in agent instructions). Favor `MERGE` to avoid duplication.

## Editing / Extending
- To add a new execution mode, copy one of the samples and adjust: `command` (e.g., switch to a different container tag) and `args`; retain env indirection.
- When introducing new Neo4j features (indexes, constraints) reflect them in generated client models by re-running schema introspection first.
- Keep agent instructions focused on minimal, extendable client code (avoid async, logging, complex retries unless explicitly requested).

## Environment & Secrets
Required variables (both org-level + repo `copilot` environment):
- `COPILOT_MCP_NEO4J_URI`, `COPILOT_MCP_NEO4J_USERNAME`, `COPILOT_MCP_NEO4J_PASSWORD`, `COPILOT_MCP_NEO4J_DATABASE`
Prefix `COPILOT_MCP_` is mandatory for exposure to MCP-integrated agents.

## Working With MCP Config JSON
Structure (example, Docker):
```jsonc
{
  "mcpServers": {
    "neo4j-local": {
      "type": "local",
      "command": "docker",
      "args": ["run", "-i", "--rm", "-e", "NEO4J_URI=$NEO4J_URI", ...],
      "tools": ["*"],
      "env": {
        "NEO4J_URI": "COPILOT_MCP_NEO4J_URI",
        "NEO4J_USERNAME": "COPILOT_MCP_NEO4J_USERNAME"
      }
    }
  }
}
```
Adjust only: container image tag, namespace, additional `-e` flags for new variables.

## Common Pitfalls
- Defining variables only at org level (must also exist in repo `copilot` environment).
- Attempting MCP integration in a non-`.github-private` repository (won't expose server tools to agents).
- Removing `--transport stdio` (breaks MCP protocol handshake for local Python mode).
- Forgetting to set `NEO4J_NAMESPACE` (tool names may collide or be unclear).

## Quick Checklist for New Agent
1. Front matter includes `mcp-servers` block with proper `namespace` & transport.
2. All `env` entries reference `COPILOT_MCP_*` variable names (no raw credentials).
3. Tool list includes only what you need (start with `"*"`, restrict later).
4. Instructions emphasize: Pydantic models, repository CRUD, parameterized Cypher.
5. Test schema introspection early to align generated code with live DB.

## Feedback
If any section is unclear (e.g., expanding test workflow, adding multi-database support), let me know what to refine and I'll iterate.
