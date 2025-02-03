import { Link } from "react-router-dom"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"

export function AgentsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1>AI Agents Dashboard</h1>
        <p className="text-lg text-muted-foreground mt-2">
          Interact with specialized AI agents for drug discovery and analysis.
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Literature Search Agent</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Search and analyze scientific literature for drug discovery insights.
            </p>
            <Link to="/literature" className="button button-primary w-full text-center">
              Start Search
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Molecule Analysis Agent</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Analyze molecular structures and predict properties.
            </p>
            <Link to="/analysis" className="button button-primary w-full text-center">
              Analyze Molecules
            </Link>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Clinical Data Agent</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground mb-4">
              Process and analyze clinical trial data.
            </p>
            <Link to="/trials" className="button button-primary w-full text-center">
              View Data
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
