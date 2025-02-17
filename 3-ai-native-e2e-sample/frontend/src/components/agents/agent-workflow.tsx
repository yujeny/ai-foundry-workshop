import { useState } from "react"

interface MedicationAnalysis {
  analysis: string;
  interactions: string[];
  warnings: string[];
  recommendations: string[];
}

export function AgentWorkflow() {
  const [medicationName, setMedicationName] = useState('');
  const [notes, setNotes] = useState('');
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<MedicationAnalysis | null>(null);
  const [error, setError] = useState<string | null>(null);

  const analyzeMedication = async () => {
    if (!medicationName) return;
    
    setLoading(true);
    setError(null);
    setAnalysis(null);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_BASE_URL}/agents/medication/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: medicationName,
          notes: notes || undefined,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || response.statusText);
      }

      const data = await response.json();
      setAnalysis(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 max-w-4xl">
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Medication Analysis</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Medication Name</label>
            <input
              type="text"
              value={medicationName}
              onChange={(e) => setMedicationName(e.target.value)}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter medication name"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Additional Notes (Optional)</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              className="w-full p-2 border rounded focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter any additional notes"
              rows={3}
            />
          </div>
          <button
            onClick={analyzeMedication}
            disabled={loading || !medicationName}
            className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Analyzing...' : 'Analyze Medication'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {analysis && (
        <div className="bg-white shadow-lg rounded-lg p-6">
          <h3 className="text-xl font-semibold mb-6 text-gray-800">{analysis.analysis}</h3>
          
          <div className="space-y-6">
            <div>
              <h4 className="font-medium text-lg mb-3 text-blue-600">Interactions</h4>
              <ul className="list-disc pl-5 space-y-2">
                {analysis.interactions.map((interaction, i) => (
                  <li key={i} className="text-gray-700">{interaction}</li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="font-medium text-lg mb-3 text-yellow-600">Warnings</h4>
              <ul className="list-disc pl-5 space-y-2">
                {analysis.warnings.map((warning, i) => (
                  <li key={i} className="text-gray-700">{warning}</li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="font-medium text-lg mb-3 text-green-600">Recommendations</h4>
              <ul className="list-disc pl-5 space-y-2">
                {analysis.recommendations.map((recommendation, i) => (
                  <li key={i} className="text-gray-700">{recommendation}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
