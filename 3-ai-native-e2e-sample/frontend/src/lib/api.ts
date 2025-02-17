import type { MedicationAnalysis, MedicationInfo, TrialEvent } from "../types/api";
import { API_URL, API_VERSION } from '../config'

interface ApiResponse<T> {
  data: T | null;
  error: string | null;
}

export const api = {
  analyzeMedication: async ({ name, notes }: MedicationInfo): Promise<ApiResponse<MedicationAnalysis>> => {
    try {
      const response = await fetch(`${API_URL}/agents/medication/analyze`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'x-api-version': API_VERSION,
        },
        body: JSON.stringify({ name, notes })
      });
      
      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || 'Failed to analyze medication');
      }
      
      if (!response.body) {
        throw new Error('No response body received');
      }

      const reader = response.body.getReader();
      let result = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = new TextDecoder().decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data.trim()) {
              try {
                const parsed = JSON.parse(data);
                if (parsed.type === 'error') {
                  throw new Error(parsed.content);
                }
                if (parsed.type === 'message') {
                  result = parsed.content;
                }
                if (parsed.done) {
                  const structuredResult = JSON.parse(result);
                  return { data: structuredResult, error: null };
                }
              } catch (e) {
                console.error('Error parsing SSE data:', e);
              }
            }
          }
        }
      }

      throw new Error('Stream ended without valid response');
    } catch (error) {
      return { 
        data: null, 
        error: error instanceof Error ? error.message : 'Failed to analyze medication'
      };
    }
  },

  simulateTrialData: async (): Promise<ApiResponse<{ events: TrialEvent[] }>> => {
    try {
      const response = await fetch(`${API_URL}/api/trials/simulate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-version': API_VERSION,
        }
      });

      if (!response.ok) {
        const error = await response.text();
        throw new Error(error || 'Failed to simulate trial data');
      }

      const data = await response.json();
      return { data, error: null };
    } catch (error) {
      return {
        data: null,
        error: error instanceof Error ? error.message : 'Failed to simulate trial data'
      };
    }
  }
};

export interface LiteratureSearchResponse {
  results: string[]
  summary?: string
  error?: string
}

export async function searchLiterature(query: string): Promise<LiteratureSearchResponse> {
  try {
    const response = await fetch(`${API_URL}/agents/literature-search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-version': API_VERSION,
      },
      body: JSON.stringify({ query }),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Error searching literature:', error)
    return {
      results: [],
      error: error instanceof Error ? error.message : 'An unknown error occurred'
    }
  }
}

export interface LiteratureChatResponse {
  response: string
  error?: string
}

export interface LiteratureChatRequest {
  message: string
  history?: Array<{ role: 'user' | 'assistant', content: string }>
}

export async function literatureChat(request: LiteratureChatRequest): Promise<LiteratureChatResponse> {
  try {
    const response = await fetch(`${API_URL}/agents/literature-chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-version': API_VERSION,
      },
      body: JSON.stringify(request),
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    console.error('Error in literature chat:', error)
    return {
      response: '',
      error: error instanceof Error ? error.message : 'An unknown error occurred'
    }
  }
}
