lib/
├── core/                        # Global, shared framework logic
│   ├── network/                 # API client, interceptors, error handling
│   ├── theme/                   # App styling, colors, text styles
│   ├── utils/                   # Extensions, formatters, global constants
│   └── widgets/                 # Reusable global UI (buttons, loaders, dialogs)
│
├── features/                    # Encapsulated product features
│   ├── authentication/
│   │   ├── models/              # Feature data structures
│   │   ├── presenters/          # Feature state and business logic
│   │   ├── views/               # Feature UI screens and components
│   │   └── repositories/        # Feature data fetching/auth services
│   │
│   ├── dashboard/
│   │   ├── models/
│   │   ├── presenters/
│   │   └── views/
│   │
│   └── profile/
│       ├── models/
│       ├── presenters/
│       └── views/
│
├── main.dart                    # Application entry point
└── app.dart                     # MaterialApp initialization & routing config