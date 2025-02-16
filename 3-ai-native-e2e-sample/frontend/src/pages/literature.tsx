import { useState, type FormEvent } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { Button } from "../components/ui/button"
import { Input } from "../components/ui/input"
import { SendHorizontal } from "lucide-react"
import { api } from "../lib/api"
import type { ChatMessage } from "../types/api"

export function LiteraturePage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return
    setLoading(true)
    setError(null)
    try {
      const { data, error: apiError } = await api.searchLiterature(input)
      if (apiError) {
        throw new Error(apiError)
      }
      const timestamp = new Date().toISOString()
      const newMessages: ChatMessage[] = [
        { 
          id: `user-${timestamp}`,
          role: 'user',
          content: input,
          timestamp
        },
        { 
          id: `assistant-${timestamp}`,
          role: 'assistant',
          content: data.summary,
          timestamp
        }
      ]
      setMessages(prev => [...prev, ...newMessages])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to search literature')
    } finally {
      setLoading(false)
      setInput("")
    }
  }

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>Literature Search</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Enter your research query..."
              disabled={loading}
            />
            <Button type="submit" disabled={loading || !input.trim()}>
              {loading ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              ) : (
                <SendHorizontal className="h-4 w-4" />
              )}
            </Button>
          </form>
          
          {error && (
            <p className="mt-2 text-sm text-destructive">{error}</p>
          )}
          
          <div className="mt-4 space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`p-4 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-primary/10 ml-auto max-w-[80%]'
                    : 'bg-muted'
                }`}
              >
                <p className="text-sm">{message.content}</p>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
