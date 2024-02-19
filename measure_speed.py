#import libraries
from exif import Image
from datetime import datetime
import cv2
import math

def measure_speed(pic1, pic2): #function measure speed
    """Function to measure speed of the ISS using to pictures

    Args:
        pic1 (str): path to image1
        pic2 (str): path to image2

    Returns:
        speed (number): speed of ISS
    """
    
    def get_time(image): 
        """Function to get time from EXIF data of image

        Args:
            image (str): path to image

        Returns:
            datetime: datetime of when the image was taken
        """
        try:
            with open(image, 'rb') as image_file:
                img = Image(image_file)
                time_str = img.get("datetime_original")
                time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
            return time
        except Exception:
            return int(image[5:image.find(".jpg")])*16 # if unable to load from EXIF data use image ID times targeted loop time
        
        
    def get_time_difference(image_1, image_2):
        """Function to calculate delta T between two images

        Args:
            image_1 (str): path to first image
            image_2 (str): path to second image

        Returns:
            int: Difference in seconds
        """
        time_1 = get_time(image_1)
        time_2 = get_time(image_2)
        time_difference = time_2 - time_1
        return time_difference.seconds


    def convert_to_cv(image_1, image_2):
        """Function to open images into cv2 format

        Args:
            image_1 (str): path to first image
            image_2 (str): path to second image

        Returns:
            cv2.Image: both images opened using cv2.imread
        """
        image_1_cv = cv2.imread(image_1, 0)
        image_2_cv = cv2.imread(image_2, 0)
        return image_1_cv, image_2_cv


    def calculate_features(image_1_cv, image_2_cv, feature_number):
        """Function to find the keypoints and descriptors for the two images

        Args:
            image_1_cv (cv.image): first image loaded into openCV
            image_2_cv (cv.image): second image loaded into openCV
            feature_number (int): maximum number of features you want to search for

        Returns:
            keypoints and the descriptors of the keypoints
        """
        orb = cv2.ORB_create(nfeatures = feature_number)
        keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
        keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
        return keypoints_1, keypoints_2, descriptors_1, descriptors_2


    def calculate_matches(descriptors_1, descriptors_2):
        """ tries to find matches in the two sets of keypoints

        Args:
            descriptors_1 (any): descriptors on the first image
            descriptors_2 (any): descriptors on the second image

        Returns:
            any: matches
        """
        brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = brute_force.match(descriptors_1, descriptors_2)
        matches = sorted(matches, key=lambda x: x.distance)
        return matches
        
    """
    def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
        matches are displayed on images

        Args:
            image_1_cv (cv.image): first image loaded into openCV
            keypoints_1 (any): keypoints for the first image
            image_2_cv (cv.image): second image loaded into openCV
            keypoints_2 (any): keypoints for the second image
            matches (array): array of matching keypoints
        
        match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
        resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
        cv2.imshow('matches', resize)
        cv2.waitKey(0)
        cv2.destroyWindow('matches')
    """
        
        
    def find_matching_coordinates(keypoints_1, keypoints_2, matches):
        """Function to "link" coordinates of points in one image to the other image (index in array for 1 will be same in array for 2)

        Args:
            keypoints_1 (array): keypoints for the first image
            keypoints_2 (array): keypoint for the second image
            matches (array): matching keypoints

        Returns:
            array,array: keypoints in the first and keypoints in the second image sorted to be matching
        """
        coordinates_1 = []
        coordinates_2 = []
        for match in matches:
            image_1_idx = match.queryIdx
            image_2_idx = match.trainIdx
            (x1,y1) = keypoints_1[image_1_idx].pt
            (x2,y2) = keypoints_2[image_2_idx].pt
            coordinates_1.append((x1,y1))
            coordinates_2.append((x2,y2))
        return coordinates_1, coordinates_2


    def calculate_mean_distance(coordinates_1, coordinates_2):
        """Function to calculate distances between matching keypoints

        Args:
            coordinates_1 (array): keypoints in the first image (coords)
            coordinates_2 (array): keypoint in the second image (coors)

        Returns:
            number: mean distance between same point in first and in the second image
        """
        all_distances = 0
        merged_coordinates = list(zip(coordinates_1, coordinates_2))
        for coordinate in merged_coordinates:
            x_difference = coordinate[0][0] - coordinate[1][0]
            y_difference = coordinate[0][1] - coordinate[1][1]
            distance = math.hypot(x_difference, y_difference)
            all_distances = all_distances + distance
        return all_distances / len(merged_coordinates)


    def calculate_speed_in_kmps(feature_distance, GSD, time_difference):
        """ Function to calculate speed in kilometers per second base on the average distance of keypoints and time difference

        Args:
            feature_distance (number): calculated using `calculate_mean_distace` 
            GSD (number): 
            time_difference (number): in seconds; how long betweeen the photos

        Returns:
            number: ISS's speed in kmps
        """
        distance = feature_distance * GSD / 100000
        speed = distance / time_difference
        return speed

    def calc_GSD(): 
        return 12648

    time_difference = get_time_difference(pic1, pic2) #calculate time difference between two photos
    image_1_cv, image_2_cv = convert_to_cv(pic1, pic2) #create opencfv images objects
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) #get keypoints and descriptors
    if not (keypoints_1, keypoints_2, descriptors_1, descriptors_2):
        return None
    matches = calculate_matches(descriptors_1, descriptors_2) #match descriptors
    #display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches) #display matches
    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
    speed = calculate_speed_in_kmps(average_feature_distance, calc_GSD(), time_difference)
    
    return speed

#speed = measure_speed("image686.jpg", "image687.jpg")
#print(speed)
