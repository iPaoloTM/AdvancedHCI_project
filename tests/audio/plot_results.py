import os
import roman
import matplotlib.pyplot as plt

# List of file numbers
file_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,13, 20 ,52, 8,3 ,50, 100, 128, 256, 500, 503, 1000, 1095, 1952, 2024]

# Function to check if content matches expected Roman numeral
def check_content(file_number):

    expected_roman = roman.toRoman(file_number)

    try:
        with open(os.path.join("./audio_results/", str(file_number)+".txt"), 'r') as file:
            content = file.read().strip()
            return content == expected_roman
    except FileNotFoundError:
        print(f"File "+str(file_number)+".txt, not found.")
        return False

# Count correct and incorrect matches
correct_count = 0
incorrect_count = 0
results = {}

for number in file_numbers:
    if check_content(number):
        correct_count += 1
        results[number] = "Correct"
    else:
        incorrect_count += 1
        results[number] = "Incorrect"

# Plotting pie chart
labels = ['Correct', 'Incorrect']
sizes = [correct_count, incorrect_count]
colors = ['green', 'red']
explode = (0.1, 0)  # explode 1st slice

plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title('Matching Content in Files')
plt.show()

# Print results
print("Results:")
for number, result in results.items():
    print(f"{number}.txt: {result}")
