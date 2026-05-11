/**
 * @file ImageUploader.tsx
 * @description 이미지를 업로드하고 리사이징하여 Base64로 변환하는 컴포넌트입니다.
 * 사용자의 OOTD 사진을 받아 AI 분석이 가능한 형태로 전처리합니다.
 */

import { useState, useRef, type ChangeEvent, type DragEvent } from "react";
import { Upload, X, ImageIcon, Loader2, AlertCircle } from "lucide-react";
import { uploadToCloudStorage } from "@/services/uploadService";

interface ImageUploaderProps {
  /** 이미지 처리가 완료되었을 때 호출되는 콜백 (Base64 및 원격 URL 전달) */
  onImageProcessed: (base64: string, remoteUrl: string) => void;
  /** 현재 AI 분석이 진행 중인지 여부 */
  isAnalyzing: boolean;
}

export default function ImageUploader({ onImageProcessed, isAnalyzing }: ImageUploaderProps) {
  const [preview, setPreview] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  /**
   * 이미지 리사이징 및 클라우드 업로드 시뮬레이션
   */
  const processImage = async (file: File) => {
    if (!file.type.startsWith("image/")) {
      setError("이미지 파일만 업로드 가능합니다.");
      return;
    }

    setError(null);
    const reader = new FileReader();
    
    reader.onload = async (event) => {
      const img = new Image();
      img.onload = async () => {
        try {
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
          if (!ctx) return;
          ctx.drawImage(img, 0, 0, width, height);
          
          const base64 = canvas.toDataURL("image/jpeg", 0.9);
          setPreview(base64);
          
          // 클라우드 업로드 시뮬레이션 시작
          setIsUploading(true);
          const remoteUrl = await uploadToCloudStorage(base64);
          setIsUploading(false);
          
          onImageProcessed(base64, remoteUrl);
        } catch (err) {
          setError("이미지 처리 중 오류가 발생했습니다.");
          setIsUploading(false);
        }
      };
      img.src = event.target?.result as string;
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
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processImage(e.dataTransfer.files[0]);
    }
  };

  const removeImage = () => {
    setPreview(null);
    setError(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
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
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
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
                오늘의 스타일(OOTD) 사진을 업로드하세요
              </p>
              <p className="text-[11px] text-cream/40 uppercase tracking-wider">
                Drag & Drop or Click to browse
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="relative aspect-video bg-black/5 rounded-sm overflow-hidden group">
          <img src={preview} alt="Preview" className="w-full h-full object-cover" />
          
          {/* 오버레이 컨트롤 (분석 중이 아닐 때만 삭제 버튼 노출) */}
          {!isAnalyzing && (
            <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
              <button
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
              <Loader2 className="w-8 h-8 animate-spin mb-4" />
              <p className="text-[13px] font-bold tracking-widest uppercase">Uploading to S3...</p>
              <p className="text-[11px] opacity-70 mt-2">안전한 서버로 이미지를 전송 중입니다</p>
            </div>
          )}

          {/* 분석 중 상태 표시 */}
          {isAnalyzing && (
            <div className="absolute inset-0 bg-wood/60 backdrop-blur-sm flex flex-col items-center justify-center text-cream">
              <Loader2 className="w-8 h-8 animate-spin mb-4" />
              <p className="text-[13px] font-medium tracking-widest uppercase">Analyzing your style...</p>
              <p className="text-[11px] text-cream/60 mt-2">AI가 당신의 무드를 해석하고 있습니다</p>
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
