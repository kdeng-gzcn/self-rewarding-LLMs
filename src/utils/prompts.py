prompt_step_01 = """
Generate realistic medical inquiries that a patient might ask a doctor.
Each inquiry should reflect how a real patient would describe their symptoms or concerns to a healthcare professional.
Ensure that the questions cover a variety of medical topics, including symptoms, diagnoses, treatments, medications, and lifestyle advice.

Format each inquiry inside <task></task> tags.

Make sure the questions vary in complexity, some being general inquiries while others include detailed symptoms or concerns.
Do not add any explanations or extra text beyond the <task></task> format.
"""

#prompt_step_01 = """

#Come up with a series of tasks and questions. Only the task/question,
#no further text/explanation, no additional information.
#The task or question should be something a person would ask a chatbot.

#Here are some examples: (Note that you should generate tasks/questions inside <task></task> tags)

#"""


judge_prompt = """Review the user’s question and the corresponding response using the additive 5-point
scoring system described below. 

The user's question is between <question> and </question>
The response of the AI Assistant is between <response> and </response>

Each response is scored across four dimensions, each with a maximum of 5 points, making the total possible score 20 points.

Points are accumulated based on the satisfaction of each criteria:

1. Structure of Response (0-5 points)
Objective: Ensure the response follows a clear logical structure and presents the diagnosis in order: Symptom Recognition → Cause Analysis → Recommendation Measures → Emergency Suggestions (if any).
   - 5 points: The response clearly includes five parts (Symptom Recognition, Cause Analysis, Recommendation Measures, Emergency Suggestions) with a well-defined logical structure and organized information. Each part is presented in a consistent and clear manner, with a final summary and concluding advice.
   - 4 points: The response generally includes all parts, but the logical structure is not clear. The distinction between the four parts is not obvious, or the information is mixed.
   - 3 points: The response has a certain structure but lacks clarity in segmentation and logic. It may cover only two or three parts and lacks a proper summary.
   - 2 points: The response uses some logical linking words or attempts to structure the content but lacks clear themes or segmentation.
   - 1 points: The response lacks structure, and the information is scattered without organization.

2. Specificity of Recommendations (0-5 points)
Objective: Ensure that the recommendations provided are not only specific but also tailored to the user's background, including medication usage and related conditions.
   - 5 points: Provides highly personalized recommendations based on the user's specific background (such as medical history, current medication, symptoms). Offers comprehensive short-term and emergency measures while analyzing potential diseases and presenting various response options.
   - 4 points: Provides detailed recommendations and analysis based on symptoms, specifying how to proceed (including appropriate medical departments and medication precautions). However, lacks individual adjustments or detailed analysis of abnormal conditions.
   - 3 points: Provides basic recommendations but lacks thorough consideration of the user's background or symptoms. Typically offers only one response approach.
   - 2 points: Provides vague suggestions, only mentioning "go to the hospital" or "take medicine" without reasonable explanations or analysis of the symptoms.
   - 1 points: Provides no recommendations or simply repeats the patient's description.


3. Empathy & Human-Like Tone (0-5 points)
Objective: Ensure that the response demonstrates genuine empathy and concern, avoiding overly formal or robotic expressions.
   - 5 points: The response not only expresses empathy but also includes encouragement, comfort, or emotional support. For example:“I understand this must be very difficult for you. Remember, you're not alone, and we're here to support you.”
   - 4 points: Contains clear expressions of concern, but lacks additional comforting or supportive words.
   - 3 points: Shows a certain degree of empathy but feels insincere or emotionally flat.
   - 2 points: Provides brief and straightforward expressions of concern, but feels overly formal or stiff.
   - 1 points: Completely lacks empathetic expressions or human-like language.

4. Completeness (0-5 points)
Objective: Ensure the response not only covers all possible diseases but also provides clear response measures and prioritization.
   - 5 points: Provides multiple possible causes for the symptoms (at least three) and offers prioritized responses for each cause: 1.Clearly distinguishes which situations are emergencies and provides detailed responses. 2.Special attention to combining danger signals with the user's background.
   - 4 points: Provides two or more possible causes but fails to offer differentiated responses for different causes.May suggest responses to emergencies but lacks clarity or is incomplete.
   - 3 points: Provides only one or two possible causes and suggests corresponding recommendations, but lacks detail or explanation.
   - 2 points: Only provides a single vague cause and recommendation, with unclear suggestions.
   - 1 points: Provides no possible cause or response measures.

If the response contains any of the following situations, it will be directly scored as 0 points:
   - Repetitive Content: The content is a repetition of previous statements without adding any new information or meaning.
   - Irrelevant Content: The response contains irrelevant information or recommendations unrelated to the inquiry.
   - Redundant Information: Excessive redundant wording or meaningless explanations (e.g., the "Chat Doctor" repeating self-introduction).
   - Failure to Address Key Issues: The response fails to provide a targeted answer to the user's problem (e.g., if the user clearly requests emergency advice but the response only offers general advice or suggests waiting and observation).

<question>{prompt}</question>
<response>{response}</response>

After examining the user’s instruction and the response, judge the response in the following 4 dimensions:
Structure of Response: from 0-5 points  
Specificity of Recommendations: from 0-5 points  
Empathy & Human-Like Tone: from 0-5 points  
Completeness: from 0-5 points   

Then, directly sum the above subscores to be the total score.

- The total score should be formatted as
"score: <total points>", where <total points> is the sum of the above four dimensions subscores, ranging from 0 to 20.
- Briefly justify your total score, up to 100 words.
"""


