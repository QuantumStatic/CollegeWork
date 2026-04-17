import cv2
from image_reader import get_query_image, get_gallery_image, gallery_images_names, query_images_names
import concurrent.futures
import numpy
from DataStorage import stored_data
from CONSTANTS import MIN_MATCH, ALL_MULTITHREAD, FILTERING, bf as matcher, orb  # , FEATURES, DIST_RATIO, orb
from file_writer import write_ordered_dict, show_top_20

multithread_matches: list[tuple[str, str]] = []
img_match_count: dict[str, list[tuple]] = {}
iterations_done = 0
optimised_img_parameters = {"27.jpg": (6000, 0.66, 1), "35.jpg": (6000, 0.66, 10), "316.jpg": (4500, 0.665, 5),
                            "776.jpg": (6000, 0.66, 9), "1258.jpg": (6000, 0.66, 5), "1656.jpg": (6000, 0.66, 7),
                            "1709.jpg": (6000, 0.66, 10), "2032.jpg": (6000, 0.66, 5), "2040.jpg": (6000, 0.67, 7),
                            "2176.jpg": (6000, 0.66, 2), "2461.jpg": (10000, 0.68, 9), "2714.jpg": (10000, 0.67, 8),
                            "3502.jpg": (10000, 0.67, 10), "3557.jpg": (6000, 0.69, 9), "3833.jpg": (10000, 0.67, 3),
                            "3906.jpg": (10000, 0.67, 1), "4354.jpg": (10000, 0.675, 1), "4445.jpg": (6000, 0.67, 9),
                            "4716.jpg": (6000, 0.67, 10), "4929.jpg": (10000, 0.6, 5)}

FEATURES, DIST_RATIO = 0, 0


def view_multithread_matches():
    global multithread_matches

    for match in multithread_matches:
        gallery_img = get_gallery_image(match[0])
        query_img = get_query_image(match[1])

        kp_gallery, des_gallery = orb.detectAndCompute(gallery_img, None)
        kp_query, des_query = orb.detectAndCompute(query_img, None)

        matches = matcher.knnMatch(des_gallery, des_query, k=2)

        good = []
        try:
            for m, n in matches:
                if m.distance < DIST_RATIO * n.distance:
                    good.append([m])
        except ValueError:
            pass

        img3 = cv2.drawMatchesKnn(gallery_img, kp_gallery, get_query_image(
            match[1]), kp_query, good, None, flags=2)
        cv2.imshow("features", img3)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def show_top_list(query_img_name: str):
    global img_match_count
    print(f"Showing top list for {query_img_name}")
    img_match_count[query_img_name].sort(key=lambda x: x[1], reverse=True)
    for i in range(min(10, len(img_match_count[query_img_name]))):
        print(img_match_count[query_img_name][i])
        cv2.imshow(f"{query_img_name} {FEATURES} {DIST_RATIO}",
                   get_gallery_image(img_match_count[query_img_name][i][0]))
        cv2.waitKey(0)
    cv2.destroyAllWindows()
    print()


def check_per_query_existence_and_display(per_query_run):
    def inner_wrapper(query_img_name):
        global multithread_matches, img_match_count

        global FEATURES, DIST_RATIO
        FEATURES, DIST_RATIO, *_ = optimised_img_parameters[query_img_name]

        if FILTERING and (DIST_RATIO, MIN_MATCH, FEATURES, query_img_name) in stored_data['filter_results']:
            multithread_matches = stored_data[f"{DIST_RATIO}{MIN_MATCH}{FEATURES}{query_img_name}"]
            print(f"This has been calculated already. {len(multithread_matches)} matches were found.")
            print("Results recovered from storage")
            view_multithread_matches()
            return
        elif not FILTERING and (DIST_RATIO, FEATURES, query_img_name) in stored_data["top_results"]:
            img_match_count[query_img_name] = stored_data[f"{DIST_RATIO}{FEATURES}{query_img_name}"]
            print("This has been calculated already")
            print("Results recovered from storage")
            # show_top_list(query_img_name)
            return

        img_match_count[query_img_name] = []
        per_query_run(query_img_name)

        if FILTERING:
            print("running view")
            print(f"A total of {len(multithread_matches)} matches were found.")
            stored_data[f"{DIST_RATIO}{MIN_MATCH}{FEATURES}{query_img_name}"] = multithread_matches
            stored_data["filter_results"].add((DIST_RATIO, MIN_MATCH, FEATURES, query_img_name))
            stored_data.save()
            view_multithread_matches()
        else:
            print("showing view")
            stored_data[f"{DIST_RATIO}{FEATURES}{query_img_name}"] = img_match_count[query_img_name]
            stored_data["top_results"].add((DIST_RATIO, FEATURES, query_img_name))
            stored_data.save()
            show_top_list(query_img_name)

    return inner_wrapper


def all_multi_thread_completion() -> float:
    return iterations_done / 100_000


def per_query_multi_thread_completion() -> float:
    return iterations_done / 5_000


iteration_completion = all_multi_thread_completion if ALL_MULTITHREAD is True else per_query_multi_thread_completion


def matching_package(gallery_img_name: str, query_img_name: str):
    global iterations_done
    global FEATURES, DIST_RATIO

    des_gallery = numpy.load(f"gallery_store/orb_store/{FEATURES}_store/des_gallery{gallery_img_name}.npy",
                             allow_pickle=True)
    des_query = numpy.load(f"query_store/orb_Store/{FEATURES}_store/des_query{query_img_name}.npy", allow_pickle=True)

    try:
        matches = matcher.knnMatch(des_gallery, des_query, k=2)
    except cv2.error:
        print(f"{gallery_img_name} and {query_img_name} gave a knn error")
        kp_gallery, des_gallery = orb.detectAndCompute(get_gallery_image(gallery_img_name), None)
        kp_query, des_query = orb.detectAndCompute(get_query_image(query_img_name), None)
        matches = matcher.knnMatch(des_gallery, des_query, k=2)

    match_count = 0

    for m, n in matches:
        if m.distance < DIST_RATIO * n.distance:
            match_count += 1
            if FILTERING and match_count >= MIN_MATCH:
                multithread_matches.append((gallery_img_name, query_img_name))
                break

    if not FILTERING:
        img_match_count[query_img_name].append((gallery_img_name, match_count))

    if iterations_done % 250 == 0:
        print(f"{int(round(iteration_completion() * 100, 0))}%")
    iterations_done += 1


def inbuilt_retrieval_all():
    global iterations_done
    for query_img_name in query_images_names():
        iterations_done = 0
        inbuilt_retrieval_per_query(query_img_name)


@check_per_query_existence_and_display
def inbuilt_retrieval_per_query(query_img_name: str):
    for gallery_img_names in gallery_images_names():
        matching_package(gallery_img_names, query_img_name)


@check_per_query_existence_and_display
def inbuilt_retrieval_per_query_multithread(query_img_name: str):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for gallery_img_name in gallery_images_names():
            executor.submit(matching_package, gallery_img_name, query_img_name)


def inbuilt_retrieval_all_multithread():
    global iterations_done
    for query_img_name in query_images_names():
        iterations_done = 0
        inbuilt_retrieval_per_query(query_img_name)
    # write_ordered_dict(file_name="method2", ordered_dict=img_match_count)
    # show_top_20(ordered_dict=img_match_count)
