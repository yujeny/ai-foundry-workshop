import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { searchLiterature } from "../lib/api"
import type { MedicationInfo, MedicationAnalysis } from "../types/api"

export function AnalysisPage() {
  const [medicationData, setMedicationData] = useState<MedicationInfo>({
    name: '',
    notes: '',
  })
  const [analysis, setAnalysis] = useState<MedicationAnalysis | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyze = async () => {
    if (!medicationData.name) {
      setError("Please enter a medication name")
      return
    }

    setLoading(true)
    setError(null)
    try {
      const response = await searchLiterature(medicationData.name)
      const data = response.data
      if (!data) {
        throw new Error('No data returned from search')
      }
      setAnalysis({
        structured_info: {
          category: data.category || 'Unknown',
          risk_rating: data.risk_rating || 'Unknown',
          common_side_effects: data.side_effects || [],
          interactions: data.interactions || []
        },
        ai_explanation: response.summary || '',
        disclaimer: 'This analysis is provided for informational purposes only.'
      })
    } catch (error) {
      console.error('Analysis error:', error)
      setError(error instanceof Error ? error.message : "Failed to analyze medication. Please try again.")
      setAnalysis(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1>Medication Info Summaries</h1>
        <p className="text-lg text-muted-foreground mt-2">
          Get comprehensive medication information and analysis powered by AI.
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
          <CardTitle>Medication Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label htmlFor="medication-name" className="form-label">Medication Name</label>
              <input
                id="medication-name"
                type="text"
                value={medicationData.name}
                onChange={(e) => setMedicationData({ ...medicationData, name: e.target.value })}
                className="form-input"
                placeholder="Enter medication name (e.g., Aspirin)"
                data-appid="medication-name-input"
              />
            </div>
            <div>
              <label htmlFor="medication-notes" className="form-label">Additional Notes (Optional)</label>
              <textarea
                id="medication-notes"
                value={medicationData.notes || ''}
                onChange={(e) => setMedicationData({ ...medicationData, notes: e.target.value })}
                className="form-input"
                placeholder="Enter any additional notes or context"
                rows={3}
                data-appid="medication-notes-input"
              />
            </div>
            <button 
              onClick={handleAnalyze} 
              disabled={loading || !medicationData.name}
              className="button button-primary w-full"
              data-appid="analyze-button"
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent"></div>
                  <span>Analyzing...</span>
                </div>
              ) : (
                'Analyze Medication'
              )}
            </button>
          </div>
        </CardContent>
      </Card>

      {analysis && (
        <div className="space-y-4">
          <h2>Analysis Results</h2>
          <div className="grid md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle>Medication Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <span className="font-medium">Category:</span>
                  <span className="ml-2">{analysis.structured_info.category}</span>
                </div>
                <div>
                  <span className="font-medium">Risk Rating:</span>
                  <span className="ml-2">{analysis.structured_info.risk_rating}</span>
                </div>
                <div>
                  <span className="font-medium block mb-2">Common Side Effects:</span>
                  <ul className="list-disc list-inside space-y-1">
                    {analysis.structured_info.common_side_effects.map((effect, index) => (
                      <li key={index} className="text-sm text-muted-foreground">{effect}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <span className="font-medium block mb-2">Known Interactions:</span>
                  <ul className="list-disc list-inside space-y-1">
                    {analysis.structured_info.interactions.map((interaction, index) => (
                      <li key={index} className="text-sm text-muted-foreground">{interaction}</li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>AI Analysis</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="prose prose-sm dark:prose-invert">
                  {analysis.ai_explanation.split('\n').map((paragraph, index) => (
                    <p key={index} className="text-sm text-muted-foreground">{paragraph}</p>
                  ))}
                </div>
                <div className="mt-4 p-4 bg-muted rounded-lg">
                  <p className="text-sm text-muted-foreground italic">
                    {analysis.disclaimer}
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  )
}
