import multiprocessing
import multiprocessing.managers
import cv2
import time
import os

def read_video(video_path, queue):
    video = cv2.VideoCapture(video_path)
    while True:
        ret, frame = video.read()
        if not ret:
            break
        queue.put(frame)

    release_video(video)

def merge_frames(queue):
    combined_video = cv2.VideoWriter('multi_process/combined_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (1920, 1080))
    while True:
        try:
            frame = queue.get()
            if frame is None:
                break
            combined_video.write(frame)
        except EOFError:
            break
    combined_video.release()

def remove_existing():
    if not os.path.exists(os.path.dirname(r'/Users/rishabhxpandey/Desktop/agrofocal-prework/multi_process/')):
        os.makedirs(os.path.dirname(r'/Users/rishabhxpandey/Desktop/agrofocal-prework/multi_process/'))

    output_file = r'/Users/rishabhxpandey/Desktop/agrofocal-prework/multi_process/combined.mp4'
    if os.path.exists(output_file):
        os.remove(output_file)

def release_video(cap):
    if cap is not None:
        cap.release()

def main():
    remove_existing()
    manager = multiprocessing.Manager()
    queue = manager.Queue()
    processes = []
    for i in range(1,3):
        print(f'clip{i}.MOV')
        process = multiprocessing.Process(target=read_video, args=(f'clip{i}.MOV', queue,))
        processes.append(process)
    
    for p in processes:
        p.start()

    # Check if the queue is empty before starting the merge frames process
    if not queue.empty():
         raise ValueError('The queue is empty.')

    process = multiprocessing.Process(target=merge_frames, args=(queue,))
    process.start()

    for process in processes:
        process.join()
    
    cv2.destroyAllWindows()

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Running')
    print('FRESH----------------------------------')
    start = time.time()
    main()
    end = time.time()
    print(f"Time Elapsed: {(end-start):.3f} seconds")
