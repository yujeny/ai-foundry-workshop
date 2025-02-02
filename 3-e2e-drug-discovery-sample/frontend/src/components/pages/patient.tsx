"use client"

import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"

export function PatientPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-4xl font-bold">Patient Analysis</h1>
        <p className="text-lg text-muted-foreground mt-2">
          Analyze patient data and predict responses
        </p>
      </div>
      
      <Card>
        <CardHeader>
          <CardTitle>Patient Data</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">
            Enter patient information for analysis.
          </p>
        </CardContent>
      </Card>
    </div>
  )
} 