

def resource_url(api_base_url, resource):
    return f'{api_base_url.rstrip("/")}/{resource.lstrip("/")}'
