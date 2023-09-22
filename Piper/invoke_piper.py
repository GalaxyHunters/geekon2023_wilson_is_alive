import subprocess

def invoke_piper(input_string, piper_path, voice_model_path):
    try:
        # Construct the command
        command = [
            'echo', input_string,
            '|', piper_path, '--model', voice_model_path, '--output-raw',
            '|', 'aplay', '-r', '22050', '-f', 'S16_LE', '-t', 'raw', '-'
        ]
        
        # Join the command into a single string
        full_command = ' '.join(command)
        
        # Run the command
        subprocess.run(full_command, shell=True, check=True)
    
    except subprocess.CalledProcessError as e:
        # Handle any errors that occur when running the command
        return f"Error: {e.returncode}, {e.output.strip()}"

if __name__ == "__main__":
    input_string = input("Enter a string: ")
    piper_path = input("Enter the path to the piper program: ")
    voice_model_path = input("Enter the path to the voice model: ")
    
    invoke_piper(input_string, piper_path, voice_model_path)

