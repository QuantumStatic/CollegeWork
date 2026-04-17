import cv2

FEATURES = 5000
MIN_MATCH = 15
MIN_MATCH_SIFT = 10
DIST_RATIO = 0.75
DIST_SIFT = 0.6
ALL_MULTITHREAD = False
FLANN_INDEX_LSH = 6
FILTERING = False
SIMILARITY_THRESHOLD = 0.6

orb = cv2.ORB_create(nfeatures=FEATURES)
sift = cv2.SIFT_create(nfeatures=FEATURES)

bf = cv2.BFMatcher(cv2.NORM_L2)

index_params = dict(algorithm=FLANN_INDEX_LSH,
                    table_number=6,  # 6, 12
                    key_size=12,  # 12, 20
                    multi_probe_level=1)  # 2

search_params = {"checks": 100}
fm = cv2.FlannBasedMatcher(index_params, search_params)
DIST_ORB = DIST_RATIO
MIN_MATCH_ORB = MIN_MATCH
