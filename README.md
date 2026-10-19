# Mirror tool extension example

A tiny [Mirror](https://github.com/reflection-oss/mirror) extension that gives the
agent a callable `word_count` tool. No MCP server, API keys, network requests,
or changes to Mirror itself. The implementation is entirely in
[`extension.py`](extension.py).

Tested with the public **`reflection-mirror==0.1.0`** package and Python 3.12.

## Install and enable

Install Mirror using [uv](https://docs.astral.sh/uv/):

```sh
uv tool install reflection-mirror
mirror
```

Review this repository's code, then enter this command **inside Mirror**:

```text
/extensions-add https://github.com/reflection-oss/mirror-example-tool-extension
```

Mirror downloads the repository and asks for consent. Select **Enable**.
Use `/extensions` to check or toggle enablement, `/extensions-update` to update,
and `/extensions-remove` to remove the source. Git must be installed. Updates
are explicit; Mirror does not install extension dependencies automatically.

**Trust boundary:** extensions execute unsandboxed Python locally with your
account's filesystem, network, and credential access. Only enable reviewed code
you trust. This particular tool only processes the supplied text.

## Use

Ask Mirror:

> Use the word_count tool to count "Hello, Mirror!".

The model-facing tool is `mirror-example-tool-extension__word_count`:

```json
{"text": "Hello, Mirror!"}
```

Result:

```json
{"words": 2, "characters": 14}
```

Words are separated by whitespace; characters are Unicode code points, not
bytes or displayed grapheme clusters. Input is limited to 10,000 characters.

## Make your own tool

- `ToolExtension.tools(context)` returns objects implementing `HostTool`.
- `ToolDefinition` supplies the local name, description, and JSON Schema.
- `async execute(arguments, context)` receives JSON text and returns a
  `ToolResult(content=..., success=...)`. Validate arguments in the handler too.
- Mirror prefixes tool names with `<extension-id>__`; do not add that prefix
  yourself. Keep `extension.py` at the repository root and `id()` equal to the
  lowercase repository name. Change the ID when copying this example to a new repo.
- This pure computation sets `needs_approval=False`. Keep the default `True`
  for tools that need per-call approval; extension consent is separate.

To wrap your preferred external service, replace the counting logic with an
async request and adapt the schema/result. Use bounded timeouts, preserve
`asyncio.CancelledError`, and keep secrets out of arguments, descriptions,
results, and logs. Any data sent to the service leaves your machine. No external
service integration or automatic fallback is implemented here.

See Mirror's [extension guide](https://github.com/reflection-oss/mirror/blob/main/mirror-cli/docs/extensions.md).

## License

Copyright 2026 Reflection AI. [Apache-2.0](LICENSE), like Mirror.
