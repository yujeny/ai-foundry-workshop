"use client";

import { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { useTheme } from "next-themes";
import { MoleculeViewer } from "@/components/molecule-viewer";
import { useDrugDiscoveryStore } from "@/lib/store/drug-discovery";
import { 
  Sun, Moon, TestTube,
  Microscope, LineChart, Search,
  AlertTriangle, Dna,
  Upload, Loader2
} from "lucide-react";

export default function DrugDiscoveryPlatform() {
  const [mounted, setMounted] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [smiles, setSmiles] = useState("");
  const [targetProteins, setTargetProteins] = useState("");
  const [therapeuticArea, setTherapeuticArea] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { setTheme } = useTheme();

  const {
    searchLiterature,
    analyzeMolecule,
    analyzeTrialData,
    literatureResults,
    moleculeAnalysis,
    trialAnalysis,
    isSearching,
    isAnalyzing,
    isAnalyzingTrials,
  } = useDrugDiscoveryStore();

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleLiteratureSearch = async () => {
    if (!searchQuery.trim()) return;
    await searchLiterature(searchQuery);
  };

  const handleMoleculeAnalysis = async () => {
    if (!smiles.trim() || !targetProteins.trim() || !therapeuticArea.trim()) return;
    await analyzeMolecule({
      smiles,
      target_proteins: targetProteins.split(",").map(p => p.trim()),
      therapeutic_area: therapeuticArea
    });
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleTrialDataAnalysis = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append("file", selectedFile);
    await analyzeTrialData(formData);
  };

  // Prevent hydration mismatch by not rendering until mounted
  if (!mounted) {
    return null;
  }

  if (!mounted) return null;

  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b">
        <div className="container flex h-16 items-center px-4">
          <div className="flex items-center space-x-4">
            <Dna className="h-6 w-6" />
            <h1 className="text-xl font-bold">Drug Discovery Platform</h1>
          </div>
          <div className="ml-auto flex items-center space-x-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme("light")}
              className="hidden dark:inline-flex"
            >
              <Sun className="h-5 w-5" />
              <span className="sr-only">Light mode</span>
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme("dark")}
              className="inline-flex dark:hidden"
            >
              <Moon className="h-5 w-5" />
              <span className="sr-only">Dark mode</span>
            </Button>
          </div>
        </div>
      </nav>

      <main className="container py-6">
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-yellow-500" />
              Important Notice
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              This is a demonstration platform showcasing Azure AI Agents capabilities in drug discovery.
              Do not use for actual drug development or clinical decisions.
            </p>
          </CardContent>
        </Card>

        <Tabs defaultValue="literature" className="space-y-4">
          <TabsList>
            <TabsTrigger value="literature" className="flex items-center gap-2">
              <Search className="h-4 w-4" />
              Literature Search
            </TabsTrigger>
            <TabsTrigger value="molecule" className="flex items-center gap-2">
              <TestTube className="h-4 w-4" />
              Molecule Analysis
            </TabsTrigger>
            <TabsTrigger value="trials" className="flex items-center gap-2">
              <LineChart className="h-4 w-4" />
              Trial Data Analysis
            </TabsTrigger>
          </TabsList>

          <TabsContent value="literature" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Search className="h-5 w-5" />
                  Literature Search
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex gap-4">
                  <Input
                    placeholder="Enter your research query..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                  />
                  <Button
                    onClick={handleLiteratureSearch}
                    disabled={isSearching}
                    className="w-32"
                  >
                    {isSearching ? (
                      <Loader2 className="h-4 w-4 animate-spin" />
                    ) : (
                      "Search"
                    )}
                  </Button>
                </div>
                {literatureResults && (
                  <Card className="mt-4">
                    <CardContent className="pt-6">
                      <h3 className="font-semibold mb-2">Results</h3>
                      <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                        {literatureResults.summary}
                      </p>
                      <div className="mt-4 text-xs text-muted-foreground">
                        Agent ID: {literatureResults.agent_id}
                      </div>
                    </CardContent>
                  </Card>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="molecule" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TestTube className="h-5 w-5" />
                  Molecule Analysis
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-4">
                  <div>
                    <Input
                      placeholder="Enter SMILES notation..."
                      value={smiles}
                      onChange={(e) => setSmiles(e.target.value)}
                    />
                  </div>
                  <div>
                    <Input
                      placeholder="Target proteins (comma-separated)..."
                      value={targetProteins}
                      onChange={(e) => setTargetProteins(e.target.value)}
                    />
                  </div>
                  <div>
                    <Input
                      placeholder="Therapeutic area..."
                      value={therapeuticArea}
                      onChange={(e) => setTherapeuticArea(e.target.value)}
                    />
                  </div>
                  <Button
                    onClick={handleMoleculeAnalysis}
                    disabled={isAnalyzing}
                    className="w-full"
                  >
                    {isAnalyzing ? (
                      <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    ) : (
                      <Microscope className="h-4 w-4 mr-2" />
                    )}
                    Analyze Molecule
                  </Button>
                </div>
                {moleculeAnalysis && (
                  <div className="mt-4 space-y-4">
                    <div className="h-64 border rounded-lg overflow-hidden">
                      <MoleculeViewer smiles={moleculeAnalysis.molecule} />
                    </div>
                    <Card>
                      <CardContent className="pt-6">
                        <h3 className="font-semibold mb-2">Analysis Results</h3>
                        <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                          {moleculeAnalysis.analysis}
                        </p>
                        <div className="mt-4 text-xs text-muted-foreground">
                          Agent ID: {moleculeAnalysis.agent_id}
                        </div>
                      </CardContent>
                    </Card>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="trials" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <LineChart className="h-5 w-5" />
                  Trial Data Analysis
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid gap-4">
                  <div className="flex items-center gap-4">
                    <Input
                      type="file"
                      accept=".csv"
                      onChange={handleFileUpload}
                      className="flex-1"
                    />
                    <Button
                      onClick={handleTrialDataAnalysis}
                      disabled={isAnalyzingTrials || !selectedFile}
                      className="w-32"
                    >
                      {isAnalyzingTrials ? (
                        <Loader2 className="h-4 w-4 animate-spin mr-2" />
                      ) : (
                        <Upload className="h-4 w-4 mr-2" />
                      )}
                      Analyze
                    </Button>
                  </div>
                </div>
                {trialAnalysis && (
                  <Card>
                    <CardContent className="pt-6">
                      <h3 className="font-semibold mb-2">Analysis Results</h3>
                      <p className="text-sm text-muted-foreground whitespace-pre-wrap">
                        {trialAnalysis.analysis}
                      </p>
                      <div className="mt-4 text-xs text-muted-foreground">
                        File: {trialAnalysis.filename}
                        <br />
                        Agent ID: {trialAnalysis.agent_id}
                      </div>
                    </CardContent>
                  </Card>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
