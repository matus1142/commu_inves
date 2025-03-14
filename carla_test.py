import carla
import time
import numpy as np
import pygame
from pygame.locals import K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT

# Initialize the CARLA client and world
client = carla.Client('localhost', 3000)  # Make sure CARLA server is running
client.set_timeout(10.0)
world = client.get_world()

# Load the vehicle blueprint and spawn the car
blueprint_library = world.get_blueprint_library()
vehicle_bp = blueprint_library.filter('vehicle')[0]  # Choose a vehicle (e.g., Tesla)

# Set spawn location for the vehicle
spawn_points = world.get_map().get_spawn_points()
spawn_point = spawn_points[0]  # Choose a spawn point

vehicle = world.spawn_actor(vehicle_bp, spawn_point)

# Add a camera sensor to the vehicle
camera_bp = blueprint_library.find('sensor.camera.rgb')
camera_bp.set_attribute('image_size_x', '640')  # Set camera resolution
camera_bp.set_attribute('image_size_y', '480')
camera_location = carla.Transform(carla.Location(x=1.5, z=1.5))  # Camera location in front of the car
camera = world.spawn_actor(camera_bp, camera_location, attach_to=vehicle)

# Initialize pygame window for displaying the camera image
pygame.init()
screen = pygame.display.set_mode((640, 480), pygame.HWSURFACE | pygame.DOUBLEBUF)  # Swap width & height
clock = pygame.time.Clock()

# Function to convert CARLA image to Pygame surface
def process_image(image):
    # Convert image to array
    array = np.frombuffer(image.raw_data, dtype=np.uint8)
    array = np.reshape(array, (image.height, image.width, 4))
    array = array[:, :, :3]  # Discard alpha channel
    
    # Rotate image 90 degrees clockwise
    array = np.rot90(array, k=-1)  # k=-1 rotates 90 degrees clockwise
    
    # Mirror the image (flip horizontally)
    array = np.fliplr(array)  # Use np.flipud(array) for vertical flipping
    
    # Convert to Pygame surface
    surface = pygame.surfarray.make_surface(array)
    return surface

# Function to display camera image on Pygame window
def display_camera_image(image):
    surface = process_image(image)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

# Start the camera sensor
camera.listen(lambda image: display_camera_image(image))

# Function to control the car
def control_vehicle(vehicle):
    keys = pygame.key.get_pressed()
    
    # Create a control object
    control = carla.VehicleControl()
    
    # Accelerate
    if keys[K_UP]:
        control.throttle = 0.5  # Half throttle
    else:
        control.throttle = 0.0  # No acceleration
    
    # Brake
    if keys[K_DOWN]:
        control.brake = 0.5  # Half braking
    else:
        control.brake = 0.0
    
    # Steering
    if keys[K_LEFT]:
        control.steer = -0.3  # Turn left
    elif keys[K_RIGHT]:
        control.steer = 0.3  # Turn right
    else:
        control.steer = 0.0  # Straight

    # Apply the control to the vehicle
    vehicle.apply_control(control)

# Main loop for displaying the camera feed and controlling the vehicle
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == K_ESCAPE):
                raise KeyboardInterrupt
        
        # Control the vehicle
        control_vehicle(vehicle)

        # Limit frame rate to 30 FPS
        clock.tick_busy_loop(30)

finally:
    # Clean up
    camera.stop()
    vehicle.destroy()
    pygame.quit()
