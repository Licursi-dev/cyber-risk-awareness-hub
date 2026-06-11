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


# scenarios.py – Scenario Engine and Progress Tracking

## Purpose

scenarios.py is the main training engine for the Cyber Risk & Awareness Hub.

This file stores the cyber security scenarios, controls answer submission, tracks user progress, calculates completion results and provides progress reset functionality.

It is one of the most important backend files in the project because it contains the core learning logic.

## How It Works

The file uses a FastAPI router to expose scenario-related API endpoints.

These endpoints allow the frontend to:

• Retrieve all scenarios.
• Retrieve scenarios for a specific domain.
• Load a single scenario.
• Submit an answer.
• Track progress for a Staff ID.
• Calculate completion summaries.
• Reset progress.

## Scenario Data

The file contains a SCENARIOS list.

Each scenario includes:

• Scenario ID.
• Domain ID.
• Title.
• Difficulty level.
• Question text.
• Answer options.
• Correct answer.
• Explanation.
• Points value.

The scenarios are grouped by cyber security domain.

## Current Scenario Domains

The file includes scenarios for:

• Phishing.
• Passwords.
• Business Email Compromise.
• Credential Theft.
• Malware & Ransomware.
• Impersonation & Deepfakes.
• Data Handling & Oversharing.
• Devices, Remote & Physical Risk.

Each domain contains three scenarios.

The scenarios are designed with different difficulty levels:

• Easy.
• Medium.
• Hard.

## Points System

Each scenario has a points value.

The points increase based on difficulty:

• Easy scenarios are worth fewer points.
• Medium scenarios are worth more points.
• Hard scenarios are worth the most points.

When a user submits a correct answer, the backend awards the scenario's points.

Incorrect answers receive zero points.

## Public Scenario Views

The file includes helper functions to control what data is sent to the frontend.

### _public_list_item()

Returns a simplified version of a scenario.

This includes:

• ID.
• Domain.
• Title.
• Difficulty.

This is used when displaying scenario lists.

### _public_detail()

Returns the full scenario information needed for the question screen.

This includes:

• ID.
• Domain.
• Title.
• Difficulty.
• Question.
• Answer options.
• Points.

The correct answer is not sent in this public detail response, which helps prevent the frontend from exposing the answer before submission.

## Progress Storage

Progress is stored in an in-memory dictionary called PROGRESS.

The structure is:

• Staff ID.
• Scenario ID.
• Completion status.
• Correct or incorrect result.
• Selected option.
• Points awarded.

This allows the backend to track progress separately for each Staff ID.

Example structure:

PROGRESS[staff_id][scenario_id]

This means each user can have their own training progress.

## Staff ID Tracking

When a user submits an answer, the backend checks the Staff ID.

If the Staff ID does not already exist in PROGRESS, a new progress record is created for that user.

This allows multiple users to complete training separately during the same backend session.

## Answer Submission

The submit_answer() function handles user answers.

When an answer is submitted:

1. The Staff ID is checked.
2. The Scenario ID is checked.
3. The selected option is checked.
4. The matching scenario is found.
5. The answer is compared with the correct answer.
6. Points are awarded if the answer is correct.
7. Progress is saved for the Staff ID.
8. The result is returned to the frontend.

## Scenario Locking

The file prevents users from repeatedly answering the same scenario to gain more points.

If a scenario has already been completed by a Staff ID, the backend returns:

• already_attempted: True
• locked: True
• Previous correctness result
• Previous points awarded
• Explanation text

This means the first answer counts and later attempts do not overwrite the result.

## API Endpoints

### GET /api/v1/scenarios

Returns a list of all scenarios.

This is useful for retrieving all available training content.

### GET /api/v1/scenarios/{domain_id}

Returns scenarios belonging to a selected domain.

This is used when a user opens a training topic from the Home dashboard.

### GET /api/v1/scenario/{scenario_id}

Returns the full details for one selected scenario.

This is used when the user opens a specific scenario to answer.

### POST /api/v1/submit

Processes a user's submitted answer.

The request includes:

• Staff ID.
• Scenario ID.
• Selected option.

The response includes:

• Whether the answer was correct.
• Whether the scenario had already been attempted.
• Points awarded.
• Explanation text.
• Updated progress.

### GET /api/v1/progress/{staff_id}

Returns the raw progress data for a specific Staff ID.

This is useful for checking what scenarios a user has completed.

### GET /api/v1/completion/{staff_id}

Returns a full completion summary for a Staff ID.

This endpoint calculates:

• Total scenarios attempted.
• Correct answers.
• Overall score.
• Domain-by-domain progress.
• Pass or fail status.
• Training completion status.

### POST /api/v1/admin/reset

Resets progress data.

If a Staff ID is provided, only that user's progress is reset.

If no Staff ID is provided, all progress records are reset.