judge_prompt_01 = """Review the user’s question and the corresponding response using the additive 5-point
scoring system described below. 

The user's question is between <question> and </question>
The response of the AI Assistant is between <response> and </response>

Each response is scored across four dimensions, each with a maximum of 5 points, making the total possible score 20 points.

Points are accumulated based on the satisfaction of each criteria:

1. Structure of Response (0-5 points)
   - 5 points: The response is clearly divided into paragraphs, each focusing on a specific topic, and includes a reasonable summary or conclusion.
   - 4 points: The response is divided into paragraphs, but the logical structure is unclear, and the content does not adequately focus on a single topic.
   - 3 points: The response demonstrates coherence and a reasonable logical order with minimal repetition, building on the use of logical connecting words.
   - 2 points: The response uses some logical connecting words.
   - 1 points: The response lacks structure.

2. Specificity of Recommendations (0-5 points)
   - 5 points: Builds upon level 4 by providing highly personalized recommendations, including specific self-care methods or short-term solutions for various potential conditions. It also offers tailored advice based on the user's background, such as age, gender, and known medical history, ensuring the recommendations are both relevant and practical.
   - 4 points: Provides a detailed response based on symptoms, including a discussion of various scenarios. Offers specific advice on what medication to take, which department to visit, and explains the reasoning behind these suggestions.
   - 3 points:  Offers basic advice based on symptoms, mentioning what medication to take or which department to visit, but lacks further explanation or elaboration.
   - 2 points:  Provides only vague recommendations, such as “take medicine” or “go to the hospital,” without elaboration.
   - 1 points: Provides no recommendations at all.


3. Empathy & Human-Like Tone (0-5 points)
   - 5 points: Builds upon level 4 by providing positive reassurance or support. For example “I understand this must be really difficult for you. Remember, you are not alone, and we are here to support you.”: 
   - 4 points: Includes comforting and empathetic statements, conveying understanding of the user's emotions. For example: “I understand this must be really difficult for you.”
   - 3 points: Provides a specific apology that acknowledges the user's situation, showing some degree of empathy. For example:“Sorry for hearing that.”
   - 2 points: Offers a simple apology or expression of concern without personalization. For example:“Sorry.”
   - 1 points: Completely lacks compassionate communication.

4. Completeness (0-5 points)
   - 5 points: In addition to providing multiple possible causes, clear next steps or detailed coping measures are offered.
   - 4 points: Provides more than two possible causes of the patient's symptoms while addressing all of the patient's questions, along with a detailed case-by-case analysis.
   - 3 points: Provides two possible causes of the patient's symptoms while addressing all of the patient's questions.
   - 2 points: Provides a single possible cause of the patient's symptoms while addressing all of the patient's questions.
   - 1 points: Only partially answers the patient's questions.

- If the response contains repetitive statements, irrelevant content, or redundant numbers, score the response 0.

<question>{prompt}</question>
<response>{response}</response>

After examining the user’s instruction and the response, judge the response in the following 4 dimensions:
Structure of Response: from 0-5 points  
Specificity of Recommendations: from 0-5 points  
Empathy & Human-Like Tone: from 0-5 points  
Completeness: from 0-5 points   

Then, directly sum the above subscores to be the total score.

- The total score should be formatted as
"score: <total points>", where <total points> is the sum of the above four dimensions subscores, ranging from 0 to 20.
- Briefly justify your total score, up to 100 words.
"""


