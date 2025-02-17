import { Link } from "react-router-dom"
import { Button } from "../components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "../components/ui/card"
import { Pill, LineChart, MessageSquare, Users } from "lucide-react"

export function HomePage() {
  return (
    <div className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Welcome to Drug Discovery Platform</h1>
        <p className="text-muted-foreground">
          Explore medications, clinical trials, and research literature with AI assistance
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-2">
        <Link to="/medication">
          <Card className="hover:bg-muted/50 transition-colors">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Pill className="h-5 w-5" />
                Analyze Medications
              </CardTitle>
              <CardDescription>
                Analyze drug compounds and their potential effects
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="secondary">Get Started</Button>
            </CardContent>
          </Card>
        </Link>

        <Link to="/trials">
          <Card className="hover:bg-muted/50 transition-colors">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <LineChart className="h-5 w-5" />
                Clinical Trials
              </CardTitle>
              <CardDescription>
                Monitor and analyze ongoing clinical trials
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="secondary">View Trials</Button>
            </CardContent>
          </Card>
        </Link>

        <Link to="/literature">
          <Card className="hover:bg-muted/50 transition-colors">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageSquare className="h-5 w-5" />
                Literature Search
              </CardTitle>
              <CardDescription>
                Search and analyze research papers
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="secondary">Search Papers</Button>
            </CardContent>
          </Card>
        </Link>

        <Link to="/patient">
          <Card className="hover:bg-muted/50 transition-colors">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                Patient Data
              </CardTitle>
              <CardDescription>
                View and analyze patient information
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Button variant="secondary">View Patients</Button>
            </CardContent>
          </Card>
        </Link>
      </div>
    </div>
  )
}
