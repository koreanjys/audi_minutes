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

def extract_features(audio_file, segment_duration_sec=7):
    try:
        y, sr = librosa.load(audio_file)
    except Exception as exc:
        print(f"Error occurred while loading audio file: {exc}")
        return np.zeros((128, segment_duration_sec * sr // 512 + 1))

    hop_length = segment_duration_sec * sr // (128 - 1)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20, hop_length=hop_length)
    return mfcc, sr, hop_length

def compute_similarity_by_segments(feature1, feature2, sr, hop_length, duration_sec=7):
    if feature1 is None or feature2 is None:
        return False

    min_rows = min(feature1.shape[0], feature2.shape[0])
    min_cols = min(feature1.shape[1], feature2.shape[1])  # 범위를 벗어나지 않도록 열의 최소 크기를 가져옵니다.
    feature1 = feature1[:min_rows, :min_cols]
    feature2 = feature2[:min_rows, :min_cols]

    threshold = 0.4

    required_duration = duration_sec
    
    duration_count = 0
    for i in range(min_cols):  # 최소 열 크기를 사용하여 루프를 실행합니다.
        try:
            similarity = cosine(feature1[:, i], feature2[:, i])
        except ValueError:
            similarity = 0

        if similarity < threshold:
            time_diff = librosa.frames_to_time([1], sr=sr, hop_length=hop_length)[0]
            duration_count += time_diff
            if duration_count >= required_duration:
                return True
        else:
            duration_count = 0
    return False


def is_video_similar(entry, video_group, extracted_features, sr, hop_length):
    for video_index in video_group:
        if compute_similarity_by_segments(
            extracted_features[entry][0], extracted_features[video_index][0], sr, hop_length
        ):
            return True
    return False

def group_similar_videos(extracted_features, video_files):
    groups = []

    for i in range(len(extracted_features)):
        added_to_group = False
        for group in groups:
            if is_video_similar(i, group, extracted_features, extracted_features[i][1], extracted_features[i][2]):
                group.append(i)
                added_to_group = True
                break

        if not added_to_group:
            groups.append([i])

    grouped_videos = []
    for group in groups:
        grouped_videos.append([video_files[index] for index in group])

    return grouped_videos

def main(video_files):
    extracted_features = []

    for video in video_files:
        output_audio_file = 'temp_audio.wav'
        extract_audio_from_video(video, output_audio_file)

        features, sr, hop_length = extract_features(output_audio_file)
        extracted_features.append((features, sr, hop_length))

    groups = group_similar_videos(extracted_features, video_files)

    print("Grouped similar audio videos:", groups)
    return groups

def move_videos_to_folders(groups):
    output_folder = 'grouped_videos'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, group in enumerate(groups):
        group_folder = os.path.join(output_folder, f'group_{i + 1}')
        if not os.path.exists(group_folder):
            os.makedirs(group_folder)

        for video_file in group:
            dst = os.path.join(group_folder, os.path.basename(video_file))
            shutil.copyfile(video_file, dst)

    print(f"Successfully moved {len(groups)} groups of similar videos into '{output_folder}' folder.")

folder_path = "videos"
video_files = [
    os.path.join(folder_path, video)
    for video in os.listdir(folder_path)
    if video.endswith(".mp4")
]

if __name__ == "__main__":
    groups = main(video_files)
    move_videos_to_folders(groups)