judge_prompt_0 = """Review the user’s question and the corresponding response using the additive 5-point
scoring system described below. 

The user's question is between <question> and </question>
The response of the AI Assistant is between <response> and </response>

Each response is scored across four dimensions, each with a maximum of 5 points, making the total possible score 20 points.

Points are accumulated based on the satisfaction of each criteria:
1. Medical Relevance (0-5 points)
   - 5 points: The response directly addresses the user’s medical concern, staying fully on-topic.
   - 3-4 points: The response is mostly relevant but contains minor unrelated details.
   - 1-2 points: The response is only partially relevant or includes significant off-topic content.
   - 0 points: The response is completely irrelevant to the user's question.

2. Medical Expertise & Accuracy (0-5 points)
   - 5 points: The response demonstrates expert-level medical accuracy, free from misleading or outdated information.
   - 3-4 points: The response is mostly accurate but lacks depth or includes minor imprecisions.
   - 1-2 points: The response contains noticeable inaccuracies or lacks sufficient medical validity.
   - 0 points: The response provides incorrect or misleading medical information.

3. Empathy & Human-Like Tone (0-5 points)
   - 5 points: The response is supportive, calming, and reassuring, mimicking how a compassionate medical assistant would address a patient.
   - 3-4 points: The response is polite and neutral but lacks warmth or emotional sensitivity.
   - 1-2 points: The response is overly robotic, blunt, or lacks empathy in addressing patient concerns.
   - 0 points: The response is dismissive, condescending, or unnecessarily alarming.

4. Completeness (0-5 points)
   - 5 points: The response fully answers all parts of the user's question(s), providing a well-structured and informative explanation.
   - 3-4 points: The response covers most aspects of the question(s) but lacks some important details.
   - 1-2 points: The response is overly brief or missing key information, failing to answer some parts of the question(s).
   - 0 points: The response is vague and does not offer useful insight.

- If the response Dangerous or harmful medical advice (e.g., suggesting unsafe treatments, discouraging necessary medical attention, promoting unverified claims).
Severe misinformation (e.g., contradicting established medical guidelines or spreading false health claims), score the response 0.

<question>{prompt}</question>
<response>{response}</response>

After examining the user’s instruction and the response, judge the response in the following 4 dimensions:
Medical Relevance: from 0-5 points  
Medical Expertise: from 0-5 points  
Empathy & Human-Like Tone: from 0-5 points  
Completeness: from 0-5 points   

Then, directly sum the above subscores to be the total score.

- The total score should be formatted as
"score: <total points>", where <total points> is the sum of the above four dimensions subscores, ranging from 0 to 20.
- Briefly justify your total score, up to 100 words.
"""




judge_prompt_old = """Review the user’s question and the corresponding response using the additive 5-point
scoring system described below. 

The user's question is between <question> and </question>
The response of the AI Assistant is between <response> and </response>

Points are accumulated based on the satisfaction of each
criterion:
- Add 1 point if the response is relevant and provides some information related to
the user’s inquiry, even if it is incomplete or contains some irrelevant content.
- Add another point if the response addresses a substantial portion of the user’s question,
but does not completely resolve the query or provide a direct answer.
- Award a third point if the response answers the basic elements of the user’s question in a
useful way, regardless of whether it seems to have been written by an AI Assistant or if it
has elements typically found in blogs or search results.
- Grant a fourth point if the response is clearly written from an AI Assistant’s perspective,
addressing the user’s question directly and comprehensively, and is well-organized and
helpful, even if there is slight room for improvement in clarity, conciseness or focus.
- Bestow a fifth point for a response that is impeccably tailored to the user’s question
by an AI Assistant, without extraneous information, reflecting expert knowledge, and
demonstrating a high-quality, engaging, and insightful answer.
- If the response repeats itself or is not concise and to the point, score the response 0.

<question>{prompt}</question>
<response>{response}</response>

After examining the user’s instruction and the response:
- output the score of the evaluation using this exact format: "score: <total points>", where <total points> is between 0 and 5
- Briefly justify your total score, up to 100 words.
"""