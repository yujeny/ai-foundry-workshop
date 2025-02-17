"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { api } from "@/lib/api"
import type { ChatMessage, Document } from "@/types/api"
import { FileText } from "lucide-react"

export function LiteraturePage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [documents, setDocuments] = useState<Document[]>([
    { title: "Clinical Guidelines 2023", relevance: 0.95 },
    { title: "Research Paper: New Treatment Methods", relevance: 0.87 },
    { title: "Patient Care Protocols", relevance: 0.82 }
  ])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const sendMessage = async (content: string) => {
    if (!content.trim()) return

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: content,
      role: 'user',
      timestamp: new Date().toISOString()
    }
    setMessages(prev => [...prev, userMessage])

    setLoading(true)
    setError(null)
    try {
      const response = await api.searchLiterature(content)
      if (response.error) {
        throw new Error(response.error)
      }
      
      // Add assistant message
      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: response.data?.summary || "No summary available",
        role: 'assistant',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      setError(error instanceof Error ? error.message : "Failed to search literature")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="absolute inset-0 grid grid-cols-1 md:grid-cols-[1fr,320px]">
      {/* Main Chat Area */}
      <div className="flex flex-col">
        {/* Header */}
        <div className="shrink-0 px-4 py-3 border-b bg-background">
          <h1 className="text-2xl font-bold">Literature Research</h1>
          <p className="text-sm text-muted-foreground">
            Research and analyze scientific literature through interactive conversations.
          </p>
        </div>

        {/* Messages Area - Scrollable */}
        <div className="flex-1 min-h-0 overflow-y-auto">
          <div className="p-4 space-y-4">
            {messages.length === 0 && (
              <p className="text-center text-muted-foreground py-2">
                Ask questions about research literature to get started
              </p>
            )}
            
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-[80%] rounded-lg px-3 py-2 ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground ml-auto"
                      : "bg-muted"
                  }`}
                >
                  {message.content}
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex justify-center py-2">
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-primary border-t-transparent" />
              </div>
            )}
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="shrink-0 px-4 py-2 mx-4 mb-2 text-sm text-red-500 bg-red-50 dark:bg-red-900/20 rounded-md">
            {error}
          </div>
        )}

        {/* Input Area - Fixed at Bottom */}
        <div className="shrink-0 border-t bg-background">
          <form
            onSubmit={(e) => {
              e.preventDefault()
              if (!input.trim()) return
              sendMessage(input)
              setInput("")
            }}
            className="p-3 flex gap-2"
          >
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask questions about research literature..."
              disabled={loading}
              className="flex-1"
            />
            <Button type="submit" disabled={loading}>
              {loading ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              ) : (
                "Send"
              )}
            </Button>
          </form>
        </div>
      </div>

      {/* Referenced Documents Sidebar */}
      <div className="hidden md:block border-l bg-background/50 overflow-y-auto">
        <div className="p-4">
          <h2 className="text-lg font-semibold flex items-center gap-2 mb-3">
            <FileText className="w-5 h-5" />
            Referenced Documents
          </h2>
          <div className="space-y-3">
            {documents.map((doc, index) => (
              <div key={index} className="bg-card rounded-lg p-3 shadow-sm">
                <h3 className="font-medium mb-2">{doc.title}</h3>
                <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-500 rounded-full transition-all duration-500"
                    style={{ width: `${doc.relevance * 100}%` }}
                  />
                </div>
                <p className="text-sm text-muted-foreground mt-1">
                  {Math.round(doc.relevance * 100)}% relevance
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}   