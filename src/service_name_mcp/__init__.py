try:
    from importlib.metadata import version

    __version__ = version("mcp-service-template")
except Exception:
    __version__ = "0.1.0.dev0"
