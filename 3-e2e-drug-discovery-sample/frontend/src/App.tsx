"use client"

import { ThemeProvider } from './components/ui/theme-provider'
import { MainLayout } from './components/layout/main-layout'

function App() {
  return (
    <ThemeProvider defaultTheme="dark">
      <MainLayout>
        {/* Next.js will handle routing automatically based on the pages directory structure */}
      </MainLayout>
    </ThemeProvider>
  )
}

export default App
