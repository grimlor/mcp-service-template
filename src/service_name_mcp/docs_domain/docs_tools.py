"""
Documentation Tools for {{Service Name}} MCP Server

This module provides tools for searching and retrieving documentation from
various sources like Git repositories, file systems, documentation platforms,
or content management systems.

To customize for your service:
1. Update DEFAULT_* constants with your documentation source details
2. Implement your specific document search and retrieval logic
3. Update tool descriptions to reflect your documentation structure
4. Customize search syntax and capabilities for your needs
"""

from typing import Any

from service_name_mcp.common.logging import logger
from service_name_mcp.mcp_instance import mcp

# TODO: Update these constants for your documentation source
DEFAULT_ORGANIZATION = "your_org"
DEFAULT_PROJECT = "your_project"
DEFAULT_REPOSITORY = "your_docs_repo"
DEFAULT_PATH = "/docs/{{service_name}}/"


@mcp.tool(
    description=f"""Search the {{service_name}} documentation for relevant content using advanced text search.

    This tool performs a comprehensive full-text search across all {{service_name}} documentation files including:
    - Domain concepts, definitions, and business logic
    - Data model schemas, table structures, and field descriptions
    - API documentation and technical specifications
    - Process documentation, metrics calculations, and business rules
    - Best practices and implementation guides

    SEARCH SYNTAX & BEST PRACTICES:

    1. **Simple Keywords**: Use specific terms related to your analysis
       - Examples: "data model", "authentication"

    2. **Boolean Operators** (must be UPPERCASE):
       - AND: "schema AND validation" (finds documents with both terms)
       - OR: "API OR endpoint" (finds documents with either term)
       - NOT: "config NOT deprecated" (excludes documents with 'deprecated')
       - Parentheses: "(schema OR model) AND validation"

    3. **Wildcards**:
       - * for multiple characters: "config*" finds config, configuration, configure
       - ? for single character: "set?" finds sets, setup

    4. **Start Broad, Then Narrow**: Begin with general terms, then use more specific searches

    🚨 CRITICAL REQUIREMENT - FETCH ALL PAGES:
    This search tool ONLY returns content snippets for discovery purposes. These snippets are
    INCOMPLETE and INSUFFICIENT for answering user questions. You MUST fetch the complete
    content of EVERY SINGLE relevant page using fetch_documentation_page().

    ❌ NEVER answer questions based only on search snippets
    ✅ ALWAYS fetch ALL relevant pages before providing answers

    MANDATORY WORKFLOW - NO EXCEPTIONS:
    1. Use this search tool to discover relevant documentation pages
    2. Examine ALL search results and identify EVERY unique file path that contains relevant information
    3. Call fetch_documentation_page() for EACH AND EVERY identified file path - do not skip any
    4. Only after fetching ALL relevant pages, provide comprehensive answers using the complete documentation

    If search returns multiple pages (e.g., /concepts/overview.md AND /api/endpoints.md),
    you MUST fetch BOTH pages, not just one. Each page may contain different aspects of the answer.

    Search covers markdown files and documentation under '{DEFAULT_PATH}' by default.
    Results include file paths and content snippets for identifying which pages to fetch."""
)
def search_documentation(
    search_text: str, path_filter: str | None = DEFAULT_PATH, max_results: int = 100
) -> list[dict[str, Any]]:
    """
    Search documentation for relevant content.

    Args:
        search_text: Search query using keywords, phrases, boolean operators, or wildcards
        path_filter: Optional path prefix to filter results
        max_results: Maximum number of results to return

    Returns:
        List of search results with file paths and content snippets
    """
    try:
        if path_filter:
            logger.info(f"Filtering by path prefix: {path_filter}")

        # TODO: Implement your documentation search logic
        # This could be:
        # - Git repository search APIs (GitHub, GitLab, etc.)
        # - Documentation platform APIs (GitBook, Confluence, etc.)
        # - Full-text search engines (Elasticsearch, Solr, etc.)
        # - Content management system APIs
        # - File system search with indexing
        # - Custom document indexing service

        logger.info(f"Searching documentation for: {search_text}")

        # Mock response for template
        mock_results = [
            {
                "fileName": "concepts/overview.md",
                "path": f"{DEFAULT_PATH}concepts/overview.md",
                "contentSnippet": "Overview of {{service_name}} concepts and architecture...",
                "score": 95,
            },
            {
                "fileName": "api/endpoints.md",
                "path": f"{DEFAULT_PATH}api/endpoints.md",
                "contentSnippet": "API endpoints for {{service_name}} integration...",
                "score": 88,
            },
            {
                "fileName": "best-practices.md",
                "path": f"{DEFAULT_PATH}best-practices.md",
                "contentSnippet": "Best practices for using {{service_name}}...",
                "score": 82,
            },
        ]

        # Filter mock results based on search text (basic simulation)
        filtered_results = [
            result
            for result in mock_results
            if any(term.lower() in str(result["contentSnippet"]).lower() for term in search_text.split())
        ]

        logger.info(f"Search completed successfully. Found {len(filtered_results)} results")

        return filtered_results[:max_results]

    except Exception as e:
        logger.error(f"Error in search_documentation: {e}")
        raise


