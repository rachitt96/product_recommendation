from submission import Submission
from product_recommendation import Recommendations
import sys

if(__name__ == "__main__"):
    """ 
        The main function to request the co-occurance based recommendation.
    """

    recommendation_obj = Recommendations()
    request_recommedation_product_ids_lst = ['20592676_EA', '20801754003_C15']
    recommendation_product_dict = {}

    for product_id in request_recommedation_product_ids_lst:
        recommendation_product_dict[product_id] = recommendation_obj.get_top_recommendations(product_id, get_latency=False)

    print(recommendation_product_dict)

    submission_obj = Submission()
    submission_obj.submit_result_to_api(recommendation_product_dict)

    #recommendation_obj.get_product_names_by_ids(['20592676_EA', '20801754003_C15'])