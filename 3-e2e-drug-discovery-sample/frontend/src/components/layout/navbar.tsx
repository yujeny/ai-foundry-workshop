"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "../ui/button"
import { useTheme } from "../ui/theme-provider"
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
  { name: 'Agents', href: '/agents', icon: TestTube },
  { name: 'Analysis', href: '/analysis', icon: Microscope },
  { name: 'Trials', href: '/trials', icon: LineChart },
  { name: 'Literature', href: '/literature', icon: Search },
  { name: 'Patient', href: '/patient', icon: Users },
]

export function Navbar() {
  const { theme, setTheme } = useTheme()
  const pathname = usePathname()

  return (
    <nav className="border-b">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
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
                  href={item.href}
                  className={`flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                    pathname === item.href
                      ? 'bg-secondary text-secondary-foreground'
                      : 'hover:bg-accent hover:text-accent-foreground'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{item.name}</span>
                </Link>
              )
            })}

            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            >
              {theme === 'dark' ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>
      </div>
    </nav>
  )
}