## Completion Calculation

The completion_summary() function calculates progress across all training domains.

For each domain, it checks:

• How many scenarios exist.
• How many have been attempted.
• How many were answered correctly.
• The user's score percentage.
• Whether the domain has been passed.

A domain is passed when:

• All scenarios in the domain have been attempted.
• The score percentage is at least 70%.

## Pass Mark

The pass mark is controlled by:

PASS_MARK_PERCENT = 70

This means users must achieve at least 70% in a completed domain for it to be marked as passed.

## Overall Training Status

The system calculates whether the whole training programme is complete.

Training is complete only when all domains containing scenarios have been passed.

The backend returns this information to the frontend so the Home and Summary pages can display the user's progress.

## Error Handling

The file includes basic validation for missing data.

It checks for:

• Missing Staff ID.
• Missing Scenario ID.
• Missing selected option.
• Unknown Scenario ID.

If required data is missing, an error response is returned.

## Prototype Storage Limitation

The current version uses in-memory storage.

This means progress is stored while the FastAPI server is running.

If the backend server restarts, the stored progress is cleared.

In a production version, this would be replaced with persistent database storage.

## Why This File Is Important

scenarios.py is the core backend engine of the Cyber Risk & Awareness Hub.

It controls the main learning experience by managing:

• Training content.
• Scenario retrieval.
• Answer checking.
• Score calculation.
• User progress tracking.
• Domain completion.
• Training completion.
• Admin progress reset.

This file demonstrates how backend logic can support an interactive cyber security training application.



# admin.py – Administrative Progress Management

## Purpose

admin.py provides administrative functionality for the Cyber Risk & Awareness Hub.

Its primary purpose is to allow authorised administrators to reset user progress during testing and development.

This file adds a simple security layer through the use of an administrator PIN before any reset actions can be performed.

## How It Works

The file creates an administrative API router that is separate from the main scenario endpoints.

When a reset request is received:

• The admin PIN is checked.
• The target Staff ID is validated.
• The progress store is searched.
• Matching user progress is reset.
• A status message is returned to the frontend.

This allows administrators to clear progress without manually editing backend data.

## Administrative Security

The file uses a simple prototype security system.

The administrator PIN is defined as:

• 1234

The PIN must be supplied in the request header:

• x-admin-pin

If the PIN does not match, access is denied.

## Authentication Validation

Before any reset action is performed, the system checks:

• Whether a PIN was provided.
• Whether the PIN matches the configured administrator PIN.

If validation fails, the API returns:

• HTTP 403 Forbidden

This prevents unauthorised users from accessing administrative functions.

## Reset Request Structure

The file uses a ResetPayload model.

The request contains:

• staff_id

This identifies which user should have their progress reset.

Using a structured request model helps validate incoming data before processing.

## Active User Reset Mode

The application supports a special administrator override mode.

Using:

• PIN = 1234
• Staff ID = admin

activates the administrator shortcut.

When this occurs:

• The most recently active user is located.
• Their progress is cleared.
• A confirmation message is returned.

This was added to simplify testing during development.

## Manual User Reset

If a specific Staff ID is supplied, the system searches the progress store.

When a matching Staff ID is found:

• The user's progress is cleared.
• Their score is reset.
• Their completed scenarios are removed.

A success message is then returned.

## Progress Reset Structure

When progress is reset, the user's stored data becomes:

• Empty domain progress.
• Score set to zero.
• No completed scenarios.

This effectively returns the user to a fresh starting state.

## No Match Handling

If the supplied Staff ID cannot be found:

• No changes are made.
• A status message is returned.

This prevents errors when administrators accidentally enter an incorrect Staff ID.

## API Endpoint

### POST /api/v1/admin/reset

Processes administrative progress reset requests.

The request includes:

• Admin PIN (header)
• Staff ID (request body)

The response returns:

• Status information.
• Success confirmation.
• Error information when applicable.

## Frontend Integration

The React frontend accesses this endpoint through:

• apiAdminResetProgress()

The Admin screen allows an administrator to:

• Enter the PIN.
• Enter a Staff ID.
• Submit the reset request.
• View the result message.

This provides a simple management interface without needing direct backend access.

## Development Purpose

This administrative system was created primarily for:

• Application testing.
• Demonstrations.
• Scenario retesting.
• Development validation.

It allows progress to be reset quickly without restarting the backend.

## Production Considerations

The current implementation is a prototype.

In a production environment, the following improvements would be recommended:

• User authentication.
• Role-based access control.
• Secure password storage.
• Audit logging.
• Administrative user accounts.
• Database-backed permissions.

A hard-coded PIN would not normally be used in a live system.

## Why This File Is Important

admin.py provides administrative control over user progress within the Cyber Risk & Awareness Hub.

Without this file:

