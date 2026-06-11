# App.tsx – Main Application Controller

## Purpose

App.tsx is the central controller for the Cyber Risk & Awareness Hub. It manages application navigation, user progress, scenario loading, answer submission, completion tracking and administrative functions.

It acts as the primary connection point between the React frontend and the FastAPI backend.

## How It Works

When the application starts, App.tsx:

• Loads the current Staff ID from local storage.
• Determines which screen should be displayed.
• Loads available training domains.
• Retrieves completion statistics.
• Displays the correct application view.

The component controls every major screen within the application.

## Application Views

The application uses a view-based navigation system.

### Start View

Allows the user to enter a Staff ID before beginning training.

Functions:

• Stores Staff ID.
• Saves Staff ID to local storage.
• Loads user progress.

### Home View

The main dashboard.

Displays:

• Training progress.
• Domains passed.
• Overall score.
• Completion status.

Allows users to select training topics.

### Domain View

Displays scenarios belonging to a selected training domain.

Examples include:

• Passwords & Authentication.
• Phishing & Social Engineering.
• Malware & Ransomware.

Users can select a scenario to begin training.

### Scenario View

Displays the selected cyber security scenario.

Functions:

• Loads scenario data.
• Displays question text.
• Displays answer options.
• Accepts user selections.
• Submits answers to the backend.
• Displays explanations and results.

### Summary View

Displays overall training performance.

Includes:

• Scenarios attempted.
• Correct answers.
• Overall score.
• Training completion status.
• Domain-by-domain results.

### Admin View

Administrative control screen.

Functions:

• Reset user progress.
• Enter administrator PIN.
• Specify target Staff ID.
• Display reset status messages.

## State Management

The component uses React state to manage application data.

### User State

Tracks:

• Current Staff ID.
• Active user session.

### Domain State

Tracks:

• Available domains.
• Loading status.
• Error messages.

### Scenario State

Tracks:

• Available scenarios.
• Current scenario.
• Loading status.
• Error messages.

### Completion State

Tracks:

• Progress statistics.
• Domain completion.
• Overall completion.

### Admin State

Tracks:

• Admin PIN.
• Target Staff ID.
• Reset operations.

## Backend Communication

App.tsx communicates with the backend through api.ts.

Functions used include:

• apiGetDomains()
• apiGetScenariosByDomain()
• apiGetScenario()
• apiSubmitAnswer()
• apiGetCompletion()
• apiAdminResetProgress()

These functions allow the application to retrieve and update training data.

## Progress Tracking

The component retrieves completion data from the backend and calculates:

• Total scenarios attempted.
• Total scenarios available.
• Domains passed.
• Overall score percentage.
• Training completion status.

Progress is linked to individual Staff IDs.

## User Experience Features

The component includes:

• Loading indicators.
• Error handling.
• Progress summaries.
• Scenario explanations.
• Locked scenario protection.
• Automatic progress refresh.
• Persistent Staff ID storage.

## Why This File Is Important

App.tsx is the core controller of the Cyber Risk & Awareness Hub. It coordinates navigation, manages user progress, communicates with the backend API and controls every major training screen within the application. Without this file, the frontend application would have no central management system.
