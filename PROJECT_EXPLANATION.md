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

# api.ts – API Communication Layer

## Purpose

api.ts provides the communication layer between the React frontend and the FastAPI backend.

Instead of placing fetch requests directly inside App.tsx, this file keeps all API calls in one central location. This makes the frontend easier to maintain because backend communication is separated from the user interface logic.

## How It Works

The file defines reusable functions that send requests to backend endpoints.

These functions are imported into App.tsx and used when the application needs to:

• Load training domains.
• Load scenarios for a selected domain.
• Load a specific scenario.
• Submit a user's answer.
• Retrieve completion progress.
• Reset user progress through the admin tool.

## API Base

The file uses:

• API_BASE

This is currently set to an empty string.

This allows the frontend to use relative API paths such as:

• /api/v1/domains
• /api/v1/submit
• /api/v1/completion/{staffId}

During local development, Vite forwards these API requests to the FastAPI backend using the proxy configuration in vite.config.ts.

## Type Definitions

The file defines TypeScript types for the main data structures used by the frontend.

These include:

• Domain
• ScenarioListItem
• ScenarioDetail
• SubmitAnswerResponse

Using TypeScript types helps make the application more predictable and reduces errors when working with API data.

## Domain Loading

apiGetDomains() requests the list of cyber security training domains from the backend.

This allows the Home dashboard to display the available topics that users can choose from.

## Scenario Loading

apiGetScenariosByDomain() loads all scenarios linked to a selected domain.

For example, when a user selects a phishing-related domain, the frontend requests only the scenarios that belong to that category.

apiGetScenario() loads the full details for one selected scenario.

This includes:

• Scenario title.
• Difficulty level.
• Question text.
• Answer options.
• Points available.

## Answer Submission

apiSubmitAnswer() sends the user's selected answer to the backend.

The frontend uses selected_option internally, but the backend expects option_id.

This file handles that conversion before sending the request.

The submitted data includes:

• Staff ID.
• Scenario ID.
• Selected option.

The backend then checks whether the answer is correct and returns the result.

## Submit Response Normalisation

normaliseSubmitResponse() is used to make backend responses more consistent for the frontend.

It ensures the frontend always receives:

• Whether the answer was correct.
• Points awarded.
• Explanation text.
• Whether the scenario had already been attempted.

This is useful because earlier versions of the frontend and backend used slightly different response field names. The normalisation function helps protect the interface from breaking if response shapes vary slightly.

## Completion Tracking

apiGetCompletion() retrieves progress information for a specific Staff ID.

This is used to show:

• Scenarios attempted.
• Correct answers.
• Domain progress.
• Overall score.
• Training completion status.

Because the Staff ID is included in the API route, progress can be tracked separately for each user.

## Admin Reset

apiAdminResetProgress() sends a request to reset a user's progress.

The request includes:

• Admin PIN.
• Target Staff ID.

The admin PIN is sent in the request header, while the Staff ID is sent in the request body.

This allows the backend to decide whether the reset request should be allowed and which user should be affected.

## Error Handling

The file includes basic error handling for failed API requests.

If a request fails, the functions throw an error message that can be displayed by App.tsx.

The readJsonSafe() helper attempts to read JSON safely from the backend response. If the response cannot be parsed, it returns null instead of crashing the application.

## Why This File Is Important

api.ts keeps backend communication separate from the main React interface.

This improves the project by:

• Keeping App.tsx cleaner.
• Avoiding repeated fetch logic.
• Making API calls easier to update.
• Supporting TypeScript type safety.
• Providing consistent response handling.
• Making the frontend/backend connection easier to understand.

This file acts as the bridge between the user interface and the FastAPI backend.



# main.py – FastAPI Application Entry Point

## Purpose

main.py is the backend entry point for the Cyber Risk & Awareness Hub.

Its role is to initialise the FastAPI application, configure middleware and register the API routes used by the frontend.

This file acts as the gateway between the React frontend and the backend services.

## How It Works

When the backend starts:

• FastAPI is initialised.
• Cross-Origin Resource Sharing (CORS) is configured.
• API routers are loaded.
• Application endpoints become available.
• The frontend can begin sending requests.

The file is responsible for preparing the entire backend environment before any training data is accessed.

## FastAPI Initialisation

The application is created using:

• FastAPI()

The application is configured with the title:

• Cyber Risk & Awareness Hub

This title is displayed in the automatically generated FastAPI documentation and identifies the API service.

## CORS Configuration

The application uses CORSMiddleware to allow the React frontend to communicate with the backend.

Approved frontend addresses include:

• http://localhost:5173
• http://127.0.0.1:5173

These addresses are used by the Vite development server during local development.

