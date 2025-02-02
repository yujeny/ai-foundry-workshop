import { Inter } from "next/font/google"
import { ThemeProviderWrapper } from "@/components/theme-provider-wrapper"
import "./globals.css"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProviderWrapper>
          {children}
        </ThemeProviderWrapper>
      </body>
    </html>
  )
} 