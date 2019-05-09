OK = "?result=OK&answer={}&did_answer=Answer"
CE = "?result=CE&answer=&did_answer=Answer"
UD = "?result=UD&answer=&did_answer=Answer"
US = "?result=US&answer=&did_answer=Answer"
HINT = "?show_hint=1"

url = "http://cppquiz.org/quiz/question/{}"

token = "864062625:AAHt_xciZildH4u6VkGM8veN_GPzxBh6fjc"


# Numbers of questions aren't available in the site that I'm parsing
numbers_1 = [10, 19, 20, 21, 22, 23, 34, 36, 39, 40, 43, 45, 46, 47, 50, 51, 108, 110, 117, 146, 149, 150, 154, 155,
             156, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 175, 176, 179, 180, 181, 182, 183, 194, 197, 199,
             200, 201, 202, 203, 204, 207, 209, 210, 211, 212, 213, 214, 215, 216, 218, 220, 221, 223, 232, 234, 235,
             251, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 139, 142, 141, 143, 138, 137, 136, 134, 123,
             128]
numbers_2 = [i for i in range(53, 105)]
numbers = numbers_2 + numbers_1
