from pathlib import Path

from mcp.server.fastmcp.prompts import base

from service_name_mcp.mcp_instance import mcp


def _load_prompt_content(prompt_file: str) -> str:
    """
    Load prompt content from markdown files.

    Args:
        prompt_file: Name of the prompt file to load

    Returns:
        Content of the prompt file
    """
    current_dir = Path(__file__).parent
    prompt_path = current_dir / "prompts" / prompt_file

    try:
        with open(prompt_path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: Could not find prompt file at {prompt_path}"
    except Exception as e:
        return f"Error loading prompt: {str(e)}"


@mcp.prompt()
def domain_analyst() -> list[base.Message]:
    """
    Expert Domain Analyst prompt for analyzing data using this service.

    Customize this prompt for your specific domain and use case.
    """
    return [
        base.UserMessage(_load_prompt_content("analyst_prompt.md")),
        base.AssistantMessage(
            "I'm ready to analyze your {{domain}} data! Here are some examples of what I can help with:\n\n"
            "📊 **Data Analysis** (metrics, trends, performance analysis)\n"
            "🔍 **Data Exploration** (queries, schemas, data sampling)\n"
            "🛠️ **Troubleshooting** (investigating issues, validating data)\n\n"
            "Feel free to ask me any questions or request any analysis you need!"
        ),
    ]


@mcp.prompt()
def report_issue() -> str:
    """
    Report issues and data quality problems in the system.

    Customize this for your specific issue tracking system.
    """
    return _load_prompt_content("report_bug_prompt.md")


@mcp.prompt()
def investigate_issue(issue_id: str) -> str:
    """
    Investigate a specific issue in the system by ID.

    Args:
        issue_id: Issue ID to investigate

    Customize this for your specific issue tracking system.
    """
    prompt_content = _load_prompt_content("investigate_bug_prompt.md")
    return f"Please investigate issue ID {issue_id} using the following instructions:\n\n{prompt_content}"
