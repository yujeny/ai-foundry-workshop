"use client";

import { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useTheme } from "next-themes";
import { 
  Sun, Moon, TestTube, Activity, 
  Microscope, LineChart, Boxes,
  AlertTriangle, Dna, Pill, 
  Users, TrendingUp,
  Loader2
} from "lucide-react";
import { cn } from "@/lib/utils";

interface DrugCandidate {
  id: string;
  molecule_type: string;
  therapeutic_area: string;
  predicted_efficacy: number;
  predicted_safety: number;
  development_stage: string;
}

interface ClinicalTrial {
  trial_id: string;
  phase: string;
  status: string;
  participant_count: number;
  target_participant_count: number;
  real_time_metrics: {
    enrollment_rate: number;
    retention_rate: number;
    safety_signals: string[];
  };
}

export default function Home() {
  const [drugCandidates, setDrugCandidates] = useState<DrugCandidate[]>([]);
  const [trials, setTrials] = useState<ClinicalTrial[]>([]);
  const [loading, setLoading] = useState(true);
  const [mounted, setMounted] = useState(false);
  const { theme, setTheme } = useTheme();

  // Prevent hydration mismatch by only rendering theme-dependent content after mount
  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [candidatesRes, trialsRes] = await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/molecular-design/candidates`),
          fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/clinical-trials/monitor`)
        ]);
        
        const candidates = await candidatesRes.json();
        const trials = await trialsRes.json();
        
        setDrugCandidates(candidates);
        setTrials(trials);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    // Poll for updates every 30 seconds
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  // Prevent hydration mismatch by not rendering until mounted
  if (!mounted) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto max-w-7xl px-4 py-8">
        <nav className="flex justify-between items-center mb-8">
          <div className="flex items-center gap-2">
            <TestTube className="h-6 w-6 text-primary" />
            <h1 className="text-2xl font-bold text-foreground">
              Drug Development Platform
            </h1>
          </div>
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="rounded-full"
          >
            {theme === "dark" ? (
              <Sun className="h-5 w-5 text-yellow-500 transition-all" />
            ) : (
              <Moon className="h-5 w-5 text-slate-900 transition-all" />
            )}
          </Button>
        </nav>

        <Card className="p-6 mb-8 border-primary/20 shadow-lg bg-destructive/5">
          <div className="flex items-center gap-2 mb-4">
            <AlertTriangle className="h-5 w-5 text-destructive" />
            <h2 className="font-semibold">Research Disclaimer</h2>
          </div>
          <p className="text-sm text-muted-foreground leading-relaxed">
            This platform is for research and development purposes only. All predictions and analyses should be validated through proper scientific methods and regulatory procedures.
          </p>
        </Card>

        <div className="grid gap-6 mb-8 grid-cols-1 lg:grid-cols-4">
          <Card className="col-span-1 lg:col-span-2 p-6 bg-card/50 hover:bg-card/80 transition-all duration-300 shadow-md hover:shadow-lg border-primary/20">
            <CardHeader className="p-0 mb-4">
              <CardTitle className="flex items-center gap-2">
                <Dna className="h-5 w-5 text-primary" />
                Molecular Design
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="space-y-4">
                {loading ? (
                  <div className="flex items-center justify-center h-32">
                    <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  </div>
                ) : drugCandidates.length === 0 ? (
                  <div className="flex items-center justify-center h-32 text-muted-foreground">
                    No drug candidates available
                  </div>
                ) : (
                  drugCandidates.slice(0, 3).map((candidate) => (
                    <div key={candidate.id} className="p-4 rounded-lg bg-background/50">
                      <div className="flex justify-between items-center mb-2">
                        <span className="font-medium">{candidate.id}</span>
                        <span className="text-xs px-2 py-1 rounded-full bg-primary/10 text-primary">
                          {candidate.therapeutic_area}
                        </span>
                      </div>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="text-muted-foreground">Efficacy</p>
                          <p className="font-medium">{(candidate.predicted_efficacy * 100).toFixed(1)}%</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Safety</p>
                          <p className="font-medium">{(candidate.predicted_safety * 100).toFixed(1)}%</p>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </CardContent>
          </Card>

          <Card className="col-span-1 lg:col-span-2 p-6 bg-card/50 hover:bg-card/80 transition-all duration-300 shadow-md hover:shadow-lg border-primary/20">
            <CardHeader className="p-0 mb-4">
              <CardTitle className="flex items-center gap-2">
                <Microscope className="h-5 w-5 text-primary" />
                Clinical Trials
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="space-y-4">
                {loading ? (
                  <div className="flex items-center justify-center h-32">
                    <Loader2 className="h-8 w-8 animate-spin text-primary" />
                  </div>
                ) : trials?.length > 0 ? trials.slice(0, 3).map((trial) => (
                  <div key={trial.trial_id} className="p-4 rounded-lg bg-background/50">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium">{trial.trial_id}</span>
                      <span className={cn("text-xs px-2 py-1 rounded-full", {
                        "bg-green-500/10 text-green-500": trial.status === "active",
                        "bg-yellow-500/10 text-yellow-500": trial.status === "recruiting",
                        "bg-blue-500/10 text-blue-500": trial.status === "completed"
                      })}>
                        {trial.phase}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Enrollment</p>
                        <p className="font-medium">
                          {trial.participant_count}/{trial.target_participant_count}
                        </p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Safety Signals</p>
                        <p className="font-medium">{trial.real_time_metrics.safety_signals.length}</p>
                      </div>
                    </div>
                  </div>
                )) : (
                  <div className="flex items-center justify-center h-32 text-muted-foreground">
                    No active trials available
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-4">
          <Card className="p-6 bg-card/50 hover:bg-card/80 transition-all duration-300 shadow-md hover:shadow-lg border-primary/20">
            <Activity className="h-6 w-6 mb-4 text-primary" />
            <h3 className="font-semibold mb-2">Automated Testing</h3>
            <p className="text-sm text-muted-foreground">High-throughput screening and analysis</p>
          </Card>
          <Card className="p-6 bg-card/50 hover:bg-card/80 transition-all duration-300 shadow-md hover:shadow-lg border-primary/20">
            <LineChart className="h-6 w-6 mb-4 text-primary" />
            <h3 className="font-semibold mb-2">Trial Analytics</h3>
            <p className="text-sm text-muted-foreground">Real-time monitoring and predictions</p>
          </Card>
          <Card className="p-6 bg-card/50 hover:bg-card/80 transition-all duration-300 shadow-md hover:shadow-lg border-primary/20">
            <Users className="h-6 w-6 mb-4 text-primary" />
            <h3 className="font-semibold mb-2">Patient Cohorts</h3>
            <p className="text-sm text-muted-foreground">Stratified analysis and outcomes</p>
          </Card>
          <Card className="p-6 bg-card/50 hover:bg-card/80 transition-all duration-300 shadow-md hover:shadow-lg border-primary/20">
            <Boxes className="h-6 w-6 mb-4 text-primary" />
            <h3 className="font-semibold mb-2">Supply Chain</h3>
            <p className="text-sm text-muted-foreground">Demand prediction and optimization</p>
          </Card>
        </div>
      </div>
    </div>
  );
}
