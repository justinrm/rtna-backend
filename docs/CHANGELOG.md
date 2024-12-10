
# Changelog

## Changes from Original Knowledgebase Tarball
1. **Directory Restructure**:
   - Organized files into `api/`, `modules/`, `utilities/`, `models/`, and `tasks/` directories.
   - Improved modularity and scalability.

2. **Feature Enhancements**:
   - Added robust user authentication and registration.
   - Implemented article and source management with CRUD APIs.

3. **Caching and Performance**:
   - Integrated Redis for caching weather and alert data.
   - Added Celery for task scheduling and periodic updates.

4. **Code Quality**:
   - Added testing scaffolding for utilities and APIs.
   - Improved logging, error handling, and input validation.

5. **Documentation and Configuration**:
   - Created a `.env.example` for environment variables.
   - Enhanced documentation for developers and contributors.
