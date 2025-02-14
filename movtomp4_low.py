import cv2
import subprocess
import os

def speed_up_video(input_path, output_path, speed_factor=2):
    # 경로 확장
    input_path = os.path.expanduser(input_path)
    output_path = os.path.expanduser(output_path)
    
    # 입력 파일 확인
    if not os.path.exists(input_path):
        print(f"❌ 오류: 입력 파일이 존재하지 않습니다: {input_path}")
        return

    # 비디오 파일 열기
    cap = cv2.VideoCapture(input_path)
    
    # 원본 비디오 속성 가져오기
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # 초당 프레임 수
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 비디오 가로 크기
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 비디오 세로 크기
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 총 프레임 수

    if total_frames == 0 or width == 0 or height == 0:
        print("❌ 오류: 비디오 파일을 읽을 수 없습니다.")
        cap.release()
        return

    # 출력 비디오 설정 (코덱, 프레임 속도 변경)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # MP4 코덱
    temp_output = "temp_speedup.mov"  # 2배속 MOV 파일 저장 경로
    out = cv2.VideoWriter(temp_output, fourcc, fps * speed_factor, (width, height))

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # 2배속: 일부 프레임 건너뛰고 저장
        if frame_count % speed_factor == 0:
            out.write(frame)

        frame_count += 1

    # 자원 해제
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # 2배속 비디오가 생성되었는지 확인
    if not os.path.exists(temp_output):
        print("❌ 오류: 2배속 영상 저장 실패 (파일이 존재하지 않음)")
        return

    print("✅ 2배속 비디오 저장 완료! MOV 파일 변환 중...")

    # OpenCV로 처리한 MOV를 MP4로 변환
    convert_mov_to_mp4(temp_output, output_path)

def convert_mov_to_mp4(input_path, output_path):
    """FFmpeg를 사용하여 MOV를 MP4로 변환"""
    if not os.path.exists(input_path):
        print(f"❌ 오류: 변환할 파일이 존재하지 않습니다: {input_path}")
        return

    command = [
        "ffmpeg", "-y", "-i", input_path,
        "-vcodec", "h264",
        "-acodec", "aac",
        output_path
    ]
    subprocess.run(command)

    # 변환 후 임시 MOV 파일 삭제
    if os.path.exists(input_path):
        os.remove(input_path)

    print("✅ MOV → MP4 변환 완료!")

# 사용 예제
input_video = "~/Documents/협동2/협동2_study_finshed_video/원본/ver2_cup_stacking_원본.MOV"  # 원본 비디오 파일 경로
output_video = "~/Documents/협동2/협동2_study_finshed_video/cup_stacking_ver2_0215.mp4"  # 변환된 비디오 저장 경로 (특수 문자 제거)
speed_up_video(input_video, output_video, speed_factor=2)

print("🎉 최종 MP4 변환 완료!")
