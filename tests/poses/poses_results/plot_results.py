import argparse
import matplotlib.pyplot as plt
import os

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Check file contents and plot results.")
    parser.add_argument("correct_content", type=str, help="The correct content to check for in the files.")
    args = parser.parse_args()

    correct_content = args.correct_content
    num_files = 9  # Assuming there are 9 files to check

    correct_content_count = 0
    incorrect_content_count = 0

    for i in range(1, num_files + 1):
        # Construct the directory and file path
        file_dir = f"./{correct_content}/"
        file_path = os.path.join(file_dir, f"{correct_content}{i}.txt")

        try:
            # Open and read the file
            with open(file_path, 'r') as file:
                content = file.read().strip()

            

            # Check if the content matches the correct content
            if content == correct_content:
                correct_content_count += 1
            else:
                incorrect_content_count += 1
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            incorrect_content_count += 1

    # Data for the pie chart
    labels = 'Correct Content', 'Incorrect Content'
    sizes = [correct_content_count, incorrect_content_count]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)  # explode the first slice (Correct Content)

    # Plot the pie chart
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
    plt.title("Content Check of Files")
    plt.show()

if __name__ == "__main__":
    main()
