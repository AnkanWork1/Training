# Backend Architecture — Week 4 Day 1

## Design Philosophy
- Explicit lifecycle management
- Strict separation of concerns
- Fail-fast initialization
- Observable runtime behavior

## Boot Order
1. Environment config
2. Logger
3. Database
4. Express app
5. Routes
6. Server listener

## Folder Responsibilities
- config/      → Environment & runtime configuration
- loaders/     → Dependency orchestration
- services/    → Business logic
- repositories/→ Data access
- utils/       → Shared infrastructure

## Shutdown Strategy
- Stop accepting new requests
- Close open connections
- Flush logs
- Exit process
