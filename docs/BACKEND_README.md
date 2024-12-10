# BACKEND_TODO

## Overview
The backend for the **Regional News Aggregator** platform is designed to serve localized, real-time news for Lewiston, Idaho. This backend aggregates news, manages user feedback, provides weather and emergency alerts, and ensures transparency in content sourcing. The following tasks focus on completing, enhancing, and optimizing the backend for seamless integration with the frontend and scalability for future expansion.

---

## Missing Features and Enhancements

### **1. Real-Time Updates for Aggregation**
- **Feature**: Add an API endpoint to trigger source discovery or RSS aggregation manually.
- **Path**: `/sources/refresh`.
- **Use Case**: Allows admins to trigger real-time updates for sources or articles.
- **Implementation**:
  - Extend `source_discovery.py` and `content_aggregation.py` to support real-time execution.
  - Return a summary of discovered sources and aggregated articles.
  - Add logging for tracking triggered updates.

---

### **2. Source Status Management**
- **Feature**: Add functionality to manage the status (`active`/`inactive`) of sources based on validation checks.
- **Use Case**: Improves source reliability tracking and ensures invalid sources are marked appropriately.
- **Implementation**:
  - Add a `status` column to the `sources` table (`active`, `inactive`, `pending`).
  - Extend `source_discovery.py` to periodically validate sources and update their status.
  - Create a new API endpoint (`/sources/update-status`) to allow admins to manually change source statuses.

---

### **3. Feedback Analysis**
- **Feature**: Create a new module, `modules/feedback_analysis.py`, for analyzing and reporting user feedback trends.
- **Functionality**:
  - Analyze `feedback` table to identify:
    - Most liked/disliked articles.
    - Most flagged sources.
    - Feedback trends over time.
  - Provide APIs for exporting feedback summaries.
- **Use Case**: Helps admins improve content curation and identify user preferences.

---

### **4. User Personalization**
- **Feature**: Allow users to save preferences for:
  - Article categories.
  - Keywords.
  - Preferred sources.
- **Implementation**:
  - Add a `preferences` JSON column to the `users` table.
  - Extend `users.py` API to handle CRUD operations for user preferences.
  - Modify `content_aggregation.py` to filter articles based on user preferences.

---

### **5. API Rate Limiting**
- **Feature**: Implement rate limiting for public-facing APIs to prevent abuse.
- **Tools**: Use FastAPI middleware or Redis-based throttling.
- **Implementation**:
  - Protect sensitive endpoints such as `/users/register`, `/articles`, and `/sources`.
  - Log violations to monitor abuse and enforce limits (e.g., 100 requests per hour).

---

### **6. Alerts for Source or Aggregation Failures**
- **Feature**: Add a module for notifying admins about failures in source discovery or article aggregation.
- **Implementation**:
  - Integrate email notifications using SMTP or a service like SendGrid.
  - Add Slack or webhook alerts for critical failures.
  - Allow customizable thresholds for sending alerts (e.g., failure count or severity).

---

### **7. Source Discovery Enhancements**
- **Feature**: Extend `source_discovery.py` for dynamic source discovery.
- **Functionality**:
  - Use external APIs like Bing News Search or Google News to discover sources programmatically.
  - Fetch metadata for sources, such as content type and crawlability.
  - Add a feature to suggest sources via the frontend for admin review and approval.

---

### **8. Comprehensive Testing**
- **Feature**: Expand test coverage for the backend to ensure reliability and consistency.
- **Scope**:
  - Source discovery and validation.
  - Article aggregation and deduplication.
  - User feedback APIs.
- **Implementation**:
  - Add tests for:
    - Manual aggregation (`/sources/refresh`).
    - Feedback analysis workflows.
    - User preferences handling.
  - Test error handling for external API failures and database constraints.

---

### **9. Seamless Frontend Integration**
- **Feature**: Ensure the backend is fully compatible with the frontend requirements outlined in `FRONTEND_TODO.md`.
- **Implementation**:
  - Validate `/articles`, `/sources`, `/weather`, and `/alerts` endpoints for complete data coverage.
  - Provide clear error messages and consistent response structures for all APIs.
  - Optimize API performance for large-scale article aggregation to support infinite scrolling on the frontend.

---

## Recommendations

### **Scalability**
- Use Redis for caching article queries and throttling API requests.
- Optimize database queries to handle large datasets efficiently.

### **Transparency**
- Include metadata like fetch timestamps, source reliability scores, and update logs in API responses.

### **Monitoring and Logging**
- Enhance logging to include:
  - API usage patterns.
  - Task scheduling details.
  - Aggregation and validation errors.

### **Documentation**
- Maintain updated documentation for:
  - API endpoints (include request/response examples).
  - Configuration files (e.g., `.env` setup).
  - Deployment steps for Docker and Celery.

---

## Action Items for Backend Developers

1. **Enhance APIs**:
   - Add `/sources/refresh` and `/sources/update-status` endpoints.
   - Extend user-related APIs for managing preferences.

2. **Improve Source Discovery**:
   - Validate sources periodically and mark their status in the database.
   - Integrate external APIs for automatic source discovery.

3. **Build Feedback Analysis**:
   - Analyze and report feedback trends.
   - Provide APIs for exporting feedback summaries.

4. **Implement Notifications**:
   - Add email and webhook notifications for critical system failures.

5. **Expand Testing**:
   - Write tests for aggregation, validation, and feedback workflows.
   - Cover edge cases and error handling scenarios.

6. **Optimize Integration**:
   - Ensure the backend is performant and fully compatible with the frontend.

7. **Deploy and Monitor**:
   - Use Docker and Celery for deployment and task management.
   - Implement monitoring tools to track system health and API usage.

