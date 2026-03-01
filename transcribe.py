import mlx_whisper
import time

# Use the 'large-v3' model (most accurate) or 'turbo' (fastest)
# Since you have 64GB RAM, large-v3 will be instant for you.
MODEL_PATH = "mlx-community/whisper-large-v3-turbo"

def run_test(audio_file):
    print(f"--- Loading model: {MODEL_PATH} ---")
    start = time.time()
    
    # This automatically downloads the model the first time
    result = mlx_whisper.transcribe(audio_file, path_or_hf_repo=MODEL_PATH)
    
    end = time.time()
    print(f"--- Done in {end - start:.2f} seconds ---")
    print("\nTranscript:\n", result['text'])

if __name__ == "__main__":
    # Change 'test.wav' to any audio file you have handy
    run_test("test.wav")