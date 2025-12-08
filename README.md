## :muscle: GENGAINZ

### :open_book: OVERVIEW
Date: May 2025\
Developer(s): Ashneet Rathore, Josephine Ligatsyah, Allison Yeh




### :classical_building: ARCHITECTURE


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
└── .gitignore                     # Specifies files and folders that shouldn't be included in the repo
```