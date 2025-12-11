## :muscle: GENGAINZ

### :open_book: OVERVIEW
Date: May 2025\
Developer(s): Ashneet Rathore, Josephine Ligatsyah, Allison Yeh

GenGainz is a full-stack AI-powered web application that creates personalized workout routines based on user demographics and fitness preferences. The app leverages AWS services and was developed in a four-day span as a submission for the AWS CloudHacks hackathon hosted at UCI.

### :classical_building: ARCHITECTURE
> [!IMPORTANT]
> The AWS services are no longer active, so the app cannot run live. For reference, the AWS Lambda function used in the backend has been included in the repo.

The backend logic is implemented in **Python** and runs entirely within **AWS Lambda**. When the user submits the form to generate a workout plan, the browser sends a request that triggers the Lambda function. In turn, Lambda responds to confirm that the request is allowed. Once the form data is received, Lambda calls the **ExerciseDB API** from RapidAPI to fetch relevant exercises and constructs a prompt based on both the user's input and the retrieved exercises. The prompt is then sent to **Amazon Bedrock**, where the **Claude Sonnet LLM** generates a personalized workout routine. Finally, the workout plan is returned from the Lambda function to the frontend for display.

The frontend is built with **React + Next.js**, **JavaScript**, and **CSS** for a structured, component-based interface. Users input demographic information (height, weight, sex, age), along with their fitness preferences such as workout duration and targeted body groups. **AWS Amplify** was used for deployment and integration with AWS backend services. During Amplify setup, GitHub was selected as the app's source and environment variables were configured directly in the Amplify console to securely manage API keys and backend URLs.

### :open_file_folder: PROJECT FILE STRUCTURE
```bash
GenGainz/
├── aws_lambda/         
│   └── workout_lambda.py          # Contains original AWS Lambda function (for reference purposes)
├── src/        
│   └── app/
│       ├── styles/                # Contains CSS files for frontend        
│       ├── workout/               
│       │   └── page.js            # Renders the returned workout plan to the user
│       ├── layout.js              # Defines the layout structure for pages
│       └── page.js                # Renders the main app page and collects user input 
├── public/                        # Stores static logos and icons
├── package.json                   # Contains external dependencies
├── package-lock.json              # Contains external dependencies
├── jsconfig.json                  # Contains configuration settings
├── next.config.mjs                # Contains configuration settings
├── postcss.config.mjs             # Contains configuration settings
├── README.md                      # Project documentation
└── .gitignore                     # Excludes files and folders from version control
```

### :film_strip: DEMO
[Watch the demo on Youtube](https://youtu.be/xo7eef4Pw6g)