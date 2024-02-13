from exif import Image
from datetime import datetime
import cv2
import math

#import libraries
def measure_speed(pic1, pic2):
    
    def get_time(image):
        """Function to get time from EXIF data of image

        Args:
            image (str): path to image

        Returns:
            datetime: datetime of when the image was taken
        """
        with open(image, 'rb') as image_file:
            img = Image(image_file)
            time_str = img.get("datetime_original")
            time = datetime.strptime(time_str, '%Y:%m:%d %H:%M:%S')
        return time
        
        
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
        """_summary_

        Args:
            image_1_cv (_type_): _description_
            image_2_cv (_type_): _description_
            feature_number (_type_): _description_

        Returns:
            _type_: _description_
        """
        orb = cv2.ORB_create(nfeatures = feature_number)
        keypoints_1, descriptors_1 = orb.detectAndCompute(image_1_cv, None)
        keypoints_2, descriptors_2 = orb.detectAndCompute(image_2_cv, None)
        return keypoints_1, keypoints_2, descriptors_1, descriptors_2


    def calculate_matches(descriptors_1, descriptors_2):
        """_summary_

        Args:
            descriptors_1 (_type_): _description_
            descriptors_2 (_type_): _description_

        Returns:
            _type_: _description_
        """
        brute_force = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = brute_force.match(descriptors_1, descriptors_2)
        matches = sorted(matches, key=lambda x: x.distance)
        return matches
        

    def display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches):
        """_summary_

        Args:
            image_1_cv (_type_): _description_
            keypoints_1 (_type_): _description_
            image_2_cv (_type_): _description_
            keypoints_2 (_type_): _description_
            matches (_type_): _description_
        """
        match_img = cv2.drawMatches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches[:100], None)
        resize = cv2.resize(match_img, (1600,600), interpolation = cv2.INTER_AREA)
        cv2.imshow('matches', resize)
        cv2.waitKey(0)
        cv2.destroyWindow('matches')
        
        
    def find_matching_coordinates(keypoints_1, keypoints_2, matches):
        """_summary_

        Args:
            keypoints_1 (_type_): _description_
            keypoints_2 (_type_): _description_
            matches (_type_): _description_

        Returns:
            _type_: _description_
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
        """_summary_

        Args:
            coordinates_1 (_type_): _description_
            coordinates_2 (_type_): _description_

        Returns:
            _type_: _description_
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
        """_summary_

        Args:
            feature_distance (_type_): _description_
            GSD (_type_): _description_
            time_difference (_type_): _description_

        Returns:
            _type_: _description_
        """
        distance = feature_distance * GSD / 100000
        speed = distance / time_difference
        return speed


    time_difference = get_time_difference(pic1, pic2) #calculate time difference between two photos
    image_1_cv, image_2_cv = convert_to_cv(pic1, pic2) #create opencfv images objects
    keypoints_1, keypoints_2, descriptors_1, descriptors_2 = calculate_features(image_1_cv, image_2_cv, 1000) #get keypoints and descriptors
    matches = calculate_matches(descriptors_1, descriptors_2) #match descriptors
    display_matches(image_1_cv, keypoints_1, image_2_cv, keypoints_2, matches) #display matches
    coordinates_1, coordinates_2 = find_matching_coordinates(keypoints_1, keypoints_2, matches)
    average_feature_distance = calculate_mean_distance(coordinates_1, coordinates_2)
    speed = calculate_speed_in_kmps(average_feature_distance, 12648, time_difference)
    
    return speed

speed = measure_speed("image686.jpg", "image687.jpg")
print(speed)
