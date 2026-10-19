"""Add a local word-count tool to Mirror. No credentials or network required."""

import json
from typing import override

from mirror.cli import extension, host_tools

_MAX_CHARACTERS = 10_000


class WordCountTool:
  """Count words locally, without file or network access."""

  definition: host_tools.ToolDefinition = host_tools.ToolDefinition(
    name='word_count',
    description='Count whitespace-separated words and Unicode code points.',
    parameters={
      'type': 'object',
      'properties': {
        'text': {'type': 'string', 'maxLength': _MAX_CHARACTERS},
      },
      'required': ['text'],
      'additionalProperties': False,
    },
    needs_approval=False,  # Pure computation; consent is still required.
  )

  async def execute(
    self,
    arguments: str,
    context: host_tools.ExecutionContext = host_tools.MODEL_CONTEXT,
  ) -> host_tools.ToolResult:
    """Validate the JSON arguments and return JSON text to the agent."""
    del context
    try:
      payload: object = json.loads(arguments)
    except json.JSONDecodeError:
      return host_tools.ToolResult('Invalid JSON.', success=False)
    if not isinstance(payload, dict) or set(payload) != {'text'}:
      return host_tools.ToolResult(
        'Expected only a "text" field.', success=False
      )
    text = payload['text']
    if not isinstance(text, str) or len(text) > _MAX_CHARACTERS:
      return host_tools.ToolResult(
        f'"text" must be a string of at most {_MAX_CHARACTERS} characters.',
        success=False,
      )
    return host_tools.ToolResult(
      json.dumps({'words': len(text.split()), 'characters': len(text)}),
      success=True,
    )


class ToolExtension(extension.Extension[None, None, None]):
  """Expose one tool through Mirror's extension API."""

  @classmethod
  @override
  def id(cls) -> str:
    return 'mirror-example-tool-extension'

  @override
  def tools(self, context: extension.Context) -> list[host_tools.HostTool]:
    del context
    return [WordCountTool()]
