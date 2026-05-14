import { Loader2 } from "lucide-react";

interface LoadingSpinnerProps {
  message?: string;
  className?: string;
}

export default function LoadingSpinner({ message = "Loading...", className = "" }: LoadingSpinnerProps) {
  return (
    <div className={`flex flex-col items-center justify-center p-8 gap-4 ${className}`}>
      <div className="flex items-center gap-1.5 h-8">
        <div className="w-1.5 h-1.5 rounded-full bg-current animate-pulse [animation-delay:-0.3s]" />
        <div className="w-1.5 h-1.5 rounded-full bg-current animate-pulse [animation-delay:-0.15s]" />
        <div className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
      </div>
      <p className="text-[11px] uppercase tracking-[0.2em] text-wood/40 font-medium">
        {message}
      </p>
    </div>
  );
}
