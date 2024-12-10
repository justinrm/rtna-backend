# FRONTEND_TODO

## Overview
The frontend for the **Regional News Aggregator** platform will be built with **React**, using **Axios** for API integration and **Tailwind CSS** for styling. The design theme will combine **"Wall Street Formality"** with a **"Great Gatsby aesthetic"**, emphasizing a **futuristic, seamless scrolling experience**, inspired by [Northrop Grumman](https://www.northropgrumman.com/).

The frontend will initially be deployed using **Netlify**, leveraging its ease of use, continuous deployment capabilities, and environment variable management.

---

## Directions for the Frontend

### **1. Framework and Libraries**
- **React**:
  - Use **React 18+** for building a modern and responsive user interface.
  - Use **React Router** for navigation between pages.
- **Axios**:
  - Centralize API integration with Axios.
  - Manage authentication tokens using Axios interceptors.
- **Tailwind CSS**:
  - Implement a custom Tailwind CSS theme for a "Wall Street meets Gatsby" aesthetic with seamless scrolling.

---

### **2. Netlify-Specific Configuration**
- **Setup**:
  - Link the frontend repository to Netlify.
  - Configure **environment variables** in the Netlify dashboard for sensitive data (e.g., `REACT_APP_API_URL`).
- **Environment Variables**:
  - Example `.env` file:
    ```env
    REACT_APP_API_URL=https://api.example.com
    ```

- **Netlify Build Settings**:
  - Build Command: `npm run build`
  - Publish Directory: `build/`

- **Continuous Deployment**:
  - Enable auto-deploys from the main branch for CI/CD.
  - Use Netlify’s **branch preview URLs** for staging.

---

### **3. Theming and Design**
- **General Theme**:
  - **Colors**: Gold, black, and white for primary palette; metallic accents for highlights.
  - **Typography**: Use serif fonts (e.g., Playfair Display) for headlines and clean sans-serif fonts (e.g., Lato) for body text.
  - **Animations**: Implement smooth hover effects, parallax scrolling, and fading transitions for a futuristic aesthetic.

- **Tailwind CSS Configuration**:
  - Add custom styles in `tailwind.config.js`:
    ```javascript
    module.exports = {
      content: ["./src/**/*.{js,jsx,ts,tsx}"],
      theme: {
        extend: {
          colors: {
            gold: "#D4AF37",
            black: "#1A1A1A",
            white: "#FFFFFF",
            metallic: "#C0C0C0",
          },
          fontFamily: {
            headline: ["Playfair Display", "serif"],
            body: ["Lato", "sans-serif"],
          },
          spacing: {
            "128": "32rem",
          },
        },
      },
      plugins: [require("@tailwindcss/typography"), require("tailwind-scrollbar")],
    };
    ```

---

### **4. Key Features and Components**

#### **4.1. User Authentication**
- **Login and Registration**:
  - Create forms with React Hook Form for easy validation.
  - Use Axios for API integration with `/users/register` and `/users/token`.
  - Manage authentication tokens using localStorage:
    ```javascript
    const login = async (email, password) => {
      try {
        const response = await apiClient.post("/users/token", {
          username: email,
          password,
        });
        localStorage.setItem("token", response.data.access_token);
      } catch (error) {
        console.error("Login failed:", error);
      }
    };
    ```

---

#### **4.2. News Aggregation**
- **Homepage**:
  - Use `/articles` API to fetch and display news articles in a scrollable grid.
  - Features:
    - Filters for categories, sources, and keywords.
    - Hover effects for summaries and additional details.

- **Interactive Article Cards**:
  - Example card component using Tailwind CSS:
    ```html
    <div class="bg-black text-gold p-4 shadow-lg rounded-lg hover:shadow-xl transition-all">
      <h2 class="font-headline text-xl mb-2">Article Title</h2>
      <p class="font-body text-sm text-white">Summary...</p>
      <button class="mt-2 bg-gold text-black px-4 py-2 rounded-full">
        Read More
      </button>
    </div>
    ```

---

#### **4.3. Real-Time Updates**
- **Weather Widget**:
  - Use `/weather` API to display real-time weather data for Lewiston.
  - Example widget:
    ```html
    <div class="bg-metallic text-black p-6 rounded-lg shadow-md">
      <h2 class="text-xl font-headline">Lewiston Weather</h2>
      <p class="text-lg font-body">75°F, Sunny</p>
    </div>
    ```

- **Emergency Alerts**:
  - Create an alert banner for critical updates from `/alerts`:
    ```html
    <div class="bg-red-600 text-white p-3 text-center">
      <p>Emergency Alert: Severe Weather Warning</p>
    </div>
    ```

---

#### **4.4. Admin Dashboard**
- **Source Management**:
  - Use `/sources` and `/sources/refresh` endpoints to display and manage sources.
  - Paginated table for source listing and validation.

- **Feedback Analytics**:
  - Use charts (e.g., `recharts` or `chart.js`) to display trends from `/feedback` API.

---

### **5. Seamless Scrolling and Animations**
- **Infinite Scroll**:
  - Use `react-infinite-scroll-component` for loading articles dynamically.
- **Parallax Scrolling**:
  - Use `react-parallax` to create interactive scrolling effects.

---

### **6. Best Practices**

#### **Styling**
- Use Tailwind's utility-first classes for clean and maintainable CSS.
- Avoid inline styles; use reusable components instead.

#### **State Management**
- Use React Context or Redux for managing global states (e.g., user authentication, preferences).
- Memoize expensive operations to optimize performance.

#### **Accessibility**
- Ensure all components meet WCAG standards.
- Use semantic HTML and ARIA attributes for interactive elements.

#### **Performance**
- Optimize API calls with caching and Axios interceptors.
- Use `React.memo` and `React.lazy` to optimize rendering.

---

### **7. Deployment with Netlify**
- **Netlify Setup**:
  - Connect your GitHub repository to Netlify.
  - Configure the build settings:
    - Build Command: `npm run build`
    - Publish Directory: `build/`
  - Enable continuous deployment for auto-deploys on every push to `main`.

- **Environment Variables**:
  - Add `REACT_APP_API_URL` in Netlify's environment variable settings.

- **Optimize Tailwind CSS**:
  - Enable purging of unused CSS for smaller bundle sizes:
    ```javascript
    module.exports = {
      purge: ["./src/**/*.{js,jsx,ts,tsx}"],
    };
    ```

---

## Action Items for Frontend Developers
1. **Implement the Design**:
   - Create responsive components (article cards, admin dashboard, etc.).
   - Integrate animations for seamless scrolling and parallax effects.

2. **Integrate APIs**:
   - Use Axios to connect the frontend to the backend APIs.
   - Manage authentication tokens and error handling globally.

3. **Testing**:
   - Write tests with Jest or Cypress for all key workflows (e.g., login, article fetching).
   - Ensure the frontend is fully accessible and performs well on mobile devices.

4. **Deploy to Netlify**:
   - Set up environment variables and enable continuous deployment.
   - Test staging URLs for bugs and design consistency before going live.

