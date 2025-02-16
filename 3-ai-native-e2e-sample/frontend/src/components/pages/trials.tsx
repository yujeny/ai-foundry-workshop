"use client"

import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

export function TrialsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold">Clinical Trials</h1>
        <p className="text-lg text-muted-foreground mt-2">
          Monitor and analyze clinical trial data
        </p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Active Trials</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            No active trials found.
          </p>
        </CardContent>
      </Card>
    </div>
  )
} 