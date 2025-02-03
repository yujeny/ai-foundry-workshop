export interface PatientData {
  age: string
  gender: string
  conditions: string
  medications: string
}

export interface MoleculeData {
  smiles: string
  name?: string
  properties?: {
    molecularWeight?: number
    logP?: number
    hBondDonors?: number
    hBondAcceptors?: number
  }
}

export interface LiteratureSearchResult {
  title: string
  authors: string[]
  abstract: string
  publicationDate: string
  doi?: string
}

export interface ClinicalTrialData {
  id: string
  phase: number
  status: string
  startDate: string
  completionDate?: string
  participants: number
  conditions: string[]
  interventions: string[]
}

export interface PredictionResult {
  efficacy: number
  sideEffects: string[]
  confidence: number
  recommendations: string[]
}

export interface AnalysisResult {
  properties: MoleculeData['properties']
  predictions: {
    toxicity: number
    drugLikeness: number
    synthesizability: number
  }
  similarCompounds: string[]
}

export interface SearchResponse {
  results: LiteratureSearchResult[]
  totalResults: number
  page: number
  pageSize: number
}

export interface TrialResponse {
  trials: ClinicalTrialData[]
  totalTrials: number
  page: number
  pageSize: number
}

export interface DigitalTwinResponse {
  population_size: number
  toxicity_scores: {
    mean: number
    std: number
  }
  efficacy_metrics: {
    response_rate: number
    survival_gain: string
  }
  adverse_events: {
    mild: number
    moderate: number
    severe: number
  }
  agent_id: string
}
