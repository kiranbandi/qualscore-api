Build the docker image

    docker compose build

Start the container in detached mode

    docker compose up -d 
  
Call  the API to see if its active 
  
    curl -X POST http://localhost:8082/generate-qualscore -H "Content-Type: application/json" -d "{\"comments\":[\"Overall very well done history on a teenager. Always remember the SHADES/HEADSSS history and in persons who have had sample, to do a sample history.\"]}"

Response should look as below 

    [[{"q1":3,"q2i":0,"q3i":0,"qual":5}]]
  

Qual - Overall QualScore
0: 'minimal',
1: 'very low',
2: 'low',
3: 'average',
4: 'above average',
5: 'excellent'

Q1 - Evidence - Does the rater provide sufficient evidence about resident performance? (0-no comment at all, 1-no, but comment present, 2-somewhat, 3-yes/full description)

0: "minimal",
1: "low",
2: "moderate",
3: "high"

Q2i - Suggestion - Does the rater provide a suggestion for improvement? (1-no/0-yes)
Q31 - Connection - Is the rater’s suggestion linked to the behavior described? (1-no/0-yes)