import subprocess
import re

def process_powershell_file(input_file, output_file):
    # Read the content of the input PowerShell file
    with open(input_file, 'r') as f:
        content = f.read()

    # Replace the "iex" command with "$command =" and remove the closing parenthesis
    modified_content = re.sub(r'iex\s*\(', '$command = ', content).rstrip(')')
    # Add a line to print the output of $command
    modified_content += '\nWrite-Output $command\n'

    # Save the modified content to a new PowerShell file
    with open(output_file, 'w') as f:
        f.write(modified_content)

    # Run the modified PowerShell script to evaluate the format string
    result = subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", output_file], capture_output=True, text=True)

    # Extract the evaluated $command value
    evaluated_command = result.stdout.strip()

    return evaluated_command

def main():
    input_file = "formatps.ps1"
    iteration = 1
    current_file = input_file

    while True:
        output_file = f"{iteration}.ps1"

        # Process the current PowerShell file and get the evaluated command
        evaluated_command = process_powershell_file(current_file, output_file)

        # Check if the evaluated command still contains a format string
        if '{' not in evaluated_command and '}' not in evaluated_command:
            print(f"Final result after {iteration} iterations: {evaluated_command}")
            break

        # Save the evaluated command as the new file for the next iteration
        with open(f"{iteration + 1}.ps1", 'w') as f:
            f.write(f"{evaluated_command}")

        # Update the file for the next iteration
        current_file = f"{iteration + 1}.ps1"
        iteration += 1

    print("Process complete.")

if __name__ == "__main__":
    main()
