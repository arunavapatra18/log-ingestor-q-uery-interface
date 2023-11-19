import click
import requests

API_URL = "http://localhost:3000/search"

@click.command()
@click.option('-q', '--query', help='Search query string.')
@click.option('-l', '--level', help='Log level.')
@click.option('-m', '--message', help='Log message.')
@click.option('-ri', '--resource-id', help='Resource ID.')
@click.option('-t', '--timestamp', help='Log timestamp.')
@click.option('-tr', '--trace-id', help='Trace ID.')
@click.option('-s', '--span-id', help='Span ID.')
@click.option('-c', '--commit', help='Git commit hash.')
@click.option('-p', '--parent-resource-id', help='Parent resource ID.')
def seacrh(
    query, 
    level,
    message,
    resource_id,
    timestamp,
    trace_id,
    span_id,
    commit,
    parent_resource_id
):
    """
    Function to search and filter logs from CLI
    """
    params = {}
    
    if query:
        params['query'] = query
    if level:
        params['level'] = level
    if message:
        params['message'] = message
    if resource_id:
        params['resource_id'] = resource_id
    if timestamp:
        params['timestamp'] = timestamp
    if trace_id:
        params['trace'] = trace_id
    if span_id:
        params['span_id'] = span_id
    if commit:
        params['commit'] = commit
    if parent_resource_id:
        params['metadata.parentResourceId'] = parent_resource_id
        
    response = requests.get(API_URL, params=params)
    data = response.json()
    
    click.echo("Search Results:")
    for result in data:
        click.echo(f"{result}\n")

if __name__ == '__main__':
    seacrh()