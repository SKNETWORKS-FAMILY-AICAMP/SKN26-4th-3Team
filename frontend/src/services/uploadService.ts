/**
 * @file uploadService.ts
 * @description 이미지를 클라우드 스토리지(S3/R2)에 업로드하는 과정을 시뮬레이션하는 서비스입니다.
 */

/**
 * 이미지를 업로드하고 저장된 원격 URL을 반환합니다.
 * @param base64OrFile 업로드할 이미지 데이터
 * @returns {Promise<string>} 업로드된 이미지의 가짜 S3 URL
 */
export const uploadToCloudStorage = async (base64OrFile: string | File): Promise<string> => {
  console.log("Uploading image to cloud storage...", typeof base64OrFile);
  // 네트워크 지연 시뮬레이션 (1.5초)
  await new Promise((resolve) => setTimeout(resolve, 1500));

  // 실제 환경에서는 여기서 AWS S3 SDK나 Cloudflare R2 API를 호출합니다.
  // 시뮬레이션을 위해 고유 ID가 포함된 가짜 URL을 생성합니다.
  const uniqueId = Math.random().toString(36).substring(7);
  const fakeUrl = `https://s3.ap-northeast-2.amazonaws.com/olfit-assets/user-uploads/aura-${uniqueId}.jpg`;

  console.log("Cloud Storage Upload Success:", fakeUrl);
  return fakeUrl;
};
