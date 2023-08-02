import os
import cv2
import time

def open_video(file_path:str):
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        print(f"Error opening video: {file_path}")
        return None
    return cap

def remove_existing():
    if not os.path.exists(os.path.dirname(r'/Users/rishabhxpandey/Desktop/agrofocal-prework/single_process/')):
        os.makedirs(os.path.dirname(r'/Users/rishabhxpandey/Desktop/agrofocal-prework/single_process/'))

    output_file = r'/Users/rishabhxpandey/Desktop/agrofocal-prework/single_process/combined.mp4'
    if os.path.exists(output_file):
        os.remove(output_file)

def release_video(cap):
    if cap is not None:
        cap.release()

def merge_videos(vid1:str, vid2:str, fps=30):
    cap1 = open_video(vid1)
    cap2 = open_video(vid2)

    height, width, fps = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap1.get(cv2.CAP_PROP_FPS)) 

    # print(height_1, width_1, height_2, width_2)
    # ->      1920    1080     1920      1080
    # print(fps1, fps2)
    # ->     30    30

    remove_existing()

    fourcc_mov = cv2.VideoWriter_fourcc(*'mp4v')
    video_out = cv2.VideoWriter(r'/Users/rishabhxpandey/Desktop/agrofocal-prework/single_process/combined.mp4', fourcc_mov, fps, (width, height))

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        # roll over the excess frames from each vid
        if not ret1 and not ret2:
            break
        if ret1:
            video_out.write(frame1)
        if ret2:
            video_out.write(frame2)

    print('saved video')
    release_video(cap1)
    release_video(cap2)
    video_out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Running')
    start = time.time()
    merge_videos('clip1.MOV', 'clip2.MOV')
    end = time.time()
    print(f"Time Elapsed: {(end-start):.3f} seconds")


'''
possible errors
- error: fps and vid size errors causing issues. 
- fix: record from phone to keep it consistent
- but: why is there no video when you write only one vid frame?

- error: existing file is causing issue?
- fix: write code to delete video before it runs

- conclusion: issue fixed after fixing size and changing fourcc codec
'''