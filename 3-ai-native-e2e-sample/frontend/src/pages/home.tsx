import { Button } from "../components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { useNavigate } from "react-router-dom"
import { Bot, Microscope, LineChart, MessageSquare } from "lucide-react"

export function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-bold tracking-tight mb-2">Event-Driven AI Platform</h1>
        <p className="text-base sm:text-lg text-muted-foreground">
          Explore how Azure AI Foundry powers real-time, event-driven ambient agents for clinical research and drug discovery.
        </p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <Card className="group hover:shadow-lg transition-all duration-200 flex flex-col">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-lg sm:text-xl font-bold">Clinical Trials Monitor</CardTitle>
            <LineChart className="h-5 w-5 sm:h-6 sm:w-6 text-muted-foreground group-hover:text-primary transition-colors" />
          </CardHeader>
          <CardContent className="flex-1 flex flex-col">
            <p className="text-sm sm:text-base text-muted-foreground mb-4 flex-1">
              Experience real-time clinical trial monitoring with event-driven AI agents. Simulate trial data streams and observe how agents analyze safety signals and efficacy trends.
            </p>
            <Button 
              variant="outline"
              className="w-full hover:bg-primary hover:text-primary-foreground" 
              onClick={() => navigate('/trials')}
              data-appid="trials-link"
            >
              Monitor Trials
            </Button>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-lg transition-all duration-200 flex flex-col">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-lg sm:text-xl font-bold">Literature Answer Engine</CardTitle>
            <MessageSquare className="h-5 w-5 sm:h-6 sm:w-6 text-muted-foreground group-hover:text-primary transition-colors" />
          </CardHeader>
          <CardContent className="flex-1 flex flex-col">
            <p className="text-sm sm:text-base text-muted-foreground mb-4 flex-1">
              Get instant answers from your research literature. Ask questions about drug research, clinical studies, and scientific publications to receive focused, evidence-based responses.
            </p>
            <Button 
              variant="outline"
              className="w-full hover:bg-primary hover:text-primary-foreground" 
              onClick={() => navigate('/literature')}
              data-appid="literature-link"
            >
              Ask Questions
            </Button>
          </CardContent>
        </Card>

        <Card className="group hover:shadow-lg transition-all duration-200 flex flex-col">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-lg sm:text-xl font-bold">Medication Analysis</CardTitle>
            <Microscope className="h-5 w-5 sm:h-6 sm:w-6 text-muted-foreground group-hover:text-primary transition-colors" />
          </CardHeader>
          <CardContent className="flex-1 flex flex-col">
            <p className="text-sm sm:text-base text-muted-foreground mb-4 flex-1">
              Get comprehensive medication information and AI-powered analysis of drug interactions and effects.
            </p>
            <Button 
              variant="outline"
              className="w-full hover:bg-primary hover:text-primary-foreground" 
              onClick={() => navigate('/analysis')}
              data-appid="analysis-link"
            >
              Analyze Medications
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
