import { useState } from "react"
import { Button } from "../components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { api } from "../lib/api"
import type { PatientData, PredictionResult } from "../types/api"

export function PatientPage() {
  const [patientData, setPatientData] = useState<PatientData>({
    age: '',
    gender: '',
    conditions: '',
    medications: ''
  })
  const [prediction, setPrediction] = useState<PredictionResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handlePredictResponse = async () => {
    if (!patientData.age || !patientData.gender) {
      setError('Please fill in at least age and gender')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const { data, error: apiError } = await api.predictPatientResponse(patientData)
      if (apiError) {
        throw new Error(apiError)
      }
      if (data) {
        setPrediction(data)
      }
    } catch (error) {
      setError(error instanceof Error ? error.message : 'Failed to predict patient response')
      setPrediction(null)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold">Patient Response Prediction</h1>
        <p className="text-lg text-muted-foreground mt-2">
          Predict patient responses to treatments using AI analysis.
        </p>
      </div>

      {error && (
        <Card className="border-destructive">
          <CardContent className="p-6">
            <p className="text-center text-destructive">{error}</p>
          </CardContent>
        </Card>
      )}

      <div className="grid md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Patient Information</CardTitle>
          </CardHeader>
          <CardContent>
            <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
              <div>
                <label className="block text-sm font-medium mb-1">Age</label>
                <input
                  type="number"
                  value={patientData.age}
                  onChange={(e) => setPatientData({ ...patientData, age: e.target.value })}
                  className="form-input"
                  placeholder="Enter age"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Gender</label>
                <select
                  value={patientData.gender}
                  onChange={(e) => setPatientData({ ...patientData, gender: e.target.value })}
                  className="form-input"
                >
                  <option value="">Select gender</option>
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Pre-existing Conditions</label>
                <textarea
                  value={patientData.conditions}
                  onChange={(e) => setPatientData({ ...patientData, conditions: e.target.value })}
                  className="form-input"
                  rows={3}
                  placeholder="Enter pre-existing conditions"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Current Medications</label>
                <textarea
                  value={patientData.medications}
                  onChange={(e) => setPatientData({ ...patientData, medications: e.target.value })}
                  className="form-input"
                  rows={3}
                  placeholder="Enter current medications"
                />
              </div>
              <Button 
                onClick={handlePredictResponse} 
                disabled={loading || !patientData.age || !patientData.gender}
                className="w-full"
              >
                {loading ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent"></div>
                    <span>Analyzing Patient Data...</span>
                  </div>
                ) : (
                  'Predict Response'
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        <div className="space-y-4">
          <h2 className="text-2xl font-semibold">Prediction Results</h2>
          {prediction ? (
            <Card>
              <CardContent className="p-6 space-y-6">
                <div>
                  <h3 className="font-medium mb-2">Treatment Efficacy</h3>
                  <p className="text-muted-foreground">{(prediction.efficacy * 100).toFixed(1)}%</p>
                </div>
                <div>
                  <h3 className="font-medium mb-2">Confidence Level</h3>
                  <p className="text-muted-foreground">{(prediction.confidence * 100).toFixed(1)}%</p>
                </div>
                <div>
                  <h3 className="font-medium mb-2">Potential Side Effects</h3>
                  <div className="flex flex-wrap gap-2">
                    {prediction.sideEffects.map((effect, index) => (
                      <span key={index} className="px-2 py-1 bg-secondary rounded-md text-sm">
                        {effect}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <h3 className="font-medium mb-2">Recommendations</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {prediction.recommendations.map((rec, index) => (
                      <li key={index} className="text-muted-foreground">
                        {rec}
                      </li>
                    ))}
                  </ul>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="p-6">
                <p className="text-muted-foreground">
                  Enter patient information and click "Predict Response" to see AI-powered predictions.
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  )
}