• Progress could not be reset easily.
• Testing would be slower.
• Demonstrations would require backend restarts.
• Administrative actions would require direct code changes.

This file supports the management and maintenance of the training environment while development and testing are taking place.



# main.tsx – Frontend Application Entry Point

## Purpose

main.tsx is the frontend entry point for the Cyber Risk & Awareness Hub.

Its responsibility is to start the React application and render the main App component into the browser.

This file acts as the first piece of frontend code executed when the application loads.

## How It Works

When the application starts:

• The React library is loaded.
• The ReactDOM rendering engine is loaded.
• The App component is imported.
• Global styling is imported.
• React creates the application root.
• The App component is rendered inside the webpage.

This process starts the entire frontend interface.

## React Imports

The file imports:

• React
• ReactDOM

These libraries provide the functionality required to build and display the user interface.

React manages components and state, while ReactDOM handles rendering content into the browser.

## App Component Loading

The file imports:

• App.tsx

The App component contains the main application logic and user interface.

Once loaded, App becomes the root component for the entire frontend application.

All screens, navigation and functionality are controlled through this component.

## Global Styling

The file imports:

• styles/app.css

This stylesheet provides the visual appearance used throughout the application.

Loading the stylesheet at this level ensures that styling is available across all components.

## Root Element

The application is rendered into:

• root

This element is located inside index.html.

React replaces the contents of this element with the application's user interface.

The rendering process begins with:

• ReactDOM.createRoot()

This creates the React rendering container.

## Strict Mode

The application is wrapped inside:

• React.StrictMode

Strict Mode is a React development feature that helps identify potential issues during development.

Benefits include:

• Detecting unsafe code.
• Highlighting deprecated features.
• Encouraging best practices.
• Improving application stability.

Strict Mode is primarily used during development and does not affect the production user experience.

## Application Flow

The frontend startup process follows this sequence:

Browser
↓
index.html
↓
main.tsx
↓
App.tsx
↓
Application Interface

This allows React to initialise and display the Cyber Risk & Awareness Hub.

## Why This File Is Important

main.tsx is the frontend starting point for the Cyber Risk & Awareness Hub.

Without this file:

• React would not start.
• App.tsx would never load.
• Styling would not be applied.
• The user interface would not appear.

Although small, this file is essential because it bootstraps the entire frontend application and connects React to the browser.



# App.css – Global Styling System

## Purpose

App.css provides the visual styling for the Cyber Risk & Awareness Hub.

The file controls the application's appearance, layout, typography, buttons, forms and reusable interface components.

It creates a consistent dark-themed design that is used throughout the application.

## How It Works

When the application starts:

• App.css is imported by main.tsx.
• The stylesheet is loaded by the browser.
• Global styling rules are applied.
• Reusable component styles become available.
• The user interface adopts a consistent appearance.

This allows all pages to share the same design system.

## Theme Configuration

The file begins by defining:

• color-scheme: dark

This informs the browser that the application is designed for dark mode.

Compatible browsers can then automatically adjust built-in controls to better match the application's appearance.

## Global Body Styling

The body element defines the main application appearance.

Features include:

• Dark background colour.
• Light text colour.
• System font stack.
• Zero page margin.

This creates the foundation used by every screen in the application.

## Layout System

### Container

The .container class provides a central content area.

Features include:

• Maximum width control.
• Automatic horizontal centring.
• Consistent page padding.

This prevents content from becoming too wide on large displays.

### Row

The .row class creates flexible horizontal layouts.

Features include:

• Flexbox layout.
• Automatic wrapping.
• Consistent spacing.
• Vertical alignment.

This is useful for buttons, controls and grouped content.

### Spacer

The .spacer class provides vertical spacing between sections.

This helps improve readability and page structure.

## Typography

### Main Heading

The .h1 class provides large heading styling.

Features include:

• Large font size.
• Tight line spacing.
• Reduced letter spacing.

This helps create strong visual page titles.

### Muted Text

The .muted class is used for secondary information.

Examples include:

• Help text.
• Explanations.
• Status information.

Reduced opacity makes this content less visually dominant.

## Card System

The .card class creates reusable content panels.

Features include:

• Rounded corners.
• Border styling.
• Internal padding.
• Semi-transparent background.

Cards are used throughout the application to group related information.

## Button Styling

The .btn class defines the standard application button.

Features include:

• Rounded corners.
• Dark background.
• Light text.
• Border styling.
• Pointer cursor.
• Consistent padding.

### Disabled Buttons

Disabled buttons automatically:

• Reduce opacity.
• Remove interactive cursor behaviour.

This provides visual feedback when actions are unavailable.

## Form Styling

### Input Fields

The .input class controls text field appearance.

Features include:

• Full-width layout.
• Maximum width restriction.
• Dark theme styling.
• Rounded corners.
• Consistent padding.
• Readable font size.

This is used for Staff ID entry and administrative controls.

