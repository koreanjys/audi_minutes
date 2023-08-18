import numpy as np
import os
import sys
import librosa
import ffmpeg
import io
import shutil
from scipy.spatial.distance import cosine
from moviepy.editor import VideoFileClip

ffmpeg_exec_path = os.path.join(os.path.dirname(sys.executable), "ffmpeg", "bin")
os.environ['PATH'] = ffmpeg_exec_path + os.pathsep + os.environ['PATH']


def extract_audio_from_video(video_file, output_audio_file):
    video = VideoFileClip(video_file)
    audio = video.audio
    audio.write_audiofile(output_audio_file)


def segment_audio(y, sr, segment_duration_sec):
    n_samples_per_segment = int(sr * segment_duration_sec)
    n_segments = len(y) // n_samples_per_segment

    segments = []
    for i in range(n_segments):
        start_sample = i * n_samples_per_segment
        end_sample = start_sample + n_samples_per_segment
        segment = y[start_sample:end_sample]
        segments.append(segment)

    return segments


def extract_features(audio_file, segment_duration_sec=3):
    try:
        y, sr = librosa.load(audio_file)
    except Exception as exc:
        print(f"Error occurred while loading audio file: {exc}")
        return np.zeros((128, segment_duration_sec * sr // 512 + 1))

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)  # 20개의 MFCC 계수를 추출합니다.
    return mfcc


def compute_similarity_by_segments(feature1, feature2):
    if feature1 is None or feature2 is None:
        return 0

    min_rows = min(feature1.shape[0], feature2.shape[0])
    feature1 = feature1[:min_rows]
    feature2 = feature2[:min_rows]

    score = np.mean([cosine(feature1[:, i], feature2[:, i]) for i in range(feature1.shape[1])])
    return score


def main(video_files):
    extracted_features = []
    for video in video_files:
        output_audio_file = 'temp_audio.wav'
        extract_audio_from_video(video, output_audio_file)

        features = extract_features(output_audio_file)
        extracted_features.append(features)

    threshold = 0.15
    same_audio_videos = []

    for i in range(len(extracted_features)):
        for j in range(i + 1, len(extracted_features)):
            similarity = compute_similarity_by_segments(extracted_features[i], extracted_features[j])

            if similarity < threshold:
                same_audio_videos.append((video_files[i], video_files[j]))

    print("Same audio videos:", same_audio_videos)
    return same_audio_videos


def move_videos_to_folders(same_audio_videos_list):
    output_folder = 'grouped_videos'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, videos in enumerate(same_audio_videos_list):
        group_folder = os.path.join(output_folder, f'group_{i + 1}')
        if not os.path.exists(group_folder):
            os.makedirs(group_folder)

        for video_file in videos:
            dst = os.path.join(group_folder, os.path.basename(video_file))
            shutil.copyfile(video_file, dst)

    print(f"Successfully moved {len(same_audio_videos_list)} groups of similar videos into '{output_folder}' folder.")


folder_path = "videos"
video_files = [
    os.path.join(folder_path, video)
    for video in os.listdir(folder_path)
    if video.endswith(".mp4")
]

if __name__ == "__main__":
    main_video_files = main(video_files)
    move_videos_to_folders(main_video_files)
