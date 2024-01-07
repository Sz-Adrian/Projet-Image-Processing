import cv2 as cv
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    for i in range(9,20,4):
        if all([landmarks[i].y <landmarks[i+3].y ]): return "ROCK"
        elif landmarks[4].y <landmarks[2].y and landmarks[4].y < landmarks[9].y: return "OK"
        elif landmarks[i].y < landmarks[16].y and landmarks[17].y < landmarks[20].y: return "SCISSORS"
        else: return "PAPER"

cam = cv.VideoCapture(0)

clock = 0
p1 = p2 = None
scorep1 = scorep2 = 0
gameText=""
noPlayCount = 0
success = True
ready = False
with mp_hands.Hands(model_complexity=0,
                   min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:
    while True:

        ret,frame = cam.read()
        if not ret or frame is None: break
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        results = hands.process(frame)

        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame,
                                          hand_landmarks,
                                          mp_hands.HAND_CONNECTIONS,
                                          mp_drawing_styles.get_default_hand_landmarks_style(),
                                          mp_drawing_styles.get_default_hand_connections_style())
        frame = cv.flip(frame,1)
        if ready == False:
            hls=results.multi_hand_landmarks
            if hls and len(hls) == 2:
                print(f"P1 {getHandMove(hls[0])} ")
                print(f"P2 {getHandMove(hls[1])} ")
                if getHandMove(hls[0]) == "OK" and getHandMove(hls[1]) == "OK":
                    ready = True
                    print ("Its ok to draw")

        if ready == True:
            if 0 <= clock <20:
                success = True
                gameText = "Ready to play?"
                change = 0
            elif clock < 30: gameText = "3..."
            elif clock < 40: gameText = "2..."
            elif clock < 50: gameText = "1..."
            elif clock < 60: 
                gameText = "GOOOOOOOO!!!!!!!!!"
            elif clock == 60:
                hls=results.multi_hand_landmarks
                if hls and len(hls) == 2:
                    p1 = getHandMove(hls[0])
                    print(f"P1 {getHandMove(hls[0])} ")
                    print(f"P2 {getHandMove(hls[1])} ")
                    p2 = getHandMove(hls[1])
                else:
                    success = False
            elif clock < 200:
                if success and change == 0:
                    gameText = f"Player 1 played {p1} and PLayer 2 played {p2}."
                    
                    if p1 == p2: 
                        gameText = " Game is tied."
                    elif p1 == "PAPER" and p2 == "ROCK":
                        gameText = " Player 1 wins!"
                        change = 1
                        scorep1 += 1
                    elif p1 == "ROCK" and p2 == "SCISSORS": 
                        gameText = "Player 1 wins!"
                        change = 1
                        scorep1 += 1
                    elif p1 == "SCISSORS" and p2 == "PAPER":
                        gameText = " Player 1 wins!"
                        change = 1
                        scorep1 += 1
                    else: 
                        gameText = "Player 2 wins"
                        change = 1
                        scorep2 += 1
                        print(scorep1, scorep2)
                    noPlayCount = 0
                else:
                    if change == 0 and noPlayCount < 2:
                        gameText = "Present both of your weapons!"
                        noPlayCount = noPlayCount +1
                        change = 1
                        print(noPlayCount)
                        
                    elif change == 0 and noPlayCount < 5 and noPlayCount >= 2:
                        gameText = "Weapons are your hands!"
                        change = 1
                        noPlayCount = noPlayCount +1
                        print(noPlayCount)
                    elif change == 0 and noPlayCount == 5:
                        change = 1
                        gameText = "Did a Jedi cut off your hands?"
                        print(noPlayCount)
                        noPlayCount = 0
        else:
            gameText = "Put your thumbs up to begin playing"
            clock = 0

        #cv.putText(frame, f"Clock: {clock}",(50,50),cv.FONT_HERSHEY_PLAIN,1,(255,0,0),2,cv.LINE_AA)
        cv.putText(frame, f"Player 1 score: {scorep1}",(50,80),cv.FONT_HERSHEY_PLAIN,1,(255,0,0),2,cv.LINE_AA)
        cv.putText(frame, f"Player 2 score: {scorep2}",(50,100),cv.FONT_HERSHEY_PLAIN,1,(255,0,0),2,cv.LINE_AA)
        cv.putText(frame, gameText,(50,200),cv.FONT_HERSHEY_PLAIN,2,(0,0,255),2,cv.LINE_AA)
        clock = (clock + 1) % 100
        frame = cv.resize(frame, (1600, 900))  # Set the desired width and height
        cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'): break
cam.release()
cv.destroyAllWindows()