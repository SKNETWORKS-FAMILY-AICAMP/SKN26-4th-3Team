interface ReportHeaderProps {
  isVisible: boolean;
}

export default function ReportHeader({ isVisible }: ReportHeaderProps) {
  return (
    <div className={`flex flex-col items-center mb-20 transition-all duration-800 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
      <p className="label-upper text-wood/40 mb-4">Diagnosis Report</p>
      <h2 className="text-3xl sm:text-4xl md:text-5xl font-light tracking-tight break-keep text-wood text-center">
        당신의 비주얼 아우라 진단
      </h2>
    </div>
  );
}
