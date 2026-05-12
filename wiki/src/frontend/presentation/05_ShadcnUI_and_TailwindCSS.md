# Shadcn UI & Tailwind CSS: 현대적 UI 구축 전략

## 1. 기존 UI 라이브러리 vs Shadcn UI

### 기존 UI 라이브러리 (MUI, Ant Design 등)
- **방식**: `yarn add`를 통해 라이브러리 전체를 의존성으로 추가.
- **특징**: 
  - 컴포넌트가 패키지 내부에 캡슐화되어 있어 내부 로직이나 스타일 수정이 어려움.
  - 사용하지 않는 컴포넌트까지 번들에 포함될 수 있음 (Tree-shaking이 되더라도 한계 존재).
  - 라이브러리 고유의 디자인 시스템에 종속됨.

### Shadcn UI
- **방식**: `npx shadcn-ui@latest add [component]` 명령어를 통해 컴포넌트 **소스 코드를 직접 프로젝트로 복사**.
- **특징**:
  - **소유권(Ownership)**: 컴포넌트 코드가 내 프로젝트 폴더(`src/components/ui`)에 직접 존재하므로 100% 커스터마이징 가능.
  - **Radix UI 기반**: 접근성(Accessibility)과 핵심 로직은 검증된 headless 라이브러리인 Radix UI를 사용.
  - **의존성 최소화**: 필요한 컴포넌트만 선택적으로 가져와 사용하므로 번들 사이즈가 효율적임.

---

## 2. Shadcn UI를 선택한 이유

1. **디자인 자유도**: Olfit(Persona:L) 프로젝트는 감각적이고 프리미엄한 브랜드 경험이 중요합니다. Shadcn UI는 스타일이 강제되지 않아 프로젝트의 브랜드 아이덴티티에 맞춰 스타일을 세밀하게 조정하기에 최적입니다.
2. **접근성(A11y)**: 복잡한 UI(Modal, Popover, Dropdown 등)를 직접 구현할 때 놓치기 쉬운 키보드 네비게이션, 웹 접근성 표준을 Radix UI 기반의 Shadcn UI가 완벽하게 제공합니다.
3. **코드 투명성**: 외부 라이브러리의 블랙박스 같은 동작 대신, 직접 코드를 읽고 수정할 수 있어 유지보수와 학습에 유리합니다.

---

## 3. Tailwind CSS와의 관계

Shadcn UI는 **"Tailwind CSS를 위한 컴포넌트 엔진"**이라고 할 수 있습니다.

- **스타일링 매개체**: Shadcn UI의 모든 스타일은 Tailwind CSS 클래스로 작성되어 있습니다.
- **일관된 설정**: `tailwind.config.js`에 정의된 테마(컬러, 폰트, 애니메이션 등)를 컴포넌트가 그대로 공유합니다.
- **class-variance-authority (CVA)**: Tailwind 클래스를 사용하여 컴포넌트의 variant(size, color, shape 등)를 체계적으로 관리합니다.
- **결합의 이점**: 
  - 별도의 CSS 파일 없이 유틸리티 클래스만으로 컴포넌트 디자인을 완성.
  - `cn()` 유틸리티 함수를 통해 조건부 스타일링과 클래스 병합을 안전하게 처리.

---

## 4. 요약
Shadcn UI는 라이브러리가 아닌 **"컴포넌트 모음집"**입니다. 이를 통해 개발자는 검증된 UI 로직(Radix UI) 위에 Tailwind CSS의 강력한 스타일링 능력을 결합하여, 빠르면서도 독창적인 UI를 구축할 수 있습니다.
