"""Literature Search Index Module.

This module handles the creation and management of the Azure AI Search index
for scientific literature. It defines the schema and provides utilities for
index management.
"""

from typing import List, Optional
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SimpleField,
    SearchableField,
    SearchFieldDataType
)
from azure.core.credentials import AzureKeyCredential

def create_literature_index(
    client: SearchIndexClient,
    index_name: str = "literature-index"
) -> SearchIndex:
    """Create the literature search index.
    
    Args:
        client: Azure Search Index client
        index_name: Name for the search index
        
    Returns:
        Created SearchIndex instance
    """
    # Define index fields
    fields = [
        SimpleField(
            name="DocumentID",
            type=SearchFieldDataType.String,
            key=True
        ),
        SearchableField(
            name="Title",
            type=SearchFieldDataType.String,
            analyzer_name="standard.lucene"
        ),
        SearchableField(
            name="Abstract",
            type=SearchFieldDataType.String,
            analyzer_name="standard.lucene"
        ),
        SearchableField(
            name="Authors",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            analyzer_name="standard.lucene"
        ),
        SimpleField(
            name="PublicationDate",
            type=SearchFieldDataType.DateTimeOffset,
            sortable=True,
            filterable=True
        ),
        SearchableField(
            name="Keywords",
            type=SearchFieldDataType.Collection(SearchFieldDataType.String),
            analyzer_name="standard.lucene",
            filterable=True,
            facetable=True
        ),
        SearchableField(
            name="FullText",
            type=SearchFieldDataType.String,
            analyzer_name="standard.lucene"
        ),
        SimpleField(
            name="DOI",
            type=SearchFieldDataType.String,
            filterable=True
        ),
        SimpleField(
            name="Journal",
            type=SearchFieldDataType.String,
            filterable=True,
            facetable=True
        )
    ]
    
    # Create index definition
    index = SearchIndex(
        name=index_name,
        fields=fields
    )
    
    # Create or update index
    existing_indexes = list(client.list_indexes())
    for idx in existing_indexes:
        if getattr(idx, 'name', None) == index_name:
            client.delete_index(index_name)
            break
    
    # Create new index
    result = client.create_index(index)
    return result
