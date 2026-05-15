/**
 * @file ImageUploader.tsx
 * @description 이미지를 업로드하고 리사이징하여 Base64로 변환하는 컴포넌트입니다.
 * 사용자의 OOTD 사진을 받아 AI 분석이 가능한 형태로 전처리합니다.
 */

import { useState, useRef, type ChangeEvent, type DragEvent } from "react";
import { Upload, X, ImageIcon, AlertCircle, Sparkles } from "lucide-react";
import { uploadToCloudStorage } from "@/services/uploadService";

interface ImageUploaderProps {
  /** 이미지 처리가 완료되었을 때 호출되는 콜백 (Base64 및 원격 URL 전달) */
  onImageProcessed: (base64: string, remoteUrl: string) => void;
  /** 현재 AI 분석이 진행 중인지 여부 */
  isAnalyzing: boolean;
}

export default function ImageUploader({ onImageProcessed, isAnalyzing }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [processedImage, setProcessedImage] = useState<{ base64: string; remoteUrl: string } | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const uploadProcessingRef = useRef(false);

  const resetFileInput = () => {
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const releaseUploadLock = () => {
    uploadProcessingRef.current = false;
    setIsUploading(false);
  };

  const failUpload = (message: string) => {
    setError(message);
    releaseUploadLock();
    resetFileInput();
  };

  /**
   * 🛠️ REFACTOR (보안 강화): 파일의 바이너리 헤더(Magic Number)를 확인하여 
   * 위조된 확장자를 가진 악성 파일(Web Shell 등)의 업로드를 차단합니다.
   */
  const validateFileSignature = async (file: File): Promise<boolean> => {
    const header = await new Promise<string>((resolve) => {
      const reader = new FileReader();
      reader.onloadend = (e) => {
        if (!e.target?.result || !(e.target.result instanceof ArrayBuffer)) return resolve("");
        const arr = new Uint8Array(e.target.result).subarray(0, 4);
        let header = "";
        for (let i = 0; i < arr.length; i++) {
          header += arr[i].toString(16);
        }
        resolve(header.toLowerCase());
      };
      reader.readAsArrayBuffer(file.slice(0, 4));
    });

    // Magic Numbers: JPEG(ffd8ffe0/1/2/3/8), PNG(89504e47), WEBP(52494646)
    const signatures: Record<string, string[]> = {
      "image/jpeg": ["ffd8ff"],
      "image/png": ["89504e47"],
      "image/webp": ["52494646"]
    };

    const fileType = file.type;
    return signatures[fileType]?.some(sig => header.startsWith(sig)) ?? false;
  };

  /**
   * 이미지 리사이징 및 클라우드 업로드 시뮬레이션
   */
  const processImage = async (file: File) => {
    if (uploadProcessingRef.current || isUploading || isAnalyzing) return; // 🚨 FIX: POST 중복 요청 방지

    uploadProcessingRef.current = true;
    
    // 🛡️ SECURITY FIX: 허용된 이미지 MIME 타입 및 확장자 엄격 검사
    const allowedTypes = ["image/jpeg", "image/png", "image/webp"];
    const allowedExtensions = ["jpg", "jpeg", "png", "webp"];
    const fileExtension = file.name.split(".").pop()?.toLowerCase();

    if (!allowedTypes.includes(file.type) || !fileExtension || !allowedExtensions.includes(fileExtension)) {
      failUpload("JPG, PNG, WEBP 형식의 이미지만 업로드 가능합니다.");
      return;
    }

    // 🛠️ REFACTOR (보안 강화): 바이너리 시그니처 검증으로 파일 위조 차단
    let isValidSignature = false;
    try {
      isValidSignature = await validateFileSignature(file);
    } catch {
      failUpload("파일을 검증하는 중 오류가 발생했습니다.");
      return;
    }

    if (!isValidSignature) {
      failUpload("유효하지 않은 이미지 파일입니다. 파일 내용이 손상되었거나 위조되었습니다.");
      return;
    }

    // 🛡️ SECURITY FIX: 파일 크기 제한 (10MB) 설정하여 Image Bomb 및 DOS 공격 방어
    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
    if (file.size > MAX_FILE_SIZE) {
      failUpload("파일 크기는 10MB 이하만 가능합니다.");
      return;
    }

    setError(null);
    setProcessedImage(null);
    const reader = new FileReader();
    
    reader.onload = async (event) => {
      if (!event.target?.result || typeof event.target.result !== "string") {
        failUpload("파일을 읽는 중 오류가 발생했습니다.");
        return;
      }

      const img = new Image();
      img.onload = async () => {
        try {
          // 🛡️ SECURITY FIX: 캔버스 크기 상한선 강제 적용 (비정상적으로 큰 이미지의 픽셀 공격 방어)
          const MAX_CANVAS_SIZE = 4096;
          if (img.width > MAX_CANVAS_SIZE || img.height > MAX_CANVAS_SIZE) {
            failUpload("이미지 해상도가 너무 높습니다.");
            return;
          }

          const canvas = document.createElement("canvas");
          const MAX_WIDTH = 1200; 
          const MAX_HEIGHT = 1200;
          let width = img.width;
          let height = img.height;

          if (width > height) {
            if (width > MAX_WIDTH) {
              height *= MAX_WIDTH / width;
              width = MAX_WIDTH;
            }
          } else {
            if (height > MAX_HEIGHT) {
              width *= MAX_HEIGHT / height;
              height = MAX_HEIGHT;
            }
          }

          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext("2d");
          if (!ctx) {
            failUpload("이미지 처리 중 오류가 발생했습니다.");
            return;
          }
          ctx.drawImage(img, 0, 0, width, height);
          
          const base64 = canvas.toDataURL("image/jpeg", 0.9);
          setPreview(base64);
          
          // 클라우드 업로드 시뮬레이션 시작
          setIsUploading(true);
          const remoteUrl = await uploadToCloudStorage(base64);
          setProcessedImage({ base64, remoteUrl });
          releaseUploadLock(); // 🚨 FIX: POST 중복 요청 방지
        } catch {
          failUpload("이미지 처리 중 오류가 발생했습니다.");
        }
      };
      
      // 🛡️ SECURITY FIX: onerror 핸들러 추가하여 이미지 로딩 실패 시 자원 해제
      img.onerror = () => {
        failUpload("이미지를 불러올 수 없습니다. 파일이 손상되었거나 올바른 형식이 아닙니다.");
      };

      img.src = event.target.result;
    };

    // 🛡️ SECURITY FIX: FileReader 오류 핸들링 추가
    reader.onerror = () => {
      failUpload("파일을 읽는 중 오류가 발생했습니다.");
    };

    reader.readAsDataURL(file);
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      processImage(e.target.files[0]);
    }
  };

  const handleDragOver = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processImage(e.dataTransfer.files[0]);
    }
  };

  const removeImage = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setPreview(null);
    setProcessedImage(null);
    releaseUploadLock();
    setError(null);
    resetFileInput();
  };

  const startAnalysis = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!processedImage || isUploading || isAnalyzing) return;
    onImageProcessed(processedImage.base64, processedImage.remoteUrl);
  };

  return (
    <div className="w-full max-w-xl mx-auto">
      {error && (
        <div className="mb-4 p-3 bg-red-500/10 border border-red-500/20 rounded-sm flex items-center gap-2 text-red-400 text-[12px]">
          <AlertCircle size={14} />
          {error}
        </div>
      )}

      {!preview ? (
        <label
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`relative aspect-video flex flex-col items-center justify-center border-2 border-dashed transition-all duration-300 cursor-pointer rounded-sm ${
            isDragging ? "border-wood bg-cream/20" : "border-cream/20 bg-white/10 hover:bg-white/20"
          }`}
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept="image/*"
            className="hidden"
          />
          <div className="flex flex-col items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-cream/10 flex items-center justify-center">
              <Upload className="text-cream/60 w-6 h-6" />
            </div>
            <div className="text-center">
              <p className="text-[13px] font-medium text-cream mb-1">
                이곳을 클릭하여 OOTD 사진을 업로드하세요
              </p>
              <p className="text-[11px] text-cream/40 uppercase tracking-wider">
                Click to browse or Drag & Drop
              </p>
            </div>
          </div>
        </label>
      ) : (
        <div className="space-y-5">
          <div className="relative aspect-video bg-black/5 rounded-sm overflow-hidden group">
            <img src={preview} alt="Preview" className="w-full h-full object-cover" />
            
            {/* 오버레이 컨트롤 (분석 중이 아닐 때만 삭제 버튼 노출) */}
            {!isAnalyzing && (
              <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                <button
                  type="button"
                  onClick={removeImage}
                  className="p-3 bg-cream text-wood rounded-full hover:scale-110 shadow-lg transition-transform"
                  title="이미지 제거"
                >
                  <X size={20} />
                </button>
              </div>
            )}

            {/* 업로드 중 상태 표시 */}
            {isUploading && (
              <div className="absolute inset-0 bg-gold/40 backdrop-blur-sm flex flex-col items-center justify-center text-wood">
                <div className="flex items-center gap-1.5 mb-6">
                  <div className="w-1.5 h-1.5 rounded-full bg-current animate-pulse [animation-delay:-0.3s]" />
                  <div className="w-1.5 h-1.5 rounded-full bg-current animate-pulse [animation-delay:-0.15s]" />
                  <div className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
                </div>
                <p className="text-[13px] font-bold tracking-widest uppercase">Uploading to S3...</p>
                <p className="text-[11px] opacity-70 mt-2">안전한 서버로 이미지를 전송 중입니다</p>
              </div>
            )}

            {/* 분석 중 상태 표시 */}
            {isAnalyzing && (
              <div className="absolute inset-0 bg-wood/60 backdrop-blur-sm flex flex-col items-center justify-center text-cream">
                <div className="flex items-center gap-1.5 mb-6">
                  <div className="w-1.5 h-1.5 rounded-full bg-current animate-pulse [animation-delay:-0.3s]" />
                  <div className="w-1.5 h-1.5 rounded-full bg-current animate-pulse [animation-delay:-0.15s]" />
                  <div className="w-1.5 h-1.5 rounded-full bg-current animate-pulse" />
                </div>
                <p className="text-[13px] font-medium tracking-widest uppercase">Analyzing your style...</p>
                <p className="text-[11px] text-cream/60 mt-2">AI가 당신의 무드를 해석하고 있습니다</p>
              </div>
            )}
          </div>

          {!isAnalyzing && (
            <div className="grid grid-cols-1 sm:grid-cols-[1fr_auto] gap-3">
              <button
                type="button"
                onClick={startAnalysis}
                disabled={isUploading || !processedImage}
                className="h-12 inline-flex items-center justify-center gap-3 rounded-sm bg-wood px-8 text-[11px] font-bold uppercase tracking-widest text-cream border border-cream/15 shadow-[0_12px_30px_rgba(33,24,18,0.24)] transition-all duration-300 hover:bg-cream hover:text-wood disabled:cursor-not-allowed disabled:opacity-45 disabled:hover:bg-wood disabled:hover:text-cream"
              >
                <Sparkles size={14} />
                <span>{isUploading ? "업로드 중" : "분석 시작"}</span>
              </button>
              <button
                type="button"
                onClick={removeImage}
                className="h-12 inline-flex items-center justify-center rounded-sm border border-cream/20 px-8 text-[11px] font-medium uppercase tracking-widest text-cream/70 transition-all duration-300 hover:bg-cream/10 hover:text-cream"
              >
                초기화
              </button>
            </div>
          )}
        </div>
      )}
      
      <div className="mt-6 flex items-start gap-3 px-2">
        <ImageIcon size={14} className="text-cream/30 mt-0.5" />
        <p className="text-[11px] text-cream/40 leading-relaxed break-keep">
          정면 전신사진 혹은 의상의 질감과 색상이 잘 드러나는 사진일수록 더욱 정교한 분석이 가능합니다. <br />업로드된 이미지는 분석 즉시 경량화되어 안전하게 처리됩니다.
        </p>
      </div>
    </div>
  );
}

// EOF: ImageUploader.tsx
