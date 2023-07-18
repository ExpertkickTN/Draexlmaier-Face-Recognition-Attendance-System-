import os
import pygame
import pygame.camera

def take_and_save_picture(save_path):
    pygame.init()
    gameDisplay = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    icon_path = "assets/iconcamera.png"  # Replace with the path to your icon file
    icon_image = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_image)
    pygame.camera.init()
    cam = pygame.camera.Camera(0, (1280, 720))
    pygame.display.set_caption("Camera")  # Set the window caption as "Camera"
    cam.start()
    USER_INP = emailName_entry.get()
    capturing = False
    save_path = "Unknown/"+str(USER_INP)+".png"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cam.stop()
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Create the "Unknown" folder if it doesn't exist
                folder_name = os.path.dirname(save_path)
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)

                # Capture an image and save it as "photo.png" in the "Unknown" folder
                img = cam.get_image()
                pygame.image.save(img, save_path)
                print(f"Picture saved to {save_path}")
                capturing = True

        if capturing:
            break

        img = cam.get_image()
        gameDisplay.blit(img, (0, 0))
        pygame.display.update()

    cam.stop()
    pygame.quit()

if __name__ == "__main__":
    # Specify the path where you want to save the picture
    save_path = "Unknown/photo.png"

    # Call the function to capture an image from the camera and save it
    take_and_save_picture(save_path)
