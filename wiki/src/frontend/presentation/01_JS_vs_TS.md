# 01. JavaScript vs TypeScript

이 파트는 프론트엔드 언어 선택 이유를 설명하는 발표 자료의 시작점입니다. 핵심 메시지는 “TypeScript는 JavaScript를 대체하는 완전히 다른 언어가 아니라, JavaScript에 타입 시스템을 더해 협업 안정성을 높인 언어”라는 것입니다.

## JavaScript 기초 개념

JavaScript는 브라우저에서 화면을 동적으로 바꾸고 사용자의 입력에 반응하게 만드는 웹 표준 프로그래밍 언어입니다. 버튼 클릭, 이미지 업로드, API 요청, 모달 열기, 애니메이션 같은 프론트엔드 동작은 결국 JavaScript로 실행됩니다.

JavaScript의 장점은 유연성입니다. 변수에 문자열을 넣었다가 숫자를 넣을 수도 있고, 객체 구조를 빠르게 바꿀 수도 있습니다. 하지만 프로젝트가 커지면 이 유연성이 오류의 원인이 됩니다.

```ts
let price = "458000";
price = 458000;
```

작은 코드에서는 문제가 없어 보이지만, 어떤 컴포넌트는 문자열 가격을 기대하고 다른 로직은 숫자 가격을 기대하면 정렬, 계산, 화면 표시에서 버그가 생깁니다.

## TypeScript 기초 개념

TypeScript는 JavaScript 문법 위에 타입을 추가한 언어입니다. 개발 중에 변수, 함수 인자, API 응답, 컴포넌트 props가 어떤 형태인지 미리 정의하고 검사합니다.

```ts
interface Product {
  id: number;
  name: string;
  brand: string;
  price: string;
  price_krw?: number;
}
```

위처럼 타입을 정의하면 `Product`를 사용하는 컴포넌트는 `name`, `brand`, `price` 같은 필드가 있다는 것을 전제로 안전하게 구현할 수 있습니다. 잘못된 필드를 쓰거나 필수 값을 누락하면 브라우저에서 실행하기 전 빌드 단계에서 오류를 확인할 수 있습니다.

## JavaScript와 TypeScript의 차이

| 구분 | JavaScript | TypeScript |
| --- | --- | --- |
| 실행 방식 | 브라우저가 직접 실행 | TypeScript가 JavaScript로 변환된 뒤 실행 |
| 타입 검사 | 런타임에 값이 들어와야 문제를 알 수 있음 | 개발 및 빌드 단계에서 타입 오류를 확인 |
| 협업 안정성 | 객체 구조를 문서나 약속으로 관리 | 인터페이스와 타입으로 코드에 계약을 명시 |
| 리팩토링 | 필드명 변경 시 누락을 찾기 어려움 | 타입 에러와 IDE 자동완성으로 추적 가능 |
| 단점 | 큰 프로젝트에서 데이터 구조 추적이 어려움 | 타입 작성 비용과 학습 비용이 있음 |

## Olfit에서 TypeScript를 선택한 이유

Olfit 프론트엔드는 사용자의 향기 취향, 이미지 분석 결과, 추천 상품, 리포트 데이터를 여러 컴포넌트가 공유합니다. 이 데이터들은 단순 문자열이 아니라 구조가 있는 객체입니다.

대표 타입은 `frontend/src/types/index.ts`에 정의되어 있습니다.

- `Product`: 향수 상품 카드와 상세 모달이 공통으로 사용하는 상품 구조
- `AnalysisResults`: 백엔드 분석 결과와 리포트 섹션이 사용하는 결과 구조
- `ScentType`: 분석 유형을 제한하는 유니온 타입

TypeScript를 사용한 이유는 다음과 같습니다.

1. 백엔드 응답과 프론트 UI 사이의 데이터 계약을 명확히 한다.
2. 추천 카드, 모달, 리포트가 같은 상품 타입을 공유하게 한다.
3. `price_krw`, `recommendations`, `radarScores`처럼 선택적으로 들어오는 값을 안전하게 다룬다.
4. 컴포넌트 props를 타입으로 제한해 잘못된 연결을 빌드 단계에서 발견한다.
5. 리팩토링 중 파일을 이동하거나 필드를 바꿔도 IDE와 컴파일러가 누락 지점을 알려준다.

## 프로젝트에서 적용한 방식

`tsconfig.app.json`은 `strict: true`로 설정되어 있습니다. 즉, 애매한 타입을 최대한 허용하지 않는 방향으로 작성합니다.

```json
{
  "compilerOptions": {
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "jsx": "react-jsx"
  }
}
```

`App.tsx`에서는 분석 완료 콜백의 결과 타입을 `AnalysisResults`로 고정합니다.

```tsx
<AIInterviewSection
  onComplete={(results: AnalysisResults) => setAnalysisResults(results)}
  selectedNotes={selectedNotes}
/>
```

이 덕분에 `AIInterviewSection`이 넘기는 값과 `InsightReportSection`이 읽는 값이 같은 구조라는 점을 코드로 보장할 수 있습니다.

## 발표할 때 강조할 점

TypeScript는 사용자가 보는 기능을 직접 추가하는 기술은 아니지만, 팀 프로젝트에서 기능이 깨지지 않게 만드는 안전장치입니다. Olfit에서는 백엔드 분석 결과, 추천 상품, 리포트 UI처럼 여러 파트가 공유하는 데이터를 타입으로 고정해 협업 중 생길 수 있는 필드명 불일치와 누락 오류를 줄였습니다.

## 한계와 보완

TypeScript는 컴파일 단계의 안전장치입니다. 서버에서 실제로 잘못된 JSON이 내려오면 런타임 검증이 추가로 필요합니다. 따라서 중요한 API 응답은 백엔드 계약 문서와 테스트, 필요하면 Zod 같은 런타임 스키마 검증으로 보완할 수 있습니다.
