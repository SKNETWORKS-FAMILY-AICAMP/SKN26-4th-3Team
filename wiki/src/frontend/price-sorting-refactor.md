# Price Sorting Refactor

추천 리스트의 가격순 정렬은 화면에 표시되는 `price` 문자열이 아니라 숫자 필드인 `price_krw`를 기준으로 처리한다.

## Why

향수 가격은 원화, 달러, 유로, 가격 미정 같은 다양한 형식으로 표시될 수 있다. 화면 표시용 문자열을 직접 파싱하면 통화 기호, 쉼표, 환율, 누락 값 때문에 정렬 오류가 생기기 쉽다.

그래서 UI 표시 값과 정렬 값을 분리한다.

```ts
{
  price: "$150",
  price_krw: 207000
}
```

## Implementation

정렬 로직은 `frontend/src/hooks/useInsightReport.ts`에 있다.

- `getSortablePriceKrw()`: 유효한 양수 가격만 정렬 값으로 인정한다.
- `compareByPriceKrw()`: 낮은 가격이 먼저 오도록 비교한다.
- `sortByPriceKrw()`: 원본 배열을 변경하지 않고 복사본을 정렬한다.

`price_krw`가 없거나 0 이하인 상품은 `Infinity`로 처리해 가격 정보가 있는 상품 뒤에 배치한다.

## Test

테스트는 `frontend/src/hooks/useInsightReport.test.ts`에서 관리한다.

검증하는 내용:

- 달러, 유로, 원화 표시 문자열이 섞여 있어도 `price_krw` 기준으로 정렬한다.
- 가격이 없거나 유효하지 않은 상품은 가격이 있는 상품 뒤로 보낸다.

## Presentation Point

가격 정렬은 단순 UI 기능처럼 보이지만, 표시용 데이터와 계산용 데이터를 분리한 사례다. 이 분리는 프론트엔드에서 국제화, 통화 변환, 데이터 누락을 다룰 때 중요한 안정성 포인트다.
