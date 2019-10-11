from skimage import io, measure
import numpy as np

img = io.imread('object.jpg')

red_img = img[:, :, 0]
green_img = img[:, :, 1]
blue_img = img[:, :, 2]

redBinary = np.logical_and(red_img > 120, green_img < 105)
greenBinary = np.logical_and(np.logical_and(green_img > 105, red_img < 90), blue_img < 100)
blueBinary = blue_img > 145
yellowBinary = np.logical_and(red_img > 120, green_img > 110)

redTagged = measure.label(redBinary, neighbors=8)
center_red = redTagged == 1
right_red = redTagged == 2

greenTagged = measure.label(greenBinary, neighbors=8)
left_green = greenTagged == 1
center_green = greenTagged == 2

blueTagged = measure.label(blueBinary, neighbors=8)
center_blue = blueTagged == 1
right_blue = blueTagged == 2

yellowTagged = measure.label(yellowBinary, neighbors=8)
yellow_ball = yellowTagged == 1
yellow_block = yellowTagged == 2

def calculate_centroid(image):
	row_total = 0
	column_total = 0
	total_labeled = 0
	for i in range(np.shape(image)[0]):
		for j in range(np.shape(image)[1]):
			if image[i][j] == 1:
				row_total += i
				column_total += j
				total_labeled += 1
	return (row_total/total_labeled, column_total/total_labeled)

def calculate_boundary(image):
	rows = [0, np.shape(image)[0]] #max, min rows
	cols = [0, np.shape(image)[1]] #max, min cols
	for i in range(np.shape(image)[0]):
		for j in range(np.shape(image)[1]):
			if image[i][j] == 1:
				if i > rows[0]:
					rows[0] = i
				if i < rows[1]:
					rows[1] = i
				if j > cols[0]:
					cols[0] = j
				if j < cols[1]:
					cols[1] = j
	return rows, cols

red_centroid1 = calculate_centroid(center_red)
red_centroid2 = calculate_centroid(right_red)
green_centroid1 = calculate_centroid(left_green)
green_centroid2 = calculate_centroid(center_green)
blue_centroid1 = calculate_centroid(center_blue)
blue_centroid2 = calculate_centroid(right_blue)
yellow_centroid1 = calculate_centroid(yellow_ball)
yellow_centroid2 = calculate_centroid(yellow_block)
#print(red_centroid1, red_centroid2)
#print(green_centroid1, green_centroid2)
#print(blue_centroid1, blue_centroid2)
#print(yellow_centroid1, yellow_centroid2)
red_rows1, red_cols1 = calculate_boundary(center_red)
red_rows2, red_cols2 = calculate_boundary(right_red)
green_rows1, green_cols1 = calculate_boundary(left_green)
green_rows2, green_cols2 = calculate_boundary(center_green)
blue_rows1, blue_cols1 = calculate_boundary(center_blue)
blue_rows2, blue_cols2 = calculate_boundary(right_blue)
yellow_rows1, yellow_cols1 = calculate_boundary(yellow_ball)
yellow_rows2, yellow_cols2 = calculate_boundary(yellow_block)
print(red_rows1, red_cols1, red_rows2, red_cols2)
print(green_rows1, green_cols1, green_rows2, green_cols2)
print(blue_rows1, blue_cols1, blue_rows2, blue_cols2)
print(yellow_rows1, yellow_cols1, yellow_rows2, yellow_cols2)
#test_img = right_red
#io.imshow(test_img)
#io.show()

