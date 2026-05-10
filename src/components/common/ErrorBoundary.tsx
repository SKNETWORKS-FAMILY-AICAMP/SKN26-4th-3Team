import { Component, type ErrorInfo, type ReactNode } from "react";
import ErrorFallback from "./ErrorFallback";

interface Props {
  children?: ReactNode;
  fallbackMessage?: string;
}

interface State {
  hasError: boolean;
}

/**
 * @class ErrorBoundary
 * @description 하위 컴포넌트 트리의 런타임 에러를 포착하여 화이트 스크린 대신 에러 폴백 UI를 보여줍니다.
 */
class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(_: Error): State {
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="py-20 px-6">
          <ErrorFallback 
            message={this.props.fallbackMessage || "이 섹션을 불러오는 중 문제가 발생했습니다."} 
            onRetry={() => this.setState({ hasError: false })}
          />
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
