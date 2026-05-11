import { Loader2 } from "lucide-react";

interface LoadingSpinnerProps {
  message?: string;
  className?: string;
}

export default function LoadingSpinner({ message = "Loading...", className = "" }: LoadingSpinnerProps) {
  return (
    <div className={`flex flex-col items-center justify-center p-8 gap-4 ${className}`}>
      <Loader2 className="w-8 h-8 animate-spin text-wood" strokeWidth={1.5} />
      <p className="text-[11px] uppercase tracking-[0.2em] text-wood/40 font-medium">
        {message}
      </p>
    </div>
  );
}
