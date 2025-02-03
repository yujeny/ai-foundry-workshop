// Remove unused import
import { Link, useLocation } from "react-router-dom"
import { Button } from "../ui/button"
import { useTheme } from "../theme-provider"
import {
  Sun,
  Moon,
  TestTube,
  Microscope,
  LineChart,
  Search,
  Users,
  FileText
} from "lucide-react"

const navigation = [
  { id: 'agents', name: 'Agents', href: '/agents', icon: TestTube },
  { id: 'analysis', name: 'Analysis', href: '/analysis', icon: Microscope },
  { id: 'trials', name: 'Trials', href: '/trials', icon: LineChart },
  { id: 'literature', name: 'Literature', href: '/literature', icon: Search },
  { id: 'patient', name: 'Patient', href: '/patient', icon: Users },
]

export function Navbar() {
  const { theme, setTheme } = useTheme()
  const { pathname } = useLocation()

  return (
    <nav className="border-b bg-background">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2 text-foreground hover:text-foreground/80">
              <FileText className="h-6 w-6" />
              <span className="text-lg font-semibold">Drug Discovery</span>
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            {navigation.map((item) => {
              const Icon = item.icon
              return (
                <Link
                  key={item.name}
                  to={item.href}
                  data-appid={item.id}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    pathname === item.href
                      ? 'bg-secondary text-secondary-foreground'
                      : 'hover:bg-accent hover:text-accent-foreground'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.name.charAt(0).toUpperCase() + item.name.slice(1)}</span>
                </Link>
              )
            })}

            <Button
              variant="ghost"
              size="icon"
              data-appid="0"
              className="theme-toggle"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            >
              {theme === 'dark' ? (
                <Sun className="h-5 w-5 text-yellow-500" />
              ) : (
                <Moon className="h-5 w-5 text-slate-700" />
              )}
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
