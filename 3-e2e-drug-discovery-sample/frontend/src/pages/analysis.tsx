import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { api } from "../lib/api"
import type { MoleculeData, AnalysisResult } from "../types/api"

export function AnalysisPage() {
  const [moleculeData, setMoleculeData] = useState<MoleculeData>({
    smiles: '',
    name: '',
  })
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAnalyze = async () => {
    if (!moleculeData.smiles) {
      setError("Please enter a SMILES string")
      return
    }

    setLoading(true)
    setError(null)
    try {
      const { data, error: apiError } = await api.analyzeMolecule(moleculeData)
      if (apiError) {
        throw new Error(apiError)
      }
      if (data) {
        setAnalysis(data)
      } else {
        throw new Error("No data received from API")
      }
    } catch (error) {
      console.error('Analysis error:', error)
      setError(error instanceof Error ? error.message : "Failed to analyze molecule. Please check your API configuration.")
      setAnalysis(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1>Drug Candidate Analysis</h1>
        <p className="text-lg text-muted-foreground mt-2">
          Analyze drug candidates and predict their properties using AI.
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
          <CardTitle>Molecule Input</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <label className="form-label">SMILES String</label>
              <input
                type="text"
                value={moleculeData.smiles}
                onChange={(e) => setMoleculeData({ ...moleculeData, smiles: e.target.value })}
                className="form-input"
                placeholder="Enter SMILES notation (e.g., CC(=O)OC1=CC=CC=C1C(=O)O)"
                data-appid="smiles-input"
              />
            </div>
            <div>
              <label className="form-label">Molecule Name (Optional)</label>
              <input
                type="text"
                value={moleculeData.name || ''}
                onChange={(e) => setMoleculeData({ ...moleculeData, name: e.target.value })}
                className="form-input"
                placeholder="Enter molecule name"
                data-appid="molecule-name-input"
              />
            </div>
            <button 
              onClick={handleAnalyze} 
              disabled={loading || !moleculeData.smiles}
              className="button button-primary w-full"
              data-appid="analyze-button"
            >
              {loading ? (
                <div className="flex items-center justify-center space-x-2">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent"></div>
                  <span>Analyzing...</span>
                </div>
              ) : (
                'Analyze Molecule'
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
                <CardTitle>Molecular Properties</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {analysis.properties && (
                  <>
                    <div>
                      <span className="font-medium">Molecular Weight:</span>
                      <span className="ml-2">{analysis.properties.molecularWeight?.toFixed(2)}</span>
                    </div>
                    <div>
                      <span className="font-medium">LogP:</span>
                      <span className="ml-2">{analysis.properties.logP?.toFixed(2)}</span>
                    </div>
                    <div>
                      <span className="font-medium">H-Bond Donors:</span>
                      <span className="ml-2">{analysis.properties.hBondDonors}</span>
                    </div>
                    <div>
                      <span className="font-medium">H-Bond Acceptors:</span>
                      <span className="ml-2">{analysis.properties.hBondAcceptors}</span>
                    </div>
                  </>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Predictions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <span className="font-medium">Toxicity Risk:</span>
                  <span className="ml-2">{(analysis.predictions.toxicity * 100).toFixed(1)}%</span>
                </div>
                <div>
                  <span className="font-medium">Drug-likeness:</span>
                  <span className="ml-2">{(analysis.predictions.drugLikeness * 100).toFixed(1)}%</span>
                </div>
                <div>
                  <span className="font-medium">Synthesizability:</span>
                  <span className="ml-2">{(analysis.predictions.synthesizability * 100).toFixed(1)}%</span>
                </div>
                {analysis.similarCompounds.length > 0 && (
                  <div>
                    <span className="font-medium block mb-2">Similar Compounds:</span>
                    <ul className="list-disc list-inside space-y-1">
                      {analysis.similarCompounds.map((compound, index) => (
                        <li key={index} className="text-sm text-muted-foreground">{compound}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  )
}
