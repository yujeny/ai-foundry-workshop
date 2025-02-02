"use client"

import * as React from "react"
import { Navbar } from "./navbar"

interface MainLayoutProps {
  children: React.ReactNode
}

export function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        {children}
      </main>
    </div>
  )
}
