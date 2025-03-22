import logging
import re

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# def extract_scores(answer: str) -> int:
#     """
#     Extracts the score from the answer.

#     Args:
#         answer: The answer to extract the score from.

#     Returns:
#         The extracted score.
#     """
#     try:
#         # 正则表达式匹配分数
#         pattern = r"[Ss]core:\s*(\d{1,2})"
#         matches = re.findall(pattern, answer)
        
#         if matches:
#             score = int(matches[0])
#             if 0 <= score <= 20:
#                 return score
#             else:
#                 return -1
#         return -1
    
#     except Exception as e:
#         logger.error(f"Error in extract_scores: {e}")
#         return -1


def extract_scores(answer: str) -> int:
    """
    Extracts the score from the answer.

    Args:
        answer: The answer to extract the score from.

    Returns:
        The extracted score.
    """
    try:
        pattern = r"[Ss]core:\s*(\d{1,2})"
        matches = re.findall(pattern, answer)
        score = int(matches[0]) if matches else -1
        return score if 0 <= score <= 20 else -1
    except Exception as e:
        logger.error(f"Error in extract_scores: {e}")
        return -1
    
print(extract_scores("Score: 15"))       # 15
print(extract_scores("score: 20"))       #  20
print(extract_scores("Score: 25"))       #  -1
print(extract_scores("Score:   8"))      #  8
print(extract_scores("My score: 5"))     #  -1
