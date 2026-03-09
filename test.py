from dynamo_figures.video_to_gif import VideoToGif

# Create a GIF from a video
converter = VideoToGif(
    video_path="videos/icra2024-bcbf-intention.mp4",
    fps=15,
    start_t=2.0,
    end_t=5.0,
    scale=0.1,
    speed=1.5,
    reverse=True
)

# Convert and save
success = converter.convert("output.gif")

if success:
    print("GIF created successfully!")