import { AlertCircle, RefreshCw } from "lucide-react";

interface ErrorFallbackProps {
  message: string;
  onRetry?: () => void;
  className?: string;
}

export default function ErrorFallback({ message, onRetry, className = "" }: ErrorFallbackProps) {
  return (
    <div className={`flex flex-col items-center justify-center p-12 bg-red-50/50 border border-red-100 rounded-sm gap-6 ${className}`}>
      <div className="w-12 h-12 rounded-full bg-red-50 flex items-center justify-center">
        <AlertCircle className="text-red-500 w-6 h-6" />
      </div>
      <div className="text-center space-y-2">
        <h4 className="text-sm font-bold text-red-900 uppercase tracking-widest">Error Occurred</h4>
        <p className="text-[13px] text-red-700/70 break-keep max-w-xs mx-auto">
          {message}
        </p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="flex items-center gap-2 px-6 py-2.5 bg-red-600 text-white rounded-full text-[11px] uppercase tracking-widest hover:bg-red-700 transition-colors shadow-lg shadow-red-200"
        >
          <RefreshCw size={14} />
          Retry Request
        </button>
      )}
    </div>
  );
}
