import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { ThemeProvider } from './components/theme-provider'
import { MainLayout } from './components/layout/main-layout'
import { HomePage } from './pages/home'
import { AnalysisPage } from './pages/analysis'
import { TrialsPage } from './pages/trials'
import { LiteraturePage } from './pages/literature'
import { PatientPage } from './pages/patient'
import { MedicationPage } from './pages/medication'

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="app-theme">
      <Router>
        <MainLayout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/analysis" element={<AnalysisPage />} />
            <Route path="/trials" element={<TrialsPage />} />
            <Route path="/literature" element={<LiteraturePage />} />
            <Route path="/patient" element={<PatientPage />} />
            <Route path="/medication" element={<MedicationPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </MainLayout>
      </Router>
    </ThemeProvider>
  )
}

export default App