@mcp.tool(
    description=f"""Fetch the complete content of a specific {{service_name}} documentation page.

    🚨 MANDATORY USAGE: This tool MUST be called for EVERY SINGLE relevant page identified
    through search_documentation. Search results only provide incomplete snippets -
    you need the complete page content to provide accurate, comprehensive answers.

    ❌ COMMON MISTAKE: Only fetching the first page from search results
    ✅ CORRECT APPROACH: Fetch ALL pages that appear in search results and contain relevant information

    WHEN TO USE:
    - After search_documentation identifies relevant pages
    - For EVERY SINGLE file path that appears relevant to the user's question
    - When you need complete context, definitions, examples, or detailed explanations
    - Before providing any detailed analysis or answers about {{service_name}} concepts

    EXAMPLE: If search returns both:
    - /docs/{{service_name}}/concepts/overview.md
    - /docs/{{service_name}}/api/endpoints.md

    You MUST fetch BOTH pages, not just one. Each may contain different essential information.

    The tool retrieves pages from the '{DEFAULT_REPOSITORY}' documentation repository.
    File paths should be relative to the repository root and typically start with
    '/docs/{{service_name}}/'.

    Common page types include:
    - Concept guides (e.g., overview.md, architecture.md)
    - API documentation (endpoints.md, authentication.md)
    - Technical references and specifications
    - Process and workflow documentation

    REQUIRED WORKFLOW - NO SHORTCUTS:
    1. First search: search_documentation("your search terms")
    2. Identify ALL unique file paths from search results (not just the first one)
    3. Fetch EVERY SINGLE page: fetch_documentation_page("/path/to/each/relevant/file.md")
    4. Only then provide comprehensive answers based on complete documentation from ALL pages

    Do not skip fetching any pages - search snippets alone are insufficient for accurate analysis."""
)
def fetch_documentation_page(file_path: str) -> str:
    """
    Fetch the complete content of a documentation page.

    Args:
        file_path: Relative path to the documentation file

    Returns:
        Complete content of the documentation page
    """
    try:
        logger.info(f"Fetching documentation file: {file_path}")

        # TODO: Implement your documentation retrieval logic
        # This could be:
        # - Git repository APIs to fetch file content (GitHub, GitLab, etc.)
        # - Documentation platform REST APIs
        # - Direct file system access
        # - Cloud storage APIs (various providers)
        # - Content management system APIs
        # - Custom document management system API

        # Mock response for template
        mock_content = f"""# {{Service Name}} Documentation

This is a mock documentation page for the template.

**File Path**: {file_path}

## Overview
This page would contain the complete documentation content for your service.

## Implementation Required
To make this functional, you need to:

1. **Choose Your Documentation Source**:
   - Git repositories (GitHub, GitLab, Bitbucket, etc.)
   - Documentation platforms (GitBook, Confluence, Notion, etc.)
   - File system with indexing
   - Cloud storage solutions
   - Wiki or documentation platforms

2. **Implement Search Logic**:
   - Full-text search capabilities
   - Boolean operators and wildcards
   - Path filtering and scoping
   - Result ranking and relevance

3. **Implement Content Retrieval**:
   - File/page content fetching
   - Authentication and authorization
   - Caching for performance
   - Error handling and retries

## Example Content Structure
Your documentation might include:
- API endpoints and specifications
- Configuration guides
- Best practices and tutorials
- Data models and schemas
- Troubleshooting guides

## Next Steps
1. Update the `docs_tools.py` file with your implementation
2. Configure authentication for your documentation source
3. Test search and retrieval functionality
4. Add domain-specific documentation categories

---
*This is a template file. Replace with your actual documentation content.*"""

        logger.info(f"Successfully fetched file: {file_path}")
        return mock_content

    except Exception as e:
        logger.error(f"Error fetching documentation file '{file_path}': {e}")
        raise
