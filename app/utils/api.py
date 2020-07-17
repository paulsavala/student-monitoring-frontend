

def resource_url(resource, api_base_url):
    return f'{api_base_url.rstrip("/")}/{resource.lstrip("/")}'
