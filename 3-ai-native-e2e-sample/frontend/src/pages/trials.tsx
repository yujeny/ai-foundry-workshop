import { useState, useEffect } from "react"
import { Button } from "../components/ui/button"
import { Card, CardContent } from "../components/ui/card"
import { RefreshCw } from "lucide-react"
import { api } from "../lib/api"
import type { TrialEventResponse, TrialEvent, TrialEventAnalysis } from "../types/api"
import { TrialVisualization } from "../components/trial-visualization"

export function TrialsPage() {
  const [events, setEvents] = useState<TrialEvent[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const simulateTrialData = async () => {
    setLoading(true)
    setError(null)
    try {
      console.log('Calling simulateTrialData API...')
      const { data, error: apiError } = await api.simulateTrialData()
      
      console.log('API Response:', { data, error: apiError })
      
      if (apiError) {
        throw new Error(apiError)
      }

      if (!data || typeof data !== 'object') {
        console.error('No data received from API')
        throw new Error("No data received from API")
      }

      setEvents(data.events)
      
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : "Failed to simulate trial data"
      console.error('Trial simulation error:', error)
      setError(errorMessage)
      setEvents([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    console.log('Initializing trials view...')
    simulateTrialData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="flex flex-col items-center space-y-4">
          <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"></div>
          <p className="text-muted-foreground">Loading clinical trials data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-4xl font-bold">Clinical Trials Monitor</h1>
          <p className="text-lg text-muted-foreground mt-2">
            Monitor and analyze ongoing clinical trials.
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <Button
            onClick={simulateTrialData}
            disabled={loading}
            variant="outline"
            className="border-2 hover:bg-primary hover:text-primary-foreground transition-colors"
            data-appid="simulate-trial-button"
          >
            {loading ? (
              <div className="flex items-center space-x-2">
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"></div>
                <span>Simulating...</span>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <RefreshCw className="h-4 w-4" />
                <span>Simulate Trial Data</span>
              </div>
            )}
          </Button>
        </div>
      </div>

      {error && (
        <Card className="border-destructive">
          <CardContent className="p-6">
            <p className="text-center text-destructive">{error}</p>
          </CardContent>
        </Card>
      )}

      {events.length > 0 && (
        <div className="space-y-6">
          <div className="grid gap-6">
            {events.map((event, index) => (
              <Card key={index}>
                <CardContent className="p-6">
                  <div className="flex justify-between items-start mb-4">
                    <div>
                      <h3 className="font-medium">Trial ID: {event.trialId}</h3>
                      <p className="text-sm text-muted-foreground">
                        Patient ID: {event.patientId} • Study Arm: {event.studyArm}
                      </p>
                    </div>
                    <span className="px-2 py-1 text-xs rounded-full bg-secondary">
                      {new Date(event.timestamp).toLocaleString()}
                    </span>
                  </div>
                  
                  <div className="space-y-4">
                    <div>
                      <h4 className="font-medium mb-2">Vital Signs</h4>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                        <div>
                          <span className="text-sm text-muted-foreground">Heart Rate</span>
                          <p>{event.vitals.heartRate} bpm</p>
                        </div>
                        <div>
                          <span className="text-sm text-muted-foreground">Blood Pressure</span>
                          <p>{event.vitals.bloodPressure}</p>
                        </div>
                        <div>
                          <span className="text-sm text-muted-foreground">Temperature</span>
                          <p>{event.vitals.temperature}°C</p>
                        </div>
                        <div>
                          <span className="text-sm text-muted-foreground">Respiratory Rate</span>
                          <p>{event.vitals.respiratoryRate} /min</p>
                        </div>
                        <div>
                          <span className="text-sm text-muted-foreground">O2 Saturation</span>
                          <p>{event.vitals.oxygenSaturation}%</p>
                        </div>
                      </div>
                    </div>

                    {event.adverseEvents.length > 0 && (
                      <div>
                        <h4 className="font-medium mb-2">Adverse Events</h4>
                        <div className="space-y-2">
                          {event.adverseEvents.map((ae, idx) => (
                            <div key={idx} className="flex items-center space-x-2">
                              <span className={`px-2 py-1 text-sm rounded-full ${
                                ae.type === 'Severe' ? 'bg-destructive/10 text-destructive' :
                                ae.type === 'Moderate' ? 'bg-warning/10 text-warning' :
                                'bg-muted text-muted-foreground'
                              }`}>
                                {ae.type}
                              </span>
                              {ae.description && (
                                <span className="text-sm">{ae.description}</span>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
