"""
REST API Integration Tools

This domain demonstrates integration with REST APIs using free, public APIs
that anyone can access for learning purposes. No API keys required for basic usage.

Key Patterns Demonstrated:
- HTTP client management with requests library
- Response handling and error management
- Data transformation and formatting
- Rate limiting and retry logic
- Caching patterns for API responses
"""

from datetime import datetime
from typing import Any

import requests

# from ..common.config import Config  # TODO: Remove if not using config
from ..common.logging import get_logger
from ..mcp_instance import mcp

logger = get_logger(__name__)

# Global session for connection reuse
_session = None


def get_http_session() -> requests.Session:
    """Get cached HTTP session with default configuration"""
    global _session
    if _session is None:
        _session = requests.Session()
        _session.headers.update(
            {"User-Agent": "MCP-Service-Template/1.0", "Accept": "application/json", "Content-Type": "application/json"}
        )
        logger.info("Created new HTTP session")

    return _session


@mcp.tool(description="Get current weather data from a free weather API")
def get_weather_data(city: str, country_code: str | None = None, units: str = "metric") -> dict[str, Any]:
    """
    Get current weather data for a city using OpenWeatherMap free API.

    Args:
        city: Name of the city
        country_code: Two-letter country code (optional)
        units: Temperature units (metric, imperial, kelvin)

    Returns:
        Dictionary containing weather data and metadata
    """
    try:
        session = get_http_session()

        # Build location string
        location = city
        if country_code:
            location += f",{country_code}"

        # Use OpenWeatherMap free API (requires API key for full access)
        # For demo purposes, we'll use a weather API that doesn't require keys
        # or return mock data to demonstrate the pattern

        # Alternative: Use wttr.in which provides free weather data
        url = f"https://wttr.in/{location}"
        params = {
            "format": "j1",  # JSON format
            "lang": "en",
        }

        response = session.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Extract and format key weather information
        current = data.get("current_condition", [{}])[0]
        weather_data = {
            "location": {"city": city, "country_code": country_code, "query": location},
            "current": {
                "temperature": current.get("temp_C", "N/A"),
                "temperature_f": current.get("temp_F", "N/A"),
                "description": current.get("weatherDesc", [{}])[0].get("value", "N/A"),
                "humidity": current.get("humidity", "N/A"),
                "wind_speed": current.get("windspeedKmph", "N/A"),
                "wind_direction": current.get("winddir16Point", "N/A"),
                "feels_like": current.get("FeelsLikeC", "N/A"),
                "visibility": current.get("visibility", "N/A"),
            },
            "metadata": {
                "source": "wttr.in",
                "timestamp": datetime.now().isoformat(),
                "units": "metric" if units == "metric" else "imperial",
            },
        }

        logger.info(f"Retrieved weather data for {location}")
        return weather_data

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request error: {str(e)}")
        return {
            "error": f"Failed to fetch weather data: {str(e)}",
            "location": location,
            "suggestion": "Check internet connection and city name",
        }
    except Exception as e:
        logger.error(f"Unexpected error fetching weather data: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}", "location": location}


@mcp.tool(description="Get random quotes or facts from free APIs")
def get_random_content(content_type: str = "quote") -> dict[str, Any]:
    """
    Get random content from various free APIs.

    Args:
        content_type: Type of content to fetch (quote, fact, joke, advice)

    Returns:
        Dictionary containing random content and metadata
    """
    try:
        session = get_http_session()

        if content_type == "quote":
            # Use quotable.io for quotes
            url = "https://api.quotable.io/random"
            response = session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                "type": "quote",
                "content": data.get("content", ""),
                "author": data.get("author", "Unknown"),
                "tags": data.get("tags", []),
                "length": data.get("length", 0),
                "source": "quotable.io",
                "timestamp": datetime.now().isoformat(),
            }

        elif content_type == "fact":
            # Use uselessfacts.jsph.pl for facts
            url = "https://uselessfacts.jsph.pl/random.json?language=en"
            response = session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                "type": "fact",
                "content": data.get("text", ""),
                "source": data.get("source", ""),
                "source_url": data.get("source_url", ""),
                "language": data.get("language", "en"),
                "permalink": data.get("permalink", ""),
                "api_source": "uselessfacts.jsph.pl",
                "timestamp": datetime.now().isoformat(),
            }

        elif content_type == "joke":
            # Use official-joke-api for jokes
            url = "https://official-joke-api.appspot.com/random_joke"
            response = session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                "type": "joke",
                "setup": data.get("setup", ""),
                "punchline": data.get("punchline", ""),
                "joke_type": data.get("type", "general"),
                "id": data.get("id", ""),
                "source": "official-joke-api.appspot.com",
                "timestamp": datetime.now().isoformat(),
            }

        elif content_type == "advice":
            # Use adviceslip.com for advice
            url = "https://api.adviceslip.com/advice"
            response = session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            slip = data.get("slip", {})
            return {
                "type": "advice",
                "content": slip.get("advice", ""),
                "advice_id": slip.get("id", ""),
                "source": "adviceslip.com",
                "timestamp": datetime.now().isoformat(),
            }

        else:
            return {
                "error": f"Unknown content type: {content_type}",
                "supported_types": ["quote", "fact", "joke", "advice"],
            }

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request error: {str(e)}")
        return {
            "error": f"Failed to fetch {content_type}: {str(e)}",
            "suggestion": "Check internet connection and try again",
        }
    except Exception as e:
        logger.error(f"Unexpected error fetching {content_type}: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}


@mcp.tool(description="Get information about countries using REST Countries API")
def get_country_info(country: str, info_type: str = "basic") -> dict[str, Any]:
    """
    Get detailed information about a country using the REST Countries API.

    Args:
        country: Country name, code, or capital city
        info_type: Type of info to return (basic, detailed, currency, languages)

    Returns:
        Dictionary containing country information
    """
    try:
        session = get_http_session()

        # REST Countries API - free and doesn't require API key
        base_url = "https://restcountries.com/v3.1"

        # Try different search methods
        search_urls = [f"{base_url}/name/{country}", f"{base_url}/alpha/{country}", f"{base_url}/capital/{country}"]

        data = None
        for url in search_urls:
            try:
                response = session.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    break
            except Exception:
                continue

        if not data:
            return {
                "error": f"Country '{country}' not found",
                "suggestion": "Try using the official country name, 2-letter code, or capital city",
            }

        # Get the first country from results
        country_data = data[0] if isinstance(data, list) else data

        # Extract information based on requested type
        if info_type == "basic":
            result = {
                "name": {
                    "common": country_data.get("name", {}).get("common", ""),
                    "official": country_data.get("name", {}).get("official", ""),
                },
                "capital": country_data.get("capital", []),
                "region": country_data.get("region", ""),
                "subregion": country_data.get("subregion", ""),
                "population": country_data.get("population", 0),
                "area": country_data.get("area", 0),
                "flag": country_data.get("flag", ""),
                "codes": {"iso2": country_data.get("cca2", ""), "iso3": country_data.get("cca3", "")},
            }
        elif info_type == "detailed":
            result = {
                "basic_info": {
                    "name": country_data.get("name", {}),
                    "capital": country_data.get("capital", []),
                    "region": country_data.get("region", ""),
                    "subregion": country_data.get("subregion", ""),
                    "population": country_data.get("population", 0),
                    "area": country_data.get("area", 0),
                },
                "geography": {
                    "coordinates": country_data.get("latlng", []),
                    "landlocked": country_data.get("landlocked", False),
                    "borders": country_data.get("borders", []),
                    "timezones": country_data.get("timezones", []),
                },
                "identity": {
                    "flag": country_data.get("flag", ""),
                    "coat_of_arms": country_data.get("coatOfArms", {}),
                    "codes": {
                        "iso2": country_data.get("cca2", ""),
                        "iso3": country_data.get("cca3", ""),
                        "numeric": country_data.get("ccn3", ""),
                    },
                },
            }
        elif info_type == "currency":
            currencies = country_data.get("currencies", {})
            result = {
                "country": country_data.get("name", {}).get("common", ""),
                "currencies": {
                    code: {"name": info.get("name", ""), "symbol": info.get("symbol", "")}
                    for code, info in currencies.items()
                },
            }
        elif info_type == "languages":
            result = {
                "country": country_data.get("name", {}).get("common", ""),
                "languages": country_data.get("languages", {}),
                "language_count": len(country_data.get("languages", {})),
            }
        else:
            return {
                "error": f"Unknown info type: {info_type}",
                "supported_types": ["basic", "detailed", "currency", "languages"],
            }

        result["metadata"] = {
            "source": "restcountries.com",
            "timestamp": datetime.now().isoformat(),
            "query": country,
            "info_type": info_type,
        }

        logger.info(f"Retrieved {info_type} info for country: {country}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request error: {str(e)}")
        return {"error": f"Failed to fetch country info: {str(e)}", "country": country}
    except Exception as e:
        logger.error(f"Unexpected error fetching country info: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}


@mcp.tool(description="Get JSON placeholder data for testing and development")
def get_placeholder_data(resource: str = "posts", item_id: int | None = None, limit: int = 10) -> dict[str, Any]:
    """
    Get placeholder data from JSONPlaceholder for testing purposes.

    Args:
        resource: Type of resource (posts, comments, albums, photos, todos, users)
        item_id: Specific item ID to fetch (optional)
        limit: Maximum number of items to return when fetching collections

    Returns:
        Dictionary containing placeholder data
    """
    try:
        session = get_http_session()

        # JSONPlaceholder API - free fake REST API for testing
        base_url = "https://jsonplaceholder.typicode.com"

        # Validate resource type
        valid_resources = ["posts", "comments", "albums", "photos", "todos", "users"]
        if resource not in valid_resources:
            return {"error": f"Invalid resource: {resource}", "valid_resources": valid_resources}

        # Build URL
        if item_id:
            url = f"{base_url}/{resource}/{item_id}"
        else:
            url = f"{base_url}/{resource}"

        response = session.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Apply limit for collections
        if isinstance(data, list) and not item_id:
            data = data[:limit]

        result = {
            "resource": resource,
            "data": data,
            "count": len(data) if isinstance(data, list) else 1,
            "metadata": {
                "source": "jsonplaceholder.typicode.com",
                "timestamp": datetime.now().isoformat(),
                "item_id": item_id,
                "limit_applied": limit if isinstance(data, list) and not item_id else None,
            },
        }

        logger.info(f"Retrieved placeholder data for {resource}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request error: {str(e)}")
        return {"error": f"Failed to fetch placeholder data: {str(e)}", "resource": resource}
    except Exception as e:
        logger.error(f"Unexpected error fetching placeholder data: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}


@mcp.tool(description="Make custom HTTP request to any public API")
def make_http_request(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    timeout: int = 30,
) -> dict[str, Any]:
    """
    Make a custom HTTP request to any public API.

    Args:
        url: URL to make request to
        method: HTTP method (GET, POST, PUT, DELETE, etc.)
        headers: Additional headers to send
        params: URL parameters
        data: Request body data (for POST, PUT, etc.)
        timeout: Request timeout in seconds

    Returns:
        Dictionary containing response data and metadata
    """
    try:
        session = get_http_session()

        # Validate method
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"]
        if method.upper() not in valid_methods:
            return {"error": f"Invalid HTTP method: {method}", "valid_methods": valid_methods}

        # Prepare request arguments
        request_kwargs: dict[str, Any] = {
            "timeout": min(timeout, 60)  # Cap at 60 seconds
        }

        if headers:
            # Merge with session headers
            request_kwargs["headers"] = {**session.headers, **headers}

        if params:
            request_kwargs["params"] = params

        if data and method.upper() in ["POST", "PUT", "PATCH"]:
            request_kwargs["json"] = data

        # Make request
        response = session.request(method.upper(), url, **request_kwargs)

        # Prepare result
        result: dict[str, Any] = {
            "request": {
                "url": url,
                "method": method.upper(),
                "headers": dict(response.request.headers),
                "params": params,
                "data": data,
            },
            "response": {
                "status_code": response.status_code,
                "status": "success" if response.ok else "error",
                "headers": dict(response.headers),
                "encoding": response.encoding,
                "size_bytes": len(response.content),
            },
            "metadata": {"timestamp": datetime.now().isoformat(), "elapsed_seconds": response.elapsed.total_seconds()},
        }

        # Add response content
        try:
            # Try to parse as JSON
            result["response"]["data"] = response.json()
            result["response"]["content_type"] = "json"
        except Exception:
            # Fall back to text
            result["response"]["data"] = response.text
            result["response"]["content_type"] = "text"

        if not response.ok:
            result["error"] = f"HTTP {response.status_code}: {response.reason}"

        logger.info(f"Made {method} request to {url}, status: {response.status_code}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request error: {str(e)}")
        return {"error": f"Request failed: {str(e)}", "request": {"url": url, "method": method}}
    except Exception as e:
        logger.error(f"Unexpected error making HTTP request: {str(e)}")
        return {"error": f"Unexpected error: {str(e)}"}
