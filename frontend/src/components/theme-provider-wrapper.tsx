"use client"

import { ThemeProvider } from "@/providers/theme-provider"

export function ThemeProviderWrapper({
  children,
}: {
  children: React.ReactNode
}) {
  return <ThemeProvider defaultTheme="dark">{children}</ThemeProvider>
} 