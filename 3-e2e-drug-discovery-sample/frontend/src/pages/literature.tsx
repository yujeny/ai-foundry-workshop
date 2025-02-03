import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { api } from "../lib/api"
import type { SearchResponse } from "../types/api"

export function LiteraturePage() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState<SearchResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSearch = async () => {
    if (!query.trim()) {
      setError("Please enter a search query")
      return
    }

    setLoading(true)
    setError(null)
    try {
      const { data, error: apiError } = await api.searchLiterature(query)
      if (apiError) {
        throw new Error(apiError)
      }
      if (data) {
        setResults(data)
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to search literature")
      setResults(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1>Literature Search</h1>
        <p className="text-lg text-muted-foreground mt-2">
          Search and analyze scientific literature for drug discovery.
        </p>
      </div>

      {error && (
        <Card className="border-destructive">
          <CardContent className="p-6">
            <p className="text-center text-destructive">{error}</p>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Search</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="form-label">Search Query</label>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="form-input"
                placeholder="Enter keywords, topics, or research areas"
              />
            </div>
            <button 
              onClick={handleSearch} 
              disabled={loading || !query.trim()}
              className="button button-primary w-full"
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent"></div>
                  <span>Searching...</span>
                </div>
              ) : (
                'Search Literature'
              )}
            </button>
          </div>
        </CardContent>
      </Card>

      {results && (
        <div className="space-y-4">
          <h2>Search Results</h2>
          <div className="grid gap-4">
            {results.results.map((paper, index) => (
              <Card key={index}>
                <CardContent className="p-6">
                  <h3 className="font-medium mb-2">{paper.title}</h3>
                  <p className="text-sm text-muted-foreground mb-2">
                    {paper.authors.join(", ")} • {paper.publicationDate}
                  </p>
                  <p className="text-muted-foreground mb-2">{paper.abstract}</p>
                  {paper.doi && (
                    <a
                      href={`https://doi.org/${paper.doi}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm text-primary hover:underline"
                    >
                      DOI: {paper.doi}
                    </a>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
          <div className="flex justify-between items-center text-sm text-muted-foreground">
            <span>Showing {results.results.length} of {results.totalResults} results</span>
            <span>Page {results.page} of {Math.ceil(results.totalResults / results.pageSize)}</span>
          </div>
        </div>
      )}
    </div>
  )
}
