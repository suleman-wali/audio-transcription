Audio to Text Helper

This is a simple program that listens to your audio files and writes down what is being said. 

What can it do?

- Listen to Many Files: You can give it MP3, WAV, or other audio files.
- Smart Listening: It's good at ignoring silence so it doesn't get confused.
- Fast and Simple: It uses a very smart "brain" called Whisper to understand speech quickly.
- Works on Your Computer: It uses your normal computer processor (CPU), so you don't need a fancy gaming card.

How to use it?

Step 1: Install FFmpeg
The program needs a tool called "FFmpeg" to understand different audio sounds.

Step 2: Set it up
1. Open your computer's terminal.
2. Install the program's needs by typing:
   pip install -r requirements.txt
3. Start the helper:
   uvicorn app.main:app --reload

How to talk to the program?

The program lives at `http://localhost:8000`. Here is how to use it:

1. Upload: Send your audio file to `/upload`. It will give you a "Job ID" (a secret code).
2. Check: Give that secret code to `/status/{your_code}` to see if it's finished.
3. Get Text: Once it says "completed", go to `/transcript/{your_code}` to see your text!

Good to know
- Privacy: Everything stays on your computer.
- Errors: If the audio file is broken, the program will tell you.
- CPU only: Right now, this is made for normal computer brains (CPU). It's not for special graphics cards (GPU) yet.

