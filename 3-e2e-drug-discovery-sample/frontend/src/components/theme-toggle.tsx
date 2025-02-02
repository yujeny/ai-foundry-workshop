
import { Button } from "./ui/button"
import { MoonIcon, SunIcon } from "lucide-react"
import { useTheme } from "./ui/theme-provider"

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  
  return (
    <Button
      variant="outline"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="transition-colors duration-200"
      title={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
    >
      {theme === "dark" ? (
        <SunIcon className="h-5 w-5 text-yellow-500" />
      ) : (
        <MoonIcon className="h-5 w-5 text-slate-700" />
      )}
    </Button>
  )
}
