import numpy as np
import matplotlib.pyplot as plt
width = 100
height = 100
heightmap = np.zeros((height, width))
def generate_perlin_noise(width, height, scale=100, octaves=6, persistence=0.5, lacunarity=2.0):
  def fbm(x, y):
    total = 0.0
    frequency = 1.0
    amplitude = 1.0
    for _ in range(octaves):
      total += amplitude * np.sin(x * frequency) * np.cos(y * frequency)
      frequency *= lacunarity
      amplitude *= persistence
    return total

  x = np.linspace(0, width, width) / scale
  y = np.linspace(0, height, height) / scale
  xv, yv = np.meshgrid(x, y)
  return fbm(xv, yv)
heightmap += generate_perlin_noise(width, height, scale=100, octaves=6, persistence=0.5, lacunarity=2.0) * 50
def generate_peaks(heightmap, num_peaks=5):
  for _ in range(num_peaks):
    peak_x = np.random.randint(0, width)
    peak_y = np.random.randint(0, height)
    peak_radius = np.random.randint(5, 20)
    heightmap[peak_y - peak_radius:peak_y + peak_radius, peak_x - peak_radius:peak_x + peak_radius] += np.random.randint(50, 150)
    heightmap[peak_y, peak_x] += np.random.randint(100, 200)  # Дополнительная высота в центре
def generate_hills(heightmap, num_hills=10):
  for _ in range(num_hills):
    hill_x = np.random.randint(0, width)
    hill_y = np.random.randint(0, height)
    hill_radius = np.random.randint(20, 50)
    heightmap[hill_y - hill_radius:hill_y + hill_radius, hill_x - hill_radius:hill_x + hill_radius] += np.random.randint(20, 50)
generate_peaks(heightmap, num_peaks=5)
generate_hills(heightmap, num_hills=10)
print(heightmap)
plt.imshow(heightmap, cmap='terrain', interpolation='nearest')
plt.colorbar()
plt.title("Карта высот")
plt.show()