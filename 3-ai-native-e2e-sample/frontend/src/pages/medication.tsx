import { useState } from "react"
import { Button } from "../components/ui/button"
import { Card, CardContent } from "../components/ui/card"
import { Input } from "../components/ui/input"
import { Textarea } from "../components/ui/textarea"
import { Pill } from "lucide-react"
import { api } from "../lib/api"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

import type { MedicationAnalysis } from "../types/api"
type MedicationResult = MedicationAnalysis

export function MedicationPage() {
  const [name, setName] = useState("")
  const [notes, setNotes] = useState("")
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<MedicationResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const analyzeMedication = async () => {
    setLoading(true)
    setError(null)
    try {
      const { data, error: apiError } = await api.analyzeMedication({ name, notes })
      if (apiError) {
        throw new Error(apiError)
      }
      setResult(data ?? null)
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to analyze medication")
      setResult(null)
    } finally {
      setLoading(false)
    }
  }

  // Mock data for visualization
  const sideEffectData = [
    { name: "Common", value: 75 },
    { name: "Uncommon", value: 20 },
    { name: "Rare", value: 5 }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center space-x-4">
        <Pill className="h-8 w-8 text-primary" />
        <div>
          <h1 className="text-4xl font-bold">Medication Analysis</h1>
          <p className="text-lg text-muted-foreground mt-2">
            Analyze medication properties and potential interactions
          </p>
        </div>
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="grid gap-4">
            <Input 
              placeholder="Enter medication name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
            <Textarea
              placeholder="Additional notes or context (optional)"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
            />
            <Button 
              onClick={analyzeMedication}
              disabled={loading || !name}
              className="w-full"
            >
              {loading ? (
                <div className="flex items-center space-x-2">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"></div>
                  <span>Analyzing...</span>
                </div>
              ) : (
                "Analyze Medication"
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {error && (
        <Card className="border-destructive">
          <CardContent className="p-6">
            <p className="text-center text-destructive">{error}</p>
          </CardContent>
        </Card>
      )}

      {result && (
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardContent className="p-6 space-y-4">
              <h2 className="text-2xl font-semibold">Analysis Results</h2>
              
              <div>
                <h3 className="font-medium mb-2">Category</h3>
                <p className="text-muted-foreground">{result.structured_info.category}</p>
              </div>
              
              <div>
                <h3 className="font-medium mb-2">Side Effects</h3>
                <p className="text-muted-foreground">{result.structured_info.common_side_effects.join(", ")}</p>
              </div>
              
              <div>
                <h3 className="font-medium mb-2">Risk Rating</h3>
                <p className="text-muted-foreground">{result.structured_info.risk_rating}</p>
              </div>
              
              <div>
                <h3 className="font-medium mb-2">Drug Interactions</h3>
                <p className="text-muted-foreground">{result.structured_info.interactions.join(", ")}</p>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6 space-y-4">
              <h2 className="text-2xl font-semibold">Side Effect Distribution</h2>
              <div className="h-[300px]">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={sideEffectData}>
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Line 
                      type="monotone" 
                      dataKey="value" 
                      stroke="hsl(217.2 91.2% 59.8%)"
                      strokeWidth={2}
                      dot={{ r: 4 }}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              <div className="mt-4 p-4 bg-muted rounded-lg">
                <h3 className="font-medium mb-2">Medical Disclaimer</h3>
                <p className="text-sm text-muted-foreground">{result.disclaimer}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
