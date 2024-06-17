import threading
import cv2
from deepface import DeepFace

# Open the default camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Set the video frame width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

counter = 0

# Load the reference image
reference_img = cv2.imread("WIN_20240208_00_18_23_Pro.jpg")

# Variable to store the result of face matching
face_match = False

# Function to check if the face in the current frame matches the reference image
def check_face(frame):
    global face_match
    try:
        # Use DeepFace to verify if the face in the frame matches the reference image
        if DeepFace.verify(frame, reference_img.copy())['verified']:
            face_match = True
        else:
            face_match = False
    except ValueError:
        # If DeepFace doesn't recognize a face, it throws a ValueError
        face_match = False

# Main loop
while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    if ret:
        # Every 30 frames, start a new thread to check the face
        if counter % 30 == 0:
            try:
                threading.Thread(target=check_face, args=(frame.copy(),)).start()
            except ValueError:
                pass
        counter += 1

        # If the face matches, write "MATCH!" on the frame
        if face_match:
            cv2.putText(frame, "MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            # If the face doesn't match, write "NO MATCH!" on the frame
            cv2.putText(frame, "NO MATCH!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        # Display the frame
        cv2.imshow('video', frame)

    # If 'q' is pressed on the keyboard, exit the loop
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# After the loop, close any open windows
cv2.destroyAllWindows()
