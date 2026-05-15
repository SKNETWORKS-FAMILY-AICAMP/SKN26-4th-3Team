# 03. CSS vs Tailwind CSS

이 파트는 스타일링 기술 선택 이유를 설명합니다. 핵심 메시지는 “CSS의 원리를 그대로 사용하되, Tailwind CSS의 유틸리티 클래스와 디자인 토큰으로 팀 단위 UI 구현 속도와 일관성을 높였다”입니다.

## CSS 기초 개념

CSS는 HTML 구조에 색상, 폰트, 간격, 배치, 반응형 레이아웃 같은 시각적 스타일을 입히는 언어입니다.

```css
.primary-button {
  display: flex;
  padding: 12px 24px;
  background: #3d2b1f;
  color: #fcf9f5;
}
```

전통적인 CSS 방식에서는 의미 있는 클래스 이름을 만들고, 별도 CSS 파일에서 그 클래스에 스타일을 작성합니다. 이 방식은 명확하지만 프로젝트가 커지면 클래스 이름 충돌, 사용하지 않는 스타일 누적, 우선순위 문제를 관리해야 합니다.

## Tailwind CSS 기초 개념

Tailwind CSS는 미리 정의된 작은 유틸리티 클래스를 조합해 스타일을 작성하는 CSS 프레임워크입니다.

```tsx
<button className="inline-flex items-center px-6 py-3 bg-wood text-cream">
  분석 시작
</button>
```

`px-6`, `py-3`, `bg-wood`, `text-cream` 같은 클래스가 각각 padding, 배경색, 글자색을 의미합니다. 즉, CSS 파일에 매번 새 클래스명을 만들지 않고 JSX 안에서 바로 스타일을 조립합니다.

## CSS와 Tailwind CSS의 차이

| 구분 | 일반 CSS | Tailwind CSS |
| --- | --- | --- |
| 작성 위치 | 별도 CSS 파일 중심 | JSX className 중심 |
| 클래스 이름 | 직접 네이밍 필요 | 정해진 유틸리티 클래스 사용 |
| 스타일 충돌 | cascade와 specificity 관리 필요 | 원자 단위 클래스라 충돌 가능성이 낮음 |
| 디자인 일관성 | 개발자마다 값이 달라질 수 있음 | 설정 파일의 spacing, color, radius를 재사용 |
| 단점 | 커질수록 죽은 CSS 추적이 어려움 | className이 길어질 수 있음 |

## Olfit에서 Tailwind CSS를 선택한 이유

Olfit은 이미지, 리포트, 향수 카드, 모달, 스크롤 애니메이션이 많은 프론트엔드입니다. 화면별로 디자인 톤은 같지만 컴포넌트 종류가 많기 때문에 빠르게 조합하고 일관된 간격과 색을 유지하는 것이 중요했습니다.

Tailwind CSS를 선택한 이유는 다음과 같습니다.

1. 컴포넌트와 스타일을 같은 위치에서 읽을 수 있다.
2. `bg-wood`, `text-cream`, `border-wood/10`처럼 브랜드 색상을 일관되게 재사용한다.
3. `sm:`, `md:`, `lg:` 접두사로 모바일부터 데스크톱까지 반응형을 빠르게 구성한다.
4. 새 CSS 클래스 이름을 계속 만들지 않아도 되어 네이밍 비용이 줄어든다.
5. 사용한 클래스만 빌드 결과에 포함되어 CSS 크기를 관리하기 쉽다.

## 프로젝트 디자인 토큰

브랜드 컬러와 폰트는 `frontend/tailwind.config.js`에 확장되어 있습니다.

```js
colors: {
  gold: "#C9A96E",
  cream: "#FCF9F5",
  beige: "#F5F0E6",
  wood: "#3D2B1F",
  oak: "#8B5E3C",
}
```

전역 CSS 변수와 기본 스타일은 `frontend/src/index.css`에서 관리합니다.

- `@tailwind base`, `components`, `utilities`로 Tailwind 레이어를 활성화
- `:root`에 HSL 기반 색상 변수 정의
- `.label-upper`, `.hairline`, `.fade-up-entrance`, `.editorial-grid` 같은 프로젝트 공통 유틸리티 정의
- 스크롤바, 폰트 렌더링, text balance 등 전역 사용자 경험 처리

## 반응형 구현 방식

Tailwind는 모바일 기본 스타일을 먼저 쓰고, 화면이 커질수록 접두사로 확장합니다.

```tsx
<section className="py-24 md:py-40">
  <h2 className="text-2xl sm:text-4xl md:text-5xl">
    당신의 스타일을 보여주세요
  </h2>
</section>
```

위 코드는 기본 모바일에서는 작은 여백과 글자 크기를 쓰고, `md` 이상에서 더 큰 화면에 맞춰 확장합니다.

## Olfit에서 신경 쓴 스타일 디테일

- `cream`, `wood`, `gold` 중심의 향수 브랜드형 컬러 시스템을 만들었다.
- `rounded-sm`, 얇은 border, 낮은 opacity를 사용해 카드와 모달이 과하게 둥글거나 무겁지 않게 했다.
- `transition-all`, `duration-700`, `backdrop-blur` 등을 활용해 개인정보 동의 전 화면 blur와 모달 등장 효과를 만들었다.
- `break-keep`, `text-balance`로 한글 문장이 어색하게 끊기지 않도록 했다.
- `aspect-video`, `aspect-square`, `max-w-*`를 사용해 이미지 업로드 영역과 차트가 화면 크기에 따라 안정적으로 유지되게 했다.

## 발표할 때 강조할 점

Tailwind CSS는 CSS를 몰라도 쓰는 도구가 아니라, CSS의 속성을 작은 클래스 단위로 표준화해서 쓰는 방식입니다. Olfit에서는 이 방식으로 색상, 간격, 반응형, 애니메이션을 빠르게 조합하면서도 전체 화면의 브랜드 톤을 유지했습니다.

## Q&A 방어 포인트

Q. className이 너무 길어지는 단점은 없나요?

A. 있습니다. 그래서 반복되는 UI는 컴포넌트로 분리하고, 전역적으로 반복되는 패턴은 `index.css`의 `@layer components`에 공통 클래스로 정리했습니다.

Q. 일반 CSS보다 무조건 좋은가요?

A. 무조건 좋은 것은 아닙니다. 다만 이번 프로젝트처럼 컴포넌트가 많고 디자인 토큰을 반복 적용해야 하는 UI에서는 Tailwind가 개발 속도와 일관성 측면에서 유리했습니다.
