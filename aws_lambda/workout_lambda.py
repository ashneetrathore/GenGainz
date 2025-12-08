import json
import urllib.request
import boto3
import botocore

def lambda_handler(event, context):
    if event['requestContext']['http']['method'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,Access-Control-Allow-Origin',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Expose-Headers': '*',
                'Access-Control-Max-Age': '300',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'CORS preflight check successful'})
        }
        
    try:
        if event['requestContext']['http']['method'] != 'POST':
            return {
                'statusCode': 405,
                'headers': {
                'Access-Control-Allow-Origin': '*',  
                'Content-Type': 'application/json'
                },
                'body': json.dumps({'error': 'Method Not Allowed'})
            }
        # Parse the incoming data
        user_data = input_handler(event)

        # Fetch exercises based on user input
        exercises = fetch_exercises(user_data['bodyAreas'], user_data['muscleGroups'])

        # Generate Bedrock prompt
        prompt = build_bedrock_prompt(user_data, exercises)

        # Return Bedrock response
        workout_plan = json.loads(get_bedrock_response(prompt))

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',  
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,Access-Control-Allow-Origin',  
                'Access-Control-Allow-Credentials': 'true',  
                'Access-Control-Expose-Headers': '*',  
                'Access-Control-Max-Age': '300',  
                'Content-Type': 'application/json'
            },
            'body': json.dumps(workout_plan)
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',  
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET',  
                'Access-Control-Allow-Headers': 'Content-Type,Authorization,Access-Control-Allow-Origin',  
                'Access-Control-Allow-Credentials': 'true',  
                'Access-Control-Expose-Headers': '*',  
                'Access-Control-Max-Age': '300',  
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'error': str(e)})
        }

# Retrieve and validate input, then return parsed data to main handler
def input_handler(event):
    try:
        # Parse the JSON body
        user_data = json.loads(event.get('body', '{}'))

        # Required fields for basic validation
        required_fields = ['age', 'weight', 'heightFeet', 'heightInches', 'sex', 'workoutTime', 
                           'fitnessLevel', 'bodyAreas', 'muscleGroups']

        # Check for missing fields in one line
        missing_fields = [field for field in required_fields if field not in user_data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Minimal type checking (age, weight, feet, inches, workout time)
        try:
            user_data['age'] = int(user_data['age'])
            user_data['weight'] = int(user_data['weight'])
            user_data['heightFeet'] = int(user_data['heightFeet'])
            user_data['heightInches'] = int(user_data['heightInches'])
            user_data['workoutTime'] = int(user_data['workoutTime'])
        except ValueError:
            raise ValueError("Age, weight, feet, inches, and workout time must be integers")

        # Return the validated data
        return user_data

    except Exception as e:
        raise ValueError(f"Input handling error: {str(e)}")

def fetch_exercises(body_parts, muscle_groups):
    headers = {
        "X-RapidAPI-Key": "885ac77305mshaea5e15f75d7864p1c438ejsn2bc14516b97c",
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }

    all_exercises = []
    
    # Add exercises based on the body part to an overall collection
    for part in body_parts:
        endpoint = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{part}"
        req = urllib.request.Request(endpoint, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            exercises = json.loads(data)
            
            # Filter exercises based on muscle groups
            for exer in exercises:
                if exer['target'].lower() in muscle_groups:
                    all_exercises.append(exer['name'])

    return all_exercises

def build_bedrock_prompt(user_data, all_exercises):
    demographics = (
        f"Age: {user_data['age']} years,\n"
        f"Gender: {user_data['sex']},\n"
        f"Height: {(user_data['heightFeet'] * 12) + user_data['heightInches']} inches,\n"
        f"Weight: {user_data['weight']} pounds \n"
    )

    body_part_list = ", ".join(user_data['bodyAreas'])
    muscle_group_list = ", ".join(user_data['muscleGroups'])
    exercise_list = ", ".join(all_exercises)

    prompt = (
        f"Create a daily {user_data['workout_time']} minute {user_data['workout_level']} workout plan "
        f"featuring 10 exercises with the following user criteria:\n"
        + demographics +
        f"Preferred body parts that the user would like to focus on " +
        body_part_list +
        f"\nPreferred muscle groups that the user would like to focus on " +
        muscle_group_list +
        f"\nSuggested exercises based on an expert source:\n" +
        exercise_list +
        "\nProvide specific reps, or duration if applicable, sets, intensity, rest periods, and instructions " +
        "for each exercise based on the user demographics and preferences"
    )

    return prompt

# Initialize Bedrock client
def init_bedrock_client():
    try:
        # Create a session using Boto3
        session = boto3.session.Session()
        # Set your AWS region (customize as needed)
        region = "us-west-2"
        # Create a Bedrock client using the session
        bedrock = session.client(service_name='bedrock-runtime', region_name=region)
        return bedrock
    except Exception as e:
        print(f"Error initializing Bedrock client: {str(e)}")
        return None


# Call Bedrock model and get response
def get_bedrock_response(prompt):
    try:
        # Initialize the Bedrock client
        bedrock = init_bedrock_client()
        if not bedrock:
            raise RuntimeError("Failed to initialize Bedrock client")

        model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "temperature": 0.7,
            "top_p": 0.9,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ],
        })

        response = bedrock.invoke_model(
            modelId=model_id,
            body=body,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response['body'].read())
        workout_plan = response_body["content"][0]["text"]
        return workout_plan

    except Exception as e:
        return f"Error generating workout plan: {str(e)}"