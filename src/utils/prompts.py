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