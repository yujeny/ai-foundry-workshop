import { Button } from "../components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { useNavigate } from "react-router-dom"

export function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold tracking-tight mb-2">Drug Discovery Platform</h1>
        <p className="text-lg text-muted-foreground">
          Welcome to the AI-powered Drug Discovery Platform. Explore the capabilities of Azure AI Foundry.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Drug Candidate Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Analyze drug candidates using AI-powered molecular design and evaluation.
            </p>
            <Button 
              variant="outline"
              className="w-full" 
              onClick={() => navigate('/analysis')}
              data-appid="analysis-link"
            >
              Start Analysis
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Clinical Trials</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Monitor and analyze clinical trials data with AI assistance.
            </p>
            <Button 
              variant="outline"
              className="w-full" 
              onClick={() => navigate('/trials')}
              data-appid="trials-link"
            >
              View Trials
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>AI Agent Interactions</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Interact with specialized AI agents for drug discovery tasks.
            </p>
            <Button 
              variant="outline"
              className="w-full" 
              onClick={() => navigate('/agents')}
              data-appid="agents-link"
            >
              Meet Agents
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
