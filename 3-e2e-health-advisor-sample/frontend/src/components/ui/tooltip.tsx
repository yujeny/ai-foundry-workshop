"use client"

import React, { useState } from "react"

interface TooltipProps {
  content: React.ReactNode
  children: React.ReactNode
  className?: string
}

const Tooltip = ({ content, children, className = "" }: TooltipProps) => {
  const [isVisible, setIsVisible] = useState(false)

  return (
    <div 
      className="relative inline-block"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      {children}
      {isVisible && (
        <div className={`
          absolute z-50 px-2 py-1 text-sm
          bg-popover text-popover-foreground
          rounded-md shadow-md
          -translate-y-full -translate-x-1/2
          left-1/2 top-0 mt-1
          ${className}
        `}>
          {content}
          <div className="
            absolute -bottom-1 left-1/2 
            w-2 h-2 bg-popover 
            -translate-x-1/2 rotate-45
          "/>
        </div>
      )}
    </div>
  )
}

// Simple wrapper components to maintain similar API
const TooltipProvider = ({ children }: { children: React.ReactNode }) => children
const TooltipTrigger = ({ children }: { children: React.ReactNode }) => <>{children}</>
const TooltipContent = ({ children }: { children: React.ReactNode }) => <>{children}</>

export { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider }
