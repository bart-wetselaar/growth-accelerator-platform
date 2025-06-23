# Services package for external API integrations

def init_services():
    """Initialize all services"""
    try:
        from .workable_api import workable_api
        return True
    except Exception as e:
        print(f"Service initialization error: {e}")
        return False