## List Components

### List Container

The .list class provides structured list layouts.

Features include:

• Grid display.
• Consistent spacing.
• No default list styling.

### List Items

The .item class styles individual list entries.

Features include:

• Flexbox alignment.
• Internal spacing.
• Rounded corners.
• Border styling.
• Hover-ready structure.

This is suitable for domains, scenarios and other selectable items.

## Status Badges

The .badge class creates pill-shaped status indicators.

Features include:

• Rounded appearance.
• Small font size.
• Border styling.
• Semi-transparent background.

Badges can be used to display status information and metadata.

## KPI Styling

The .kpi class emphasises important values.

Examples include:

• Scores.
• Percentages.
• Completion figures.

The heavier font weight improves visibility.

## Status Colours

The stylesheet defines several status classes.

### Success

The .success class displays positive information.

Examples:

• Passed domains.
• Successful actions.

### Warning

The .warn class highlights cautionary information.

Examples:

• In-progress status.
• Pending actions.

### Error

The .error class displays error messages.

Examples:

• Failed requests.
• Validation errors.

## Small Links

The .smalllink class styles secondary links.

Features include:

• Smaller text size.
• Underlined appearance.
• Reduced opacity.
• Pointer cursor.

These links are designed for supporting actions rather than primary navigation.

## Design Philosophy

The styling system follows a simple design approach:

• Dark theme.
• Minimal visual clutter.
• Consistent spacing.
• Readable typography.
• Reusable components.

This supports the professional training-focused nature of the application.

## Why This File Is Important

App.css provides the visual identity of the Cyber Risk & Awareness Hub.

Without this file:

• The application would lose its styling.
• Layouts would become inconsistent.
• User interface elements would be harder to use.
• The application would appear unfinished.

This file creates the consistent visual experience used throughout the platform.



# vite.config.ts – Development Server Configuration

## Purpose

vite.config.ts configures the Vite development environment used by the Cyber Risk & Awareness Hub.

Its primary role is to control how the React frontend behaves during development and how API requests are routed to the FastAPI backend.

This file allows the frontend and backend to work together without requiring complicated configuration from the user.

## How It Works

When the frontend development server starts:

• Vite loads the configuration file.
• React support is enabled.
• Development server settings are applied.
• API proxy rules are created.
• The application becomes available in the browser.

This allows frontend development to take place while the backend runs separately.

## React Integration

The configuration imports:

• @vitejs/plugin-react

This plugin provides React support within Vite.

Features include:

• React component compilation.
• Fast refresh during development.
• JSX and TSX support.
• Improved development experience.

The plugin is registered using:

• plugins: [react()]

This enables React functionality throughout the project.

## Development Server

The file configures the Vite development server.

During development the frontend runs separately from the backend.

Typical development addresses include:

• Frontend: http://localhost:5173
• Backend: http://127.0.0.1:8000

Because they operate on different ports, a proxy is required to simplify communication.

## API Proxy Configuration

The configuration creates a proxy for:

• /api

Any request beginning with /api is automatically forwarded to the backend server.

Example:

Frontend request:

/api/v1/domains

Automatically becomes:

http://127.0.0.1:8000/api/v1/domains

This allows frontend code to use simple relative paths without needing to know the backend address.

## Proxy Target

The configured backend target is:

• http://127.0.0.1:8000

This is the FastAPI server used during development.

All API requests are forwarded to this address.

## Change Origin

The proxy enables:

• changeOrigin: true

This modifies the request origin header so that requests appear to originate from the proxy server.

This helps avoid communication issues between development services.

## Secure Mode

The proxy uses:

• secure: false

This allows communication even when HTTPS certificates are not being used.

This is common in local development environments.

## Frontend and Backend Communication

The communication process works as follows:

Browser
↓
React Frontend
↓
Vite Proxy
↓
FastAPI Backend
↓
API Response
↓
React Frontend

The proxy makes this process transparent to the application.

## Development Benefits

Using a proxy provides several advantages:

• Simpler API requests.
• Cleaner frontend code.
• Reduced configuration complexity.
• Easier local development.
• Consistent API paths.

The frontend can make requests using relative URLs without needing to store backend addresses throughout the codebase.

## Production Considerations

The proxy is primarily a development feature.

In a production deployment:

• The frontend is normally built into static files.
• The backend is deployed separately.
• Environment variables may be used.
• Reverse proxies such as Nginx may handle routing.

The development proxy is therefore mainly intended for local testing and development.

## Why This File Is Important

vite.config.ts controls how the Cyber Risk & Awareness Hub frontend operates during development.

Without this file:

• React support would not be configured.
• API requests would fail locally.
• Frontend and backend communication would be more difficult.
• Development would be slower and more complex.

This file provides the bridge between the React frontend and the FastAPI backend while the application is being developed and tested.










