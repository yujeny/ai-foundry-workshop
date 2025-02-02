"use client"

import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

export function LiteraturePage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold">Literature Search</h1>
        <p className="text-lg text-muted-foreground mt-2">
          Search and analyze scientific literature
        </p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Search</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Enter keywords to search scientific literature.
          </p>
        </CardContent>
      </Card>
    </div>
  )
} 