/**
 * @file main.tsx
 * @description 애플리케이션의 진입점(Entry Point)입니다.
 * React 프로젝트의 루트 요소를 렌더링하며, 전역 스타일 로드 및 라우팅 설정을 초기화합니다.
 */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router'
import './index.css' // 글로벌 테마 및 Tailwind CSS 스타일 로드
import App from './App.tsx' // 최상위 루트 컴포넌트 로드

/**
 * HTML의 'root' 요소를 찾아 React 애플리케이션을 마운트합니다.
 */
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    {/* 
      브라우저 라우팅을 위한 컨테이너 
      (현재는 단일 페이지 레이아웃이나, 추후 확장성을 위해 유지)
    */}
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)

// EOF: main.tsx