Without CORS configuration, the browser would block requests between the frontend and backend because they run on different ports.

## Middleware Configuration

The middleware is configured to allow:

• Credentials.
• All HTTP methods.
• All request headers.

This provides flexibility during development and allows the frontend to perform all required API operations.

## Router Registration

The application loads and registers three API routers:

### domains_router

Provides endpoints related to cyber security training domains.

Examples:

• Phishing & Social Engineering
• Passwords & Authentication
• Malware & Ransomware

### scenarios_router

Provides endpoints related to:

• Scenario retrieval
• Answer submission
• Progress tracking
• Completion statistics

This router contains most of the training system functionality.

### admin_router

Provides administrative endpoints.

Functions include:

• User progress reset
• Administrative controls

Each router is imported from the api.v1 package and attached to the main FastAPI application.

## Root Endpoint

The file defines a root endpoint:

• GET /

When accessed, the endpoint returns:

• API status
• Confirmation message

Example response:

{
  "status": "ok",
  "message": "Cyber Risk & Awareness Hub API running"
}

This provides a simple health check that confirms the backend is operating correctly.

## Frontend Communication

The React frontend communicates with the backend through the routes registered in this file.

The communication flow is:

Frontend (React)
↓
api.ts
↓
FastAPI Routes
↓
Business Logic
↓
Response Returned

This allows training data, progress information and administrative actions to move between the frontend and backend.

## Development Environment

During development:

• The frontend runs on Vite.
• The backend runs on FastAPI.
• CORS allows communication between both services.

This enables the frontend and backend to be developed independently while still functioning as a single application.

## Why This File Is Important

main.py is the backend starting point for the Cyber Risk & Awareness Hub.

Without this file:

• The FastAPI application would not start.
• Routes would not be registered.
• Frontend requests would fail.
• Domain and scenario data would be inaccessible.

It acts as the central backend configuration file and provides the foundation for all API functionality used throughout the application.


# domains.py – Training Domain Management

## Purpose

domains.py manages the cyber security training categories used throughout the Cyber Risk & Awareness Hub.

It provides a central location for defining the training domains that users can access from the Home dashboard.

Each domain represents a specific cyber security topic and acts as a container for related training scenarios.

## How It Works

The file stores a predefined list of training domains.

When the frontend requests available training topics, this file returns the domain information through API endpoints.

The domains are then displayed on the Home screen where users can choose which topic they wish to study.

## Domain Structure

Each domain contains:

• A unique identifier (id).
• A display title (title).

Example:

• passwords → Passwords & Authentication
• phishing → Phishing & Social Engineering

The identifier is used internally by the application while the title is displayed to users.

## Current Training Domains

The application currently contains eight cyber security domains:

### Passwords & Authentication

Covers password security, multi-factor authentication and account protection.

### Phishing & Social Engineering

Covers suspicious emails, malicious links and social engineering attacks.

### Credential Theft

Focuses on account compromise, login security and stolen credentials.

### Business Email Compromise

Covers fraudulent payment requests, supplier fraud and executive impersonation attacks.

### Malware & Ransomware

Focuses on malicious software, infected attachments and ransomware threats.

### Impersonation & Deepfakes

Covers identity spoofing, fake communications and AI-generated impersonation attacks.

### Data Handling & Oversharing

Focuses on protecting sensitive information and preventing accidental data disclosure.

### Devices, Remote & Physical Risk

Covers remote working security, device protection and physical security threats.

## API Endpoints

### GET /api/v1/domains

Returns all available training domains.

Example use:

• Home dashboard loading.
• Training topic selection.

Example response:

{
  "domains": [...]
}

### GET /api/v1/domains/{domain_id}

Returns information for a specific domain.

Example:

• /api/v1/domains/phishing

If the domain exists, its details are returned.

If the domain does not exist, an error response is generated.

## Frontend Integration

The React frontend accesses this file through:

• apiGetDomains()

The returned domain list is displayed on the Home page and allows users to navigate into individual training areas.

The selected domain identifier is then used to retrieve the relevant scenarios from the scenario engine.

## Navigation Flow

The domain selection process follows this sequence:

Home Dashboard
↓
Domain Selection
↓
Domain ID Retrieved
↓
Scenario Request
↓
Scenario List Displayed

This allows training content to be organised into logical categories.

## Why This File Is Important

domains.py acts as the central source of truth for all training categories within the Cyber Risk & Awareness Hub.

Without this file:

• Training topics would not exist.
• Scenario grouping would not be possible.
• Navigation between training areas would fail.
• The Home dashboard would have no content to display.

It provides the organisational structure that allows scenarios to be grouped into meaningful cyber security learning areas.








