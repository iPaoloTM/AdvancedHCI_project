import pose
import speech2text
import text2speech

if __name__ == '__main__':
    number = speech2text.listen()

    poses=[]

    for x in number:
        poses.append(pose.findLetter(3))

    combined_string = "".join(poses)

    print("Success" if (combined_string==number) else "Failure")